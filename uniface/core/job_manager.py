import os
import time
import uuid
import json
import queue
import base64
import cv2
import threading
import numpy as np
from typing import Dict, Any, Optional
from pydantic import BaseModel
from uniface.core.types import Face, JobConfig

from uniface.core.workspace import WORKSPACE_DIR, ensure_workspace, get_platform_dir, get_target_sets_dir
from uniface.core.state import state
from uniface.core.video_service import process_video
from uniface.core.image_service import process_images_swarm
from uniface.core.logging import get_logger

logger = get_logger(__name__)

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
    occlusion_model: str = "xseg_1"
    target_gender: str = "all"
    face_order: str = "largest"
    similarity: bool = False
    providers: list[str] = ["cpu"]
    execution_thread_count: int = 4
    skip_existing: bool = True
    reference_face_ids: list[str] = []
    reference_threshold: float = 0.6
    
    immich_url: str = ""
    immich_api_key: str = ""
    immich_auto_save: bool = False
    immich_new_album: bool = False
    immich_album: str = ""
    immich_tags: list[str] = []
    immich_delete_local: bool = False

class PreviewSettings(BaseModel):
    enabled: bool
    resolution: int

class JobManager:
    # Status changes that must be saved immediately (not debounced)
    _IMMEDIATE_SAVE_KEYS = {"status", "error", "output_path"}
    # Minimum seconds between debounced (progress) saves
    _SAVE_DEBOUNCE_SECS = 5.0

    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.cancel_events: Dict[str, threading.Event] = {}
        self.active_websockets: Dict[str, Any] = {}
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

def run_job_background(job_id: str, req: JobStartRequest, x_client_platform: str):
    uploads_dir, outputs_dir = ensure_workspace(x_client_platform)
    source_path = os.path.join(uploads_dir, req.source_file_id)
    cancel_event = job_manager.cancel_events[job_id]
    
    parsed_providers = None
    if req.providers:
        if hasattr(state, "parse_providers"):
            parsed_providers = state.parse_providers(" ".join(req.providers))
        elif hasattr(state, "_parse_providers"):
            parsed_providers = state._parse_providers(" ".join(req.providers))
            if parsed_providers is None:
                parsed_providers = state.providers
    if not parsed_providers or not isinstance(parsed_providers, list):
        parsed_providers = state.providers or ["CPUExecutionProvider"]
    # Filter out any None elements if present
    parsed_providers = [p for p in parsed_providers if p is not None]
    if not parsed_providers:
        parsed_providers = ["CPUExecutionProvider"]
        
    job_config = JobConfig(
        processors=list(req.processors),
        swap_model=req.swap_model,
        swap_weight=req.swap_weight,
        restore_model=req.restore_model,
        restore_weight=req.restore_weight,
        restore_blend=req.restore_blend,
        mask_types=list(req.mask_types),
        mask_regions=list(req.mask_regions),
        occlusion_model=req.occlusion_model,
        target_gender=getattr(req, "target_gender", "all"),
        face_order=getattr(req, "face_order", "largest"),
        similarity=req.similarity,
        providers=parsed_providers,
        execution_thread_count=req.execution_thread_count,
        video_encoder=getattr(state, "video_encoder", "h264_nvenc"),
        reference_face_ids=list(req.reference_face_ids),
        reference_threshold=req.reference_threshold
    )
    
    logger.debug(f"Job {job_id} reference_face_ids: {len(job_config.reference_face_ids)}")
    logger.debug(f"Job {job_id} reference_threshold: {job_config.reference_threshold}")
    
    job_completed_successfully = False
    try:
        if req.source_type == "model":
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
        logger.info(f"Starting job {job_id} with {total_targets} target files: {req.target_file_ids}")
        
        image_in_paths = []
        image_out_paths = []
        video_tasks = []
        generated_filenames = []
        last_output_path = ""
        
        import mimetypes
        
        for target_id in req.target_file_ids:
            if target_id.startswith("set:"):
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
            
            generated_filenames.append(out_name)
            last_output_path = out_path
            
        job_manager.update_job(job_id, {"status": "processing"})
        processed_total = 0
        
        # 1. Process images via SwarmEngine
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
                
                current_job = job_manager.get_job(job_id) or {}
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
                
            process_images_swarm(
                source_face, 
                image_in_paths, 
                image_out_paths, 
                progress_callback=img_progress, 
                cancel_event=cancel_event,
                job_config=job_config
            )
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
                
                current_job = job_manager.get_job(job_id) or {}
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
                
            process_video(
                source_face, 
                v_in, 
                v_out, 
                progress_callback=vid_progress, 
                cancel_event=cancel_event, 
                skip_existing=req.skip_existing,
                job_config=job_config
            )
            processed_total += 1
                
        if not cancel_event.is_set():
            job_manager.update_job(job_id, {"status": "completed", "progress": 100.0, "output_path": last_output_path})
            job_completed_successfully = True
            
            # Immich Auto-Save Hook
            if req.immich_auto_save and req.immich_url and req.immich_api_key:
                try:
                    job_manager.update_job(job_id, {"status": "uploading", "progress": 100.0, "message": "Syncing to Immich..."})
                    from uniface.core.immich_sync import sync_to_immich
                    result = sync_to_immich(
                        url=req.immich_url,
                        api_key=req.immich_api_key,
                        filenames=generated_filenames,
                        is_new_album=req.immich_new_album,
                        album_name=req.immich_album,
                        tags=req.immich_tags,
                        outputs_dir=outputs_dir
                    )
                    
                    if result.get("success"):
                        if req.immich_delete_local:
                            for fname in generated_filenames:
                                fpath = os.path.join(outputs_dir, fname)
                                try:
                                    if os.path.exists(fpath):
                                        os.remove(fpath)
                                except Exception as e:
                                    logger.warning(f"Failed to delete local file {fpath}: {e}")
                            
                            job_manager.update_job(job_id, {
                                "output_path": None, 
                                "status": "completed",
                                "immich_status": "success",
                                "immich_message": result.get("message")
                            })
                        else:
                            job_manager.update_job(job_id, {
                                "status": "completed",
                                "immich_status": "success",
                                "immich_message": result.get("message")
                            })
                    else:
                        logger.error(f"Immich sync failed: {result.get('message')}")
                        job_manager.update_job(job_id, {
                            "status": "completed",
                            "immich_status": "failed",
                            "immich_message": result.get("message")
                        })
                except Exception as sync_e:
                    logger.error(f"Immich sync error: {sync_e}", exc_info=True)
                    job_manager.update_job(job_id, {
                        "status": "completed",
                        "immich_status": "failed",
                        "immich_message": str(sync_e)
                    })
            
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}", exc_info=True)
        job_manager.update_job(job_id, {"status": "failed", "error": str(e)})

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
            logger.error(f"Worker loop error: {e}", exc_info=True)

# Start background worker thread
worker_thread = threading.Thread(target=worker_loop, daemon=True)
worker_thread.start()
