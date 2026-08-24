import os
import sys
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

# --- Disable BLAS/OMP threading to prevent CPU thrashing during multi-thread processing ---
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

# Ensure we can import core modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.state import state
from core.video_service import process_video
from core.service import process_image

app = FastAPI(title="Uni-Face API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace with actual host/port if not localhost:8000
API_BASE_URL = "http://localhost:8000"



# --- WORKSPACE MANAGER ---
WORKSPACE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")

def get_platform_dir(platform: str) -> str:
    if not platform: platform = "unknown"
    platform = platform.lower().replace(r'[^a-z0-9]', '_')
    return os.path.join(WORKSPACE_DIR, platform)

def ensure_workspace(platform: str):
    p_dir = get_platform_dir(platform)
    uploads_dir = os.path.join(p_dir, "uploads")
    source_dir = os.path.join(uploads_dir, "source")
    target_dir = os.path.join(uploads_dir, "target")
    outputs_dir = os.path.join(p_dir, "outputs")
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    return uploads_dir, outputs_dir

# --- JOB MANAGER ---
class JobManager:
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.cancel_events: Dict[str, threading.Event] = {}
        self.active_websockets: Dict[str, WebSocket] = {}
        self.job_queue = queue.Queue()
        self.jobs_file = os.path.join(WORKSPACE_DIR, "jobs.json")
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
                
    def save_jobs(self):
        try:
            with open(self.jobs_file, "w", encoding="utf-8") as f:
                json.dump(self.jobs, f, indent=4)
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
        self.save_jobs()
        return job_id

    def update_job(self, job_id: str, updates: Dict[str, Any]):
        if job_id in self.jobs:
            self.jobs[job_id].update(updates)
            self.save_jobs()
            
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
    processors: list[str] = ["swap", "restore"]
    swap_model: str = "inswapper_128"
    swap_weight: float = 0.65
    swap_boost: int = 128
    restore_model: str = "gfpgan_1.4"
    restore_weight: float = 1.0
    restore_blend: int = 100
    mask_types: list[str] = ["box"]
    mask_regions: list[str] = ['skin', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 'nose', 'mouth', 'u_lip', 'l_lip']
    similarity: bool = False
    providers: list[str] = ["cpu"]
    skip_existing: bool = True

def run_job_background(job_id: str, req: JobStartRequest, x_client_platform: str):
    uploads_dir, outputs_dir = ensure_workspace(x_client_platform)
    source_path = os.path.join(uploads_dir, req.source_file_id)
    cancel_event = job_manager.cancel_events[job_id]
    
    state.init(parse_args=False)
    state.processors = req.processors
    state.swap_model = req.swap_model
    state.swap_weight = req.swap_weight
    state.swap_boost = req.swap_boost
    state.restore_model = req.restore_model
    state.restore_weight = req.restore_weight
    state.restore_blend = req.restore_blend
    state.mask_types = req.mask_types
    state.mask_regions = req.mask_regions
    state.similarity = req.similarity
    if hasattr(state, "_parse_providers"):
        state._parse_providers(" ".join(req.providers))
    state.source_path = source_path
    
    
    try:
        if req.source_type == "model":
            # Load the face model
            from core.face_model import load_face_model
            source_face = load_face_model(req.source_file_id, get_platform_dir(x_client_platform))
        else:
            from modules.detector import detect
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
        
        for idx, target_id in enumerate(req.target_file_ids):
            print(f"Processing target {idx + 1}/{total_targets}: {target_id}")
            if cancel_event.is_set():
                break
                
            target_path = os.path.join(uploads_dir, target_id)
            target_basename = os.path.basename(target_id)
            source_basename = os.path.basename(req.source_file_id)
            import mimetypes
            mime_type, _ = mimetypes.guess_type(target_path)
            is_image = mime_type and mime_type.startswith('image')
            
            target_name, _ = os.path.splitext(target_basename)
            source_name, _ = os.path.splitext(source_basename)
            
            # Shorten the names a bit to avoid extremely long paths
            out_name = f"out_{source_name[:8]}_{target_name[:8]}"
            if not req.skip_existing:
                out_name += f"_{uuid.uuid4().hex[:6]}"
                
            if is_image:
                ext = os.path.splitext(target_path)[1] or '.jpg'
                out_name += ext
            else:
                if not out_name.endswith('.mp4'):
                    out_name += ".mp4"
                    
            output_path = os.path.join(outputs_dir, out_name)
            last_output_path = output_path
            
            job_manager.update_job(job_id, {"status": "processing", "output_path": output_path})
            
            # Callback for progress and preview
            def progress_callback(current: int, total: int, frame: np.ndarray = None):
                file_pct = (current / total) * 100 if total > 0 else 0
                overall_pct = (idx / total_targets * 100) + (file_pct / total_targets)
                
                updates = {
                    "progress": round(overall_pct, 2),
                    "frames_done": current,
                    "total_frames": total
                }
                
                freq = max(1, req.preview_frequency)
                if frame is not None and (current == 1 or current % freq == 0 or current == total):
                    h, w = frame.shape[:2]
                    scale = 320 / max(h, w)
                    preview_frame = cv2.resize(frame, (int(w*scale), int(h*scale)))
                    _, buffer = cv2.imencode('.jpg', preview_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                    b64 = base64.b64encode(buffer).decode('utf-8')
                    updates["preview_image"] = f"data:image/jpeg;base64,{b64}"
                    
                job_manager.update_job(job_id, updates)
                
            if is_image:
                target_img = cv2.imread(target_path)
                if target_img is not None:
                    processed_img = process_image(source_face, target_img, verbose=False)
                    cv2.imwrite(output_path, processed_img)
                    progress_callback(1, 1, processed_img)
            else:
                process_video(source_face, target_path, output_path, progress_callback=progress_callback, cancel_event=cancel_event, skip_existing=req.skip_existing)
                
        if not cancel_event.is_set():
            job_manager.update_job(job_id, {"status": "completed", "progress": 100.0, "output_path": last_output_path})
            
        # Cleanup targets
        for target_id in set(req.target_file_ids):
            target_path = os.path.join(uploads_dir, target_id)
            try:
                os.remove(target_path)
            except:
                pass
        
        # Cleanup source if it's an uploaded image
        if req.source_type == "image":
            try:
                os.remove(source_path)
            except:
                pass
            
    except Exception as e:
        job_manager.update_job(job_id, {"status": "failed", "error": str(e)})

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
    from core.face_model import save_face_model
    from modules.detector import detect
    
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
    
    # Enqueue job instead of starting a new thread immediately
    job_manager.job_queue.put((job_id, req, x_client_platform))
    
    return {"job_id": job_id, "status": "pending"}

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
@app.post("/api/v1/history/download")
async def download_history_bulk(req: DownloadHistoryRequest, x_client_platform: str = Header("unknown")):
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
    
    found = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in req.filenames:
            safe_f = os.path.basename(f)
            path = os.path.join(outputs_dir, safe_f)
            if os.path.exists(path):
                zf.write(path, safe_f)
                found += 1
                
    if found == 0:
        raise HTTPException(status_code=404, detail="No files found")
        
    return FileResponse(zip_path, media_type="application/zip", filename="uni-face-export.zip")

# WebSocket for live progress and preview
@app.websocket("/api/v1/ws/jobs/{job_id}")
async def websocket_job_status(websocket: WebSocket, job_id: str):
    await websocket.accept()
    job_manager.active_websockets[job_id] = websocket
    
    try:
        while True:
            job = job_manager.get_job(job_id)
            if not job:
                await websocket.send_json({"error": "Job not found"})
                break
                
            await websocket.send_json(job)
            
            if job["status"] in ["completed", "failed"]:
                break
                
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        # User disconnected, but we let the job continue in the background
        print(f"Client disconnected. Job {job_id} will continue in background.")
    finally:
        if job_id in job_manager.active_websockets:
            del job_manager.active_websockets[job_id]

# Serve WebUI compiled dist
webui_dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webui", "dist")
if os.path.exists(webui_dist):
    app.mount("/", StaticFiles(directory=webui_dist, html=True), name="webui")
else:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    @app.get("/")
    async def root():
        return RedirectResponse(url="/static/index.html")


if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
