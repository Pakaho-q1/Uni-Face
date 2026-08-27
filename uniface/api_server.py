import os
import re
import sys
import time
import asyncio
import uuid
import shutil
import cv2
import base64
import hashlib
import json
import queue
from typing import Dict, Any, Optional

from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn
import threading
import numpy as np

# --- TRT Support: Auto-inject TensorRT libs into PATH ---
if sys.platform == 'win32':
    trt_path = os.path.join(sys.prefix, 'Lib', 'site-packages', 'tensorrt_libs')
    if os.path.exists(trt_path):
        os.environ['PATH'] = trt_path + os.pathsep + os.environ.get('PATH', '')
        
    # Silence asyncio Proactor connection reset errors (WinError 10054) on websocket disconnect
    from functools import wraps
    from asyncio.proactor_events import _ProactorBasePipeTransport
    
    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except (ConnectionResetError, RuntimeError):
                pass
        return wrapper
        
    _ProactorBasePipeTransport._call_connection_lost = silence_event_loop_closed(_ProactorBasePipeTransport._call_connection_lost)

# --- Disable BLAS/OMP threading to prevent CPU thrashing during multi-thread processing ---
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

# Ensure we can import uniface.core modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from uniface.core.state import state
from uniface.core.video_service import process_video
from uniface.core.service import process_image

# Load configurations from uni-face.ini
state.init(parse_args=False)

app = FastAPI(title="Uni-Face API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BasicAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] not in ["http", "websocket"]:
            return await self.app(scope, receive, send)
            
        if not state.auth:
            return await self.app(scope, receive, send)

        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode("utf-8")
        
        parts = state.auth.split(":", 1)
        if len(parts) == 2:
            expected_user, expected_pass = parts
        else:
            expected_user, expected_pass = "admin", state.auth
            
        expected = f"Basic {base64.b64encode(f'{expected_user}:{expected_pass}'.encode()).decode()}"
        
        if auth_header != expected:
            if scope["type"] == "http":
                await send({
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [(b"www-authenticate", b'Basic realm="Uni-Face"')]
                })
                await send({
                    "type": "http.response.body",
                    "body": b"Unauthorized",
                })
                return
            elif scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1008})
                return
                
        await self.app(scope, receive, send)

app.add_middleware(BasicAuthMiddleware)

# Replace with actual host/port if not localhost:8000
API_BASE_URL = "http://localhost:8000"



# --- Setup workspace paths
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.join(_ROOT, "workspace")

def get_platform_dir(platform: str) -> str:
    if not platform: platform = "unknown"
    # Use re.sub — str.replace() does not interpret regex patterns
    platform = re.sub(r'[^a-z0-9_]', '_', platform.lower())
    return os.path.join(WORKSPACE_DIR, platform)

def ensure_workspace(platform: str):
    p_dir = get_platform_dir(platform)
    uploads_dir = os.path.join(p_dir, "uploads")
    source_dir = os.path.join(uploads_dir, "source")
    target_dir = os.path.join(uploads_dir, "target")
    outputs_dir = os.path.join(p_dir, "outputs")
    target_sets_dir = os.path.join(p_dir, "target_sets")
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(target_sets_dir, exist_ok=True)
    return uploads_dir, outputs_dir

from uniface.core.db import init_db

# Initialize Deduplication DB
init_db()

def get_target_sets_dir(platform: str) -> str:
    p_dir = get_platform_dir(platform)
    target_sets_dir = os.path.join(p_dir, "target_sets")
    pool_dir = os.path.join(target_sets_dir, ".pool")
    os.makedirs(target_sets_dir, exist_ok=True)
    os.makedirs(pool_dir, exist_ok=True)
    return target_sets_dir

# --- JOB MANAGER ---
class JobManager:
    # Status changes that must be saved immediately (not debounced)
    _IMMEDIATE_SAVE_KEYS = {"status", "error", "output_path"}
    # Minimum seconds between debounced (progress) saves
    _SAVE_DEBOUNCE_SECS = 5.0

    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.cancel_events: Dict[str, threading.Event] = {}
        self.active_websockets: Dict[str, WebSocket] = {}
        self.job_queue = queue.Queue()
        self.jobs_file = os.path.join(WORKSPACE_DIR, "jobs.json")
        self._save_lock = threading.Lock()
        self._last_save_time: float = 0.0
        self.load_jobs()
        
    def load_jobs(self):
        if os.path.exists(self.jobs_file):
            try:
                with open(self.jobs_file, "r", encoding="utf-8") as f:
                    self.jobs = json.load(f)
                    # Reset stuck jobs to failed if server restarted while processing
                    for j_id, j_data in self.jobs.items():
                        if j_data["status"] in ["processing", "pending"]:
                            j_data["status"] = "failed"
                            j_data["error"] = "Server restarted during processing"
            except Exception as e:
                print(f"Error loading jobs: {e}")
                
    def save_jobs(self, force: bool = False):
        """Write jobs to disk.
        
        If force=True, always writes immediately (used for status changes).
        Otherwise debounces: skips write if last save was < _SAVE_DEBOUNCE_SECS ago.
        This avoids hammering the disk with one write per video frame.
        """
        now = time.monotonic()
        if not force and (now - self._last_save_time) < self._SAVE_DEBOUNCE_SECS:
            return
        with self._save_lock:
            try:
                with open(self.jobs_file, "w", encoding="utf-8") as f:
                    json.dump(self.jobs, f, indent=4)
                self._last_save_time = time.monotonic()
            except Exception as e:
                print(f"Error saving jobs: {e}")

    def create_job(self, platform: str) -> str:
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "id": job_id,
            "platform": platform,
            "status": "pending",
            "progress": 0.0,
            "frames_done": 0,
            "total_frames": 0,
            "preview_image": None,
            "output_path": None,
            "error": None
        }
        self.cancel_events[job_id] = threading.Event()
        self.save_jobs(force=True)
        return job_id

    def update_job(self, job_id: str, updates: Dict[str, Any]):
        if job_id in self.jobs:
            self.jobs[job_id].update(updates)
            # Force immediate save when important fields change; debounce progress-only updates
            force = bool(self._IMMEDIATE_SAVE_KEYS & updates.keys())
            self.save_jobs(force=force)
            
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.jobs.get(job_id)
        
    def cancel_job(self, job_id: str):
        if job_id in self.cancel_events:
            self.cancel_events[job_id].set()
            self.update_job(job_id, {"status": "failed", "error": "Cancelled by user"})
            
    def get_active_job_for_platform(self, platform: str) -> Optional[Dict[str, Any]]:
        # Returns the most recent pending or processing job for this platform
        for job_id, job in reversed(self.jobs.items()):
            if job["platform"] == platform and job["status"] in ["pending", "processing"]:
                return job
        return None

job_manager = JobManager()

from fastapi.responses import FileResponse

# --- TARGET SETS ENDPOINTS ---

@app.get("/api/v1/target-sets")
async def get_target_sets(x_client_platform: str = Header("unknown")):
    sets_dir = get_target_sets_dir(x_client_platform)
    result = []
    for set_name in os.listdir(sets_dir):
        if set_name == ".pool":
            continue
            
        set_path = os.path.join(sets_dir, set_name)
        if os.path.isdir(set_path):
            files = []
            for f in os.listdir(set_path):
                if os.path.isfile(os.path.join(set_path, f)):
                    # Note: UI will use this file_id to submit jobs
                    file_id = f"set:{set_name}/{f}"
                    files.append({
                        "filename": f,
                        "file_id": f"set:{set_name}/{f}",
                        "url": f"/api/v1/target-sets/media/{set_name}/{f}?platform={x_client_platform}"
                    })
            result.append({"name": set_name, "files": files})
    return {"target_sets": result}

@app.post("/api/v1/target-sets")
async def create_target_set(name: str = Form(...), x_client_platform: str = Header("unknown")):
    # Sanitize name
    safe_name = re.sub(r'[^a-zA-Z0-9_\-\s]', '', name).strip()
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid set name")
        
    sets_dir = get_target_sets_dir(x_client_platform)
    set_path = os.path.join(sets_dir, safe_name)
    if os.path.exists(set_path):
        raise HTTPException(status_code=400, detail="Target set already exists")
        
    os.makedirs(set_path)
    return {"status": "ok", "name": safe_name}

@app.delete("/api/v1/target-sets/{set_name}")
async def delete_target_set(set_name: str, x_client_platform: str = Header("unknown")):
    sets_dir = get_target_sets_dir(x_client_platform)
    set_path = os.path.join(sets_dir, set_name)
    if os.path.exists(set_path) and os.path.isdir(set_path):
        shutil.rmtree(set_path)
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="Target set not found")

from pydantic import BaseModel
from uniface.core.db import get_hash_path, register_hash, remove_hash

class FileHashInfo(BaseModel):
    filename: str
    hash: str

class PreflightRequest(BaseModel):
    files: list[FileHashInfo]

@app.post("/api/v1/target-sets/preflight")
async def target_sets_preflight(req: PreflightRequest):
    """Checks which hashes already exist in the global pool."""
    results = []
    for f in req.files:
        pool_path = get_hash_path(f.hash)
        if pool_path and os.path.exists(pool_path):
            results.append({"filename": f.filename, "hash": f.hash, "status": "exists"})
        else:
            if pool_path:
                # Stale DB entry, file was deleted from pool
                remove_hash(f.hash)
            results.append({"filename": f.filename, "hash": f.hash, "status": "new"})
    return {"results": results}

class LinkRequest(BaseModel):
    files: list[FileHashInfo]

@app.post("/api/v1/target-sets/{set_name}/link")
async def link_to_target_set(
    set_name: str,
    req: LinkRequest,
    x_client_platform: str = Header("unknown")
):
    """Hardlinks existing files from the pool to the target set."""
    sets_dir = get_target_sets_dir(x_client_platform)
    set_path = os.path.join(sets_dir, set_name)
    if not os.path.exists(set_path) or not os.path.isdir(set_path):
        raise HTTPException(status_code=404, detail="Target set not found")
        
    linked = []
    for f in req.files:
        pool_path = get_hash_path(f.hash)
        if not pool_path or not os.path.exists(pool_path):
            continue # Hash not found, skip linking
            
        target_file_path = os.path.join(set_path, f.filename)
        if os.path.exists(target_file_path):
            continue # File already exists in this set, skip
            
        try:
            os.link(pool_path, target_file_path)
            linked.append({
                "filename": f.filename,
                "file_id": f"set:{set_name}/{f.filename}",
                "url": f"/api/v1/target-sets/media/{set_name}/{f.filename}?platform={x_client_platform}"
            })
        except Exception as e:
            print(f"Error hardlinking {pool_path} to {target_file_path}: {e}")
            
    return {"linked": linked}

@app.post("/api/v1/target-sets/{set_name}/upload")
async def upload_to_target_set(
    set_name: str,
    files: list[UploadFile] = File(...),
    x_client_platform: str = Header("unknown")
):
    sets_dir = get_target_sets_dir(x_client_platform)
    set_path = os.path.join(sets_dir, set_name)
    pool_dir = os.path.join(sets_dir, ".pool")
    if not os.path.exists(set_path) or not os.path.isdir(set_path):
        raise HTTPException(status_code=404, detail="Target set not found")
        
    uploaded = []
    for file in files:
        temp_pool_path = os.path.join(pool_dir, f"temp_{uuid.uuid4().hex}.tmp")
        md5 = hashlib.md5()
        size = 0
        
        try:
            # Chunked reading to prevent Backend OOM on 1-2GB files (Point 3)
            with open(temp_pool_path, "wb") as buffer:
                while chunk := await file.read(1024 * 1024 * 5):  # 5MB chunks
                    md5.update(chunk)
                    buffer.write(chunk)
                    size += len(chunk)
                    
            file_hash = md5.hexdigest()
            _, ext = os.path.splitext(file.filename)
            pool_path = os.path.join(pool_dir, f"{file_hash}{ext}")
            
            # If hash doesn't exist, promote temp file to permanent pool file
            if not os.path.exists(pool_path):
                os.rename(temp_pool_path, pool_path)
                register_hash(file_hash, pool_path, size)
            else:
                # File already in pool, remove the temp copy
                os.remove(temp_pool_path)
                
            target_file_path = os.path.join(set_path, file.filename)
            
            # Hardlink from pool to target set
            if not os.path.exists(target_file_path):
                try:
                    os.link(pool_path, target_file_path)
                except Exception as e:
                    print(f"Error linking {pool_path} to {target_file_path}: {e}")
                    shutil.copy2(pool_path, target_file_path)
                    
            uploaded.append({
                "filename": file.filename,
                "file_id": f"set:{set_name}/{file.filename}",
                "url": f"/api/v1/target-sets/media/{set_name}/{file.filename}?platform={x_client_platform}"
            })
        except Exception as e:
            if os.path.exists(temp_pool_path):
                os.remove(temp_pool_path)
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
            
    return {"uploaded": uploaded}

@app.post("/api/v1/system/gc")
async def run_garbage_collection(x_client_platform: str = Header("unknown")):
    """Sweeps the .pool folder and deletes files with st_nlink == 1 (Point 1)."""
    sets_dir = get_target_sets_dir(x_client_platform)
    pool_dir = os.path.join(sets_dir, ".pool")
    
    if not os.path.exists(pool_dir):
        return {"status": "ok", "deleted_files": 0, "freed_bytes": 0}
        
    deleted_count = 0
    freed_bytes = 0
    
    for filename in os.listdir(pool_dir):
        file_path = os.path.join(pool_dir, filename)
        if os.path.isfile(file_path):
            stat = os.stat(file_path)
            # If st_nlink == 1, only the .pool folder has a reference to this file.
            if stat.st_nlink == 1:
                freed_bytes += stat.st_size
                os.remove(file_path)
                # filename is like "hash.ext", extract hash
                file_hash, _ = os.path.splitext(filename)
                remove_hash(file_hash)
                deleted_count += 1
                
    return {
        "status": "ok", 
        "deleted_files": deleted_count, 
        "freed_bytes": freed_bytes
    }

class DeleteFilesRequest(BaseModel):
    filenames: list[str]

@app.post("/api/v1/target-sets/{set_name}/delete-files")
async def delete_target_set_files(
    set_name: str,
    req: DeleteFilesRequest,
    x_client_platform: str = Header("unknown")
):
    sets_dir = get_target_sets_dir(x_client_platform)
    set_path = os.path.join(sets_dir, set_name)
    if not os.path.exists(set_path) or not os.path.isdir(set_path):
        raise HTTPException(status_code=404, detail="Target set not found")
        
    deleted = []
    for filename in req.filenames:
        file_path = os.path.join(set_path, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            deleted.append(filename)
            
    return {"status": "ok", "deleted": deleted}

@app.get("/api/v1/target-sets/media/{set_name}/{filename}")
async def get_target_set_media(
    set_name: str, 
    filename: str, 
    platform: str = None,
    x_client_platform: str = Header("unknown")
):
    actual_platform = platform if platform else x_client_platform
    sets_dir = get_target_sets_dir(actual_platform)
    file_path = os.path.join(sets_dir, set_name, filename)
    
    if not os.path.exists(file_path):
        # Fallback search if requested via raw browser (no headers)
        for p in os.listdir(WORKSPACE_DIR):
            alt_path = os.path.join(WORKSPACE_DIR, p, "target_sets", set_name, filename)
            if os.path.exists(alt_path):
                file_path = alt_path
                break
                
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

# --- API ENDPOINTS ---
@app.post("/api/v1/upload")
async def upload_files(
    files: list[UploadFile] = File(...),
    type: str = Form("source"),
    x_client_platform: str = Header("unknown")
):
    uploads_dir, _ = ensure_workspace(x_client_platform)
    
    # Validation
    if type not in ["source", "target"]:
        type = "target"
        
    target_folder = os.path.join(uploads_dir, type)
    results = []
    
    for file in files:
        # Read content to hash
        content = await file.read()
        
        # Calculate MD5
        md5_hash = hashlib.md5(content).hexdigest()
        _, ext = os.path.splitext(file.filename)
        
        file_id = f"{type}/{md5_hash}{ext}"
        file_path = os.path.join(target_folder, f"{md5_hash}{ext}")
        
        # Only write if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, "wb") as buffer:
                buffer.write(content)
            
        results.append({"file_id": file_id, "filename": file.filename})
        
    return {"uploaded": results}


class JobStartRequest(BaseModel):
    source_type: str = "image"
    source_file_id: str
    target_file_ids: list[str]
    preview_frequency: int = 15
    preview_enabled: bool = True
    preview_resolution: int = 320
    processors: list[str] = ["swap", "restore"]
    swap_model: str = "inswapper_128"
    swap_weight: float = 0.65
    restore_model: str = "gfpgan_1.4"
    restore_weight: float = 1.0
    restore_blend: int = 100
    mask_types: list[str] = ["box"]
    mask_regions: list[str] = ['skin', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 'nose', 'mouth', 'u_lip', 'l_lip']
    similarity: bool = False
    providers: list[str] = ["cpu"]
    execution_thread_count: int = 4
    skip_existing: bool = True

def run_job_background(job_id: str, req: JobStartRequest, x_client_platform: str):
    uploads_dir, outputs_dir = ensure_workspace(x_client_platform)
    source_path = os.path.join(uploads_dir, req.source_file_id)
    cancel_event = job_manager.cancel_events[job_id]
    
    # TODO(#1): `state` is a global singleton — safe now because there is exactly 1 worker thread.
    # If the worker pool is ever expanded to support concurrent jobs, each job must receive
    # its own isolated config snapshot instead of writing to this shared object.
    state.init(parse_args=False)
    state.processors = req.processors
    state.swap_model = req.swap_model
    state.swap_weight = req.swap_weight
    state.restore_model = req.restore_model
    state.restore_weight = req.restore_weight
    state.restore_blend = req.restore_blend
    state.mask_types = req.mask_types
    state.mask_regions = req.mask_regions
    state.similarity = req.similarity
    if hasattr(state, "_parse_providers"):
        state._parse_providers(" ".join(req.providers))
    state.execution_thread_count = req.execution_thread_count
    state.source_path = source_path
    
    job_completed_successfully = False
    try:
        if req.source_type == "model":
            # Load the face model
            from uniface.core.face_model import load_face_model
            source_face = load_face_model(req.source_file_id, get_platform_dir(x_client_platform))
        else:
            from uniface.modules.detector import detect
            source_img = cv2.imread(source_path)
            if source_img is None:
                raise Exception("Could not read source image")
                
            source_faces = detect(source_img)
            if not source_faces:
                raise Exception("No face detected in source image")
                
            source_faces.sort(key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
            source_face = source_faces[0]
        
        total_targets = len(req.target_file_ids)
        print(f"Starting job {job_id} with {total_targets} target files: {req.target_file_ids}")
        last_output_path = None
        
        image_in_paths = []
        image_out_paths = []
        video_tasks = []
        
        import mimetypes
        
        for target_id in req.target_file_ids:
            if target_id.startswith("set:"):
                # Format: set:set_name/filename.ext
                target_rel_path = target_id[4:]
                target_path = os.path.join(get_target_sets_dir(x_client_platform), target_rel_path)
            else:
                target_path = os.path.join(uploads_dir, target_id)
                
            target_basename = os.path.basename(target_path)
            source_basename = os.path.basename(req.source_file_id)
            mime_type, _ = mimetypes.guess_type(target_path)
            is_image = mime_type and mime_type.startswith('image')
            
            target_name, _ = os.path.splitext(target_basename)
            source_name, _ = os.path.splitext(source_basename)
            
            out_name = f"out_{source_name[:8]}_{target_name[:8]}"
            if not req.skip_existing:
                out_name += f"_{uuid.uuid4().hex[:6]}"
                
            if is_image:
                ext = os.path.splitext(target_path)[1] or '.jpg'
                out_name += ext
                out_path = os.path.join(outputs_dir, out_name)
                image_in_paths.append(target_path)
                image_out_paths.append(out_path)
            else:
                if not out_name.endswith('.mp4'):
                    out_name += ".mp4"
                out_path = os.path.join(outputs_dir, out_name)
                video_tasks.append((target_path, out_path))
                
            last_output_path = out_path
            
        job_manager.update_job(job_id, {"status": "processing"})
        
        processed_total = 0
        
        # 1. Process all images as a single batch using SwarmEngine
        if image_in_paths:
            from uniface.core.image_service import process_images_swarm
            def img_progress(current: int, total: int, frame: np.ndarray = None):
                nonlocal processed_total
                overall_pct = ((processed_total + current) / total_targets) * 100
                
                updates = {
                    "progress": round(overall_pct, 2),
                    "frames_done": current,
                    "total_frames": total
                }
                
                # Dynamic preview settings
                current_job = job_manager.get_job(job_id)
                preview_enabled = current_job.get("preview_enabled", req.preview_enabled)
                preview_res = current_job.get("preview_resolution", req.preview_resolution)
                
                freq = max(1, req.preview_frequency)
                if preview_enabled and frame is not None and (current == 1 or current % freq == 0 or current == total):
                    h, w = frame.shape[:2]
                    scale = preview_res / max(h, w)
                    if scale < 1.0:
                        preview_frame = cv2.resize(frame, (int(w*scale), int(h*scale)))
                    else:
                        preview_frame = frame
                    _, buffer = cv2.imencode('.jpg', preview_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                    b64 = base64.b64encode(buffer).decode('utf-8')
                    updates["preview_image"] = f"data:image/jpeg;base64,{b64}"
                job_manager.update_job(job_id, updates)
                
            process_images_swarm(source_face, image_in_paths, image_out_paths, progress_callback=img_progress, cancel_event=cancel_event)
            processed_total += len(image_in_paths)

        # 2. Process videos sequentially
        for v_in, v_out in video_tasks:
            if cancel_event.is_set():
                break
                
            job_manager.update_job(job_id, {"output_path": v_out})
            
            def vid_progress(current: int, total: int, frame: np.ndarray = None):
                file_pct = (current / total) if total > 0 else 0
                overall_pct = ((processed_total + file_pct) / total_targets) * 100
                
                updates = {
                    "progress": round(overall_pct, 2),
                    "frames_done": current,
                    "total_frames": total
                }
                
                # Dynamic preview settings
                current_job = job_manager.get_job(job_id)
                preview_enabled = current_job.get("preview_enabled", req.preview_enabled)
                preview_res = current_job.get("preview_resolution", req.preview_resolution)
                
                freq = max(1, req.preview_frequency)
                if preview_enabled and frame is not None and (current == 1 or current % freq == 0 or current == total):
                    h, w = frame.shape[:2]
                    scale = preview_res / max(h, w)
                    if scale < 1.0:
                        preview_frame = cv2.resize(frame, (int(w*scale), int(h*scale)))
                    else:
                        preview_frame = frame
                    _, buffer = cv2.imencode('.jpg', preview_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                    b64 = base64.b64encode(buffer).decode('utf-8')
                    updates["preview_image"] = f"data:image/jpeg;base64,{b64}"
                job_manager.update_job(job_id, updates)
                
            process_video(source_face, v_in, v_out, progress_callback=vid_progress, cancel_event=cancel_event, skip_existing=req.skip_existing)
            processed_total += 1
                
        if not cancel_event.is_set():
            job_manager.update_job(job_id, {"status": "completed", "progress": 100.0, "output_path": last_output_path})
            job_completed_successfully = True
            
    except Exception as e:
        job_manager.update_job(job_id, {"status": "failed", "error": str(e)})
        
    finally:
        # Always clean up uploaded target files — they are no longer needed regardless of outcome.
        # This prevents accumulation of unprocessed files in the workspace after job failures.
        for target_id in set(req.target_file_ids):
            target_path = os.path.join(uploads_dir, target_id)
            try:
                os.remove(target_path)
            except Exception:
                pass
        
        # Only clean up uploaded source image on success.
        # On failure the user may want to retry without re-uploading the same source.
        if req.source_type == "image" and job_completed_successfully:
            try:
                os.remove(source_path)
            except Exception:
                pass



# --- FACE MODELS API ---
@app.get("/api/v1/face-models")
async def list_face_models(x_client_platform: str = Header("unknown")):
    platform_dir = get_platform_dir(x_client_platform)
    models_dir = os.path.join(platform_dir, "face_models")
    if not os.path.exists(models_dir):
        return {"models": []}
    
    models = []
    for f in os.listdir(models_dir):
        if f.endswith(".safetensors"):
            models.append({"name": f})
    return {"models": models}

@app.post("/api/v1/face-models/build")
async def build_face_model(
    name: str = Form(...),
    files: list[UploadFile] = File(...),
    x_client_platform: str = Header("unknown")
):
    platform_dir = get_platform_dir(x_client_platform)
    from uniface.core.face_model import save_face_model
    from uniface.modules.detector import detect
    
    faces = []
    for file in files:
        content = await file.read()
        nparr = np.frombuffer(content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None:
            detected = detect(img)
            if detected:
                # Get the largest face
                detected.sort(key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
                faces.append(detected[0])
                
    if not faces:
        raise HTTPException(status_code=400, detail="No faces detected in the provided images.")
        
    try:
        filepath = save_face_model(name, faces, platform_dir)
        return {"status": "success", "model_name": os.path.basename(filepath), "faces_extracted": len(faces)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/api/v1/jobs")
async def create_job(
    req: JobStartRequest,
    x_client_platform: str = Header("unknown")
):
    job_id = job_manager.create_job(x_client_platform)
    job_manager.update_job(job_id, {
        "preview_enabled": req.preview_enabled,
        "preview_resolution": req.preview_resolution
    })
    
    # Enqueue job instead of starting a new thread immediately
    job_manager.job_queue.put((job_id, req, x_client_platform))
    
    return {"job_id": job_id, "status": "pending"}

class PreviewSettings(BaseModel):
    enabled: bool
    resolution: int

@app.post("/api/v1/jobs/{job_id}/preview")
async def update_preview_settings(job_id: str, settings: PreviewSettings):
    job_manager.update_job(job_id, {
        "preview_enabled": settings.enabled,
        "preview_resolution": settings.resolution
    })
    return {"status": "success"}

# Background Worker Thread
def worker_loop():
    while True:
        try:
            job_id, req, x_client_platform = job_manager.job_queue.get()
            job = job_manager.get_job(job_id)
            
            # Skip if cancelled while in queue
            if job and job.get("status") == "failed" and job.get("error") == "Cancelled by user":
                job_manager.job_queue.task_done()
                continue
                
            run_job_background(job_id, req, x_client_platform)
            job_manager.job_queue.task_done()
        except Exception as e:
            print(f"Worker loop error: {e}")

# Start the worker thread
worker_thread = threading.Thread(target=worker_loop, daemon=True)
worker_thread.start()

@app.get("/api/v1/jobs/active")
async def get_active_job(x_client_platform: str = Header("unknown")):
    job = job_manager.get_active_job_for_platform(x_client_platform)
    if not job:
        return {"job_id": None}
    
    resp = job.copy()
    resp.pop("preview_image", None)
    return {"job_id": job["id"], "job": resp}

@app.get("/api/v1/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    resp = job.copy()
    resp.pop("preview_image", None)
    return resp

@app.post("/api/v1/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job_manager.cancel_job(job_id)
    return {"status": "cancelling"}

from fastapi.responses import FileResponse
@app.get("/api/v1/jobs/{job_id}/download")
async def download_job(job_id: str):
    job = job_manager.get_job(job_id)
    if not job or not job.get("output_path"):
        raise HTTPException(status_code=404, detail="Job output not found")
        
    output_path = job["output_path"]
    if not os.path.exists(output_path):
        # Maybe it was partially rendered
        base, ext = os.path.splitext(output_path)
        percent = int(job.get("progress", 0))
        partial_path = f"{base}_{percent}%{ext}"
        if os.path.exists(partial_path):
            output_path = partial_path
        else:
            raise HTTPException(status_code=404, detail="File not ready")
            
    import mimetypes
    media_type, _ = mimetypes.guess_type(output_path)
    if not media_type:
        media_type = "application/octet-stream"
        
    return FileResponse(output_path, media_type=media_type, filename=os.path.basename(output_path))

class DeleteHistoryRequest(BaseModel):
    filenames: list[str] = []
    delete_all: bool = False

class DownloadHistoryRequest(BaseModel):
    filenames: list[str]

@app.get("/api/v1/history")
async def get_history(x_client_platform: str = Header("unknown"), skip: int = 0, limit: int = 50):
    _, outputs_dir = ensure_workspace(x_client_platform)
    files = []
    if os.path.exists(outputs_dir):
        for f in os.listdir(outputs_dir):
            path = os.path.join(outputs_dir, f)
            if os.path.isfile(path):
                import mimetypes
                mt, _ = mimetypes.guess_type(path)
                mtype = 'video' if mt and mt.startswith('video') else 'image'
                files.append({
                    "filename": f,
                    "url": f"/api/v1/history/{f}?platform={x_client_platform}",
                    "type": mtype,
                    "created_at": os.path.getmtime(path)
                })
        # Sort by newest first
        files.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {"history": files[skip:skip+limit], "total": len(files)}

@app.get("/api/v1/history/{filename}")
async def serve_history_file(filename: str, platform: str = "unknown"):
    _, outputs_dir = ensure_workspace(platform)
    file_path = os.path.join(outputs_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    import mimetypes
    media_type, _ = mimetypes.guess_type(file_path)
    return FileResponse(file_path, media_type=media_type or "application/octet-stream")

@app.delete("/api/v1/history")
async def delete_history(req: DeleteHistoryRequest, x_client_platform: str = Header("unknown")):
    _, outputs_dir = ensure_workspace(x_client_platform)
    deleted = 0
    
    if req.delete_all:
        if os.path.exists(outputs_dir):
            for f in os.listdir(outputs_dir):
                path = os.path.join(outputs_dir, f)
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                        deleted += 1
                    except:
                        pass
    else:
        for f in req.filenames:
            # Prevent directory traversal
            safe_f = os.path.basename(f)
            path = os.path.join(outputs_dir, safe_f)
            if os.path.exists(path):
                try:
                    os.remove(path)
                    deleted += 1
                except:
                    pass
    return {"deleted": deleted}

import zipfile
import asyncio
from fastapi import BackgroundTasks

def create_zip_sync(zip_path, filenames, outputs_dir):
    found = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in filenames:
            safe_f = os.path.basename(f)
            path = os.path.join(outputs_dir, safe_f)
            if os.path.exists(path):
                zf.write(path, safe_f)
                found += 1
    return found

def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except:
        pass

@app.post("/api/v1/history/download")
async def download_history_bulk(req: DownloadHistoryRequest, background_tasks: BackgroundTasks, x_client_platform: str = Header("unknown")):
    _, outputs_dir = ensure_workspace(x_client_platform)
    
    # If only 1 file, return it directly
    if len(req.filenames) == 1:
        safe_f = os.path.basename(req.filenames[0])
        path = os.path.join(outputs_dir, safe_f)
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(path, filename=safe_f)
        
    # Multiple files -> zip
    downloads_dir = os.path.join(get_platform_dir(x_client_platform), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    zip_filename = f"uni_face_export_{uuid.uuid4().hex[:8]}.zip"
    zip_path = os.path.join(downloads_dir, zip_filename)
    
    # Run ZIP creation in a separate thread so it doesn't block the FastAPI event loop
    found = await asyncio.to_thread(create_zip_sync, zip_path, req.filenames, outputs_dir)
                
    if found == 0:
        cleanup_file(zip_path)
        raise HTTPException(status_code=404, detail="No files found")
        
    # Add cleanup to background tasks to run AFTER the user finishes downloading
    background_tasks.add_task(cleanup_file, zip_path)
    
    return FileResponse(zip_path, media_type="application/zip", filename="uni-face-export.zip")


# WebSocket for live progress and preview
@app.websocket("/api/v1/ws/jobs/{job_id}")
async def websocket_job_status(websocket: WebSocket, job_id: str):
    await websocket.accept()
    job_manager.active_websockets[job_id] = websocket
    # Track the MD5 of the last preview we sent so we can skip unchanged frames.
    # This avoids re-transmitting the same base64 JPEG on every 0.5-second tick.
    last_preview_hash: str = ""
    
    try:
        while True:
            job = job_manager.get_job(job_id)
            if not job:
                await websocket.send_json({"error": "Job not found"})
                break
            
            # Build the payload, conditionally including preview_image
            resp = {k: v for k, v in job.items() if k != "preview_image"}
            preview = job.get("preview_image")
            if preview:
                # BUG FIX: preview[:128] was always the same for every frame because all
                # JPEG files start with an identical SOI+APP0 header (~200 bytes of binary
                # = ~270 base64 chars), making the dedup hash useless.
                # Instead, sample from the middle of the image data + the tail.
                mid = len(preview) // 2
                preview_hash = hashlib.md5(
                    (preview[mid : mid + 256] + preview[-128:]).encode()
                ).hexdigest()
                if preview_hash != last_preview_hash:
                    resp["preview_image"] = preview
                    last_preview_hash = preview_hash
                # else: preview unchanged — omit it from this tick to save bandwidth
                
            await websocket.send_json(resp)
            
            if job["status"] in ["completed", "failed"]:
                break
                
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        # User disconnected, but we let the job continue in the background
        print(f"Client disconnected. Job {job_id} will continue in background.")
    except Exception as e:
        print(f"WebSocket error for job {job_id}: {e}")
    finally:
        if job_id in job_manager.active_websockets:
            del job_manager.active_websockets[job_id]

# Serve WebUI compiled dist
# api_server.py is in uniface/ so we go up one directory to reach the root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
webui_dist = os.path.join(ROOT_DIR, "webui", "dist")
if os.path.exists(webui_dist):
    app.mount("/", StaticFiles(directory=webui_dist, html=True), name="webui")
else:
    static_dir = os.path.join(ROOT_DIR, "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    @app.get("/")
    async def root():
        return RedirectResponse(url="/static/index.html")


if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
