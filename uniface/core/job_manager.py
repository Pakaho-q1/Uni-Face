import os
import re
import time
import uuid
import json
import queue
import hashlib
import base64
import cv2
import threading
import numpy as np
from datetime import datetime
import mimetypes
from typing import Dict, Any, Optional
from pydantic import BaseModel
from uniface.core.types import Face, JobConfig

from uniface.core.workspace import (
    WORKSPACE_DIR, ensure_workspace, get_platform_dir, get_target_sets_dir,
    get_jobs_dir, get_job_workspace, ensure_job_workspace, safe_hardlink, cleanup_job_workspace
)
from uniface.core.state import state
from uniface.core.video_service import process_video
from uniface.core.image_service import process_images_swarm
from uniface.core.logging import get_logger
from uniface.core import db

logger = get_logger(__name__)

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif', '.jfif', '.avif'}

def is_image_path(path: str) -> bool:
    """Robust image check supporting modern formats (.webp, .jfif, .avif) on Windows."""
    ext = os.path.splitext(path)[1].lower()
    if ext in IMAGE_EXTENSIONS:
        return True
    mt, _ = mimetypes.guess_type(path)
    return bool(mt and mt.startswith('image'))

def generate_job_id() -> str:
    """Generate human-readable, sortable, OS-safe Job ID: YYMMDD_HHMMSS_<short_hex>"""
    now_str = datetime.now().strftime("%y%m%d_%H%M%S")
    short_id = uuid.uuid4().hex[:4]
    return f"{now_str}_{short_id}"

def create_b64_preview(frame: np.ndarray, resolution: int, quality: int = 50) -> str:
    """Encode an in-memory frame to a base64 JPEG thumbnail string."""
    h, w = frame.shape[:2]
    scale = resolution / max(h, w)
    if scale < 1.0:
        preview_frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
    else:
        preview_frame = frame
    _, buffer = cv2.imencode('.jpg', preview_frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"

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
    face_detector_score: float = 0.65
    face_landmark_score: float = 0.50
    
    # Dual-Stage Swap & Staged Restore
    stage1_restore: bool = False
    dual_swap: bool = False
    swap_model_2: str = "hyperswap_high_512"
    swap_weight_2: float = 0.80
    stage2_restore: bool = True
    restore_model_2: str = "gfpgan_1.4"
    restore_weight_2: float = 1.0
    restore_blend_2: int = 100
    
    # Clean Source Face & Mask Padding
    clean_source_face: bool = False
    mask_padding: list[int] = [0, 0, 0, 0]
    mask_blur: float = 0.3
    
    # ReActor Enhancements & Face Boost
    face_boost: str = "none"
    restore_source_face: bool = False
    restore_source_face_model: str = "gfpgan_1.4"
    restore_source_face_weight: float = 0.8
    target_hair_protect: bool = True
    
    immich_url: str = ""
    immich_api_key: str = ""
    immich_auto_save: bool = False
    immich_new_album: bool = False
    immich_album: str = ""
    immich_tags: list[str] = []
    immich_delete_local: bool = False

def setup_job_hardlinks(platform: str, job_id: str, req: JobStartRequest) -> dict:
    """Prepare ephemeral job sandbox and create zero-copy hardlinks for source and targets."""
    uploads_dir, _ = ensure_workspace(platform)
    ws = ensure_job_workspace(platform, job_id)
    
    # 1. Hardlink source file
    if req.source_file_id:
        if req.source_type == "model":
            src_orig = os.path.join(get_platform_dir(platform), req.source_file_id)
        else:
            src_orig = os.path.join(uploads_dir, req.source_file_id)
        if os.path.exists(src_orig):
            src_link = os.path.join(ws["source_dir"], os.path.basename(req.source_file_id))
            safe_hardlink(src_orig, src_link)
            
    # 2. Hardlink target files
    for target_id in req.target_file_ids:
        if target_id.startswith("set:"):
            target_rel = target_id[4:]
            target_orig = os.path.join(get_target_sets_dir(platform), target_rel)
        else:
            target_orig = os.path.join(uploads_dir, target_id)
            
        if os.path.exists(target_orig):
            tgt_link = os.path.join(ws["target_dir"], os.path.basename(target_orig))
            safe_hardlink(target_orig, tgt_link)
            
    return ws

class PreviewSettings(BaseModel):
    enabled: bool
    resolution: int

class JobManager:
    # Status changes that must be saved immediately (not debounced)
    _IMMEDIATE_SAVE_KEYS = {"status", "error", "output_path"}
    # Minimum seconds between debounced (progress) saves
    _SAVE_DEBOUNCE_SECS = 2.0

    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.cancel_events: Dict[str, threading.Event] = {}
        self.active_websockets: Dict[str, Any] = {}
        self.job_queue = queue.Queue()
        self.jobs_file = os.path.join(WORKSPACE_DIR, "jobs.json")
        self._save_lock = threading.Lock()
        self._last_save_time: float = 0.0
        self.init_storage()

    def init_storage(self):
        db.init_db()
        # 1. Migrate legacy jobs.json if exists
        if os.path.exists(self.jobs_file):
            try:
                with open(self.jobs_file, "r", encoding="utf-8") as f:
                    old_jobs = json.load(f)
                for j_id, j_data in old_jobs.items():
                    if not db.get_job_record(j_id):
                        st = j_data.get("status", "pending")
                        if st in ["pending", "processing"]:
                            st = "failed"
                        db.create_job_record(
                            job_id=j_id,
                            platform=j_data.get("platform", "unknown"),
                            status=st,
                            source_type=j_data.get("source_type", "image"),
                            source_file_id=j_data.get("source_file_id"),
                            source_name=j_data.get("source_name") or (os.path.basename(j_data.get("source_file_id")) if j_data.get("source_file_id") else None),
                            target_type=j_data.get("target_type", "upload"),
                            target_count=j_data.get("target_count", 0),
                            target_summary=j_data.get("target_summary")
                        )
                        db.update_job_record(j_id, {
                            "progress": j_data.get("progress", 0.0),
                            "frames_done": j_data.get("frames_done", 0),
                            "total_frames": j_data.get("total_frames", 0),
                            "output_path": j_data.get("output_path"),
                            "error": j_data.get("error")
                        })
            except Exception as e:
                logger.error(f"Error migrating jobs.json: {e}")

        # 2. Reset any jobs left in pending/processing state from previous crash/restart
        try:
            with db._db_lock:
                conn = db._get_connection()
                conn.execute("UPDATE jobs SET status = 'failed', error = 'Server restarted during processing' WHERE status IN ('pending', 'processing')")
                conn.commit()
                conn.close()
        except Exception as e:
            logger.error(f"Error resetting active jobs in db: {e}")

    def save_jobs(self, force: bool = False):
        """Write jobs to disk (debounced) for file compatibility."""
        if not hasattr(self, "_last_save_time"):
            self._last_save_time = 0.0
        if not hasattr(self, "_save_lock"):
            self._save_lock = threading.Lock()
            
        now = time.monotonic()
        if not force and (now - self._last_save_time) < self._SAVE_DEBOUNCE_SECS:
            return
        with self._save_lock:
            try:
                if hasattr(self, "jobs_file") and self.jobs_file:
                    with open(self.jobs_file, "w", encoding="utf-8") as f:
                        json.dump(self.jobs, f, indent=4)
                self._last_save_time = time.monotonic()
            except Exception as e:
                logger.debug(f"Error saving jobs to file: {e}")

    def create_job(self, platform: str, req: Optional[JobStartRequest] = None) -> str:
        job_id = generate_job_id()
        ensure_job_workspace(platform, job_id)
        
        source_type = req.source_type if req else "image"
        source_file_id = req.source_file_id if req else None
        source_name = None
        if source_file_id:
            source_name = os.path.basename(source_file_id)
        
        target_type = "upload"
        target_count = len(req.target_file_ids) if req else 0
        target_summary = None
        if req and req.target_file_ids:
            first_target = os.path.basename(req.target_file_ids[0])
            if target_count > 1:
                target_summary = f"{first_target} +{target_count - 1} more"
            else:
                target_summary = first_target
                
        config_json = req.model_dump_json() if req else None
        
        record = db.create_job_record(
            job_id=job_id,
            platform=platform,
            status="pending",
            source_type=source_type,
            source_file_id=source_file_id,
            source_name=source_name,
            target_type=target_type,
            target_count=target_count,
            target_summary=target_summary,
            config_json=config_json
        )
        
        self.jobs[job_id] = {
            "id": job_id,
            "platform": platform,
            "status": "pending",
            "source_type": source_type,
            "source_file_id": source_file_id,
            "source_name": source_name,
            "target_type": target_type,
            "target_count": target_count,
            "target_summary": target_summary,
            "progress": 0.0,
            "frames_done": 0,
            "total_frames": 0,
            "preview_image": None,
            "output_path": None,
            "error": None,
            "created_at": record.get("created_at")
        }
        self.cancel_events[job_id] = threading.Event()
        self.save_jobs(force=True)
        return job_id

    def update_job(self, job_id: str, updates: Dict[str, Any], force: bool = False):
        if not hasattr(self, "_last_save_time"):
            self._last_save_time = 0.0
        if not hasattr(self, "_save_lock"):
            self._save_lock = threading.Lock()
            
        if job_id not in self.jobs:
            job_rec = db.get_job_record(job_id)
            if job_rec:
                self.jobs[job_id] = dict(job_rec)
                self.jobs[job_id]["preview_image"] = None
            else:
                self.jobs[job_id] = {"id": job_id}
                
        self.jobs[job_id].update(updates)
        
        # Prepare DB updates (exclude preview_image to keep SQLite fast and lightweight)
        db_updates = {k: v for k, v in updates.items() if k != "preview_image"}
        should_force = force or bool(self._IMMEDIATE_SAVE_KEYS & updates.keys())
        now = time.monotonic()
        
        if db_updates and (should_force or (now - self._last_save_time) >= self._SAVE_DEBOUNCE_SECS):
            try:
                db.update_job_record(job_id, db_updates)
                self._last_save_time = now
            except Exception as e:
                logger.debug(f"DB update error: {e}")
                
        self.save_jobs(force=should_force)

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        in_mem = self.jobs.get(job_id)
        if in_mem and in_mem.get("status"):
            return in_mem
        record = db.get_job_record(job_id)
        if record:
            self.jobs[job_id] = dict(record)
            if in_mem and "preview_image" in in_mem:
                self.jobs[job_id]["preview_image"] = in_mem["preview_image"]
            return self.jobs[job_id]
        return None

    def cancel_job(self, job_id: str):
        if job_id in self.cancel_events:
            self.cancel_events[job_id].set()
            
        job = db.get_job_record(job_id)
        frames_done = 0
        total_frames = 0
        progress = 0.0
        
        if job:
            platform = job.get("platform", "unknown")
            ws = get_job_workspace(platform, job_id)
            out_dir = ws["output_dir"]
            if os.path.exists(out_dir):
                actual_files = [f for f in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, f)) and os.path.getsize(os.path.join(out_dir, f)) > 0]
                frames_done = len(actual_files)
                
            total_frames = job.get("total_frames") or job.get("target_count") or 0
            if total_frames > 0:
                progress = round((frames_done / total_frames) * 100, 2)
                
        updates = {
            "status": "failed",
            "error": "Cancelled by user",
            "frames_done": frames_done,
            "total_frames": total_frames,
            "progress": progress
        }
        self.update_job(job_id, updates, force=True)

    def clean_job_temp_dir(self, job: Dict[str, Any]):
        """Remove temp session folders and partial video files for a given job."""
        try:
            import shutil
            platform = job.get("platform", "unknown")
            job_id = job.get("id")
            if job_id:
                ws = get_job_workspace(platform, job_id)
                if os.path.exists(ws["temp_dir"]):
                    shutil.rmtree(ws["temp_dir"], ignore_errors=True)
            _, outputs_dir = ensure_workspace(platform)
            temp_root = os.path.join(outputs_dir, "temp")
            
            prefixes_to_clean = set()
            if job.get("config_json"):
                try:
                    req = JobStartRequest.model_validate_json(job["config_json"])
                    source_base = os.path.splitext(os.path.basename(req.source_file_id))[0] if req.source_file_id else ""
                    for tid in req.target_file_ids:
                        t_base = os.path.splitext(os.path.basename(tid))[0]
                        prefix = f"out_{source_base[:8]}_{t_base[:8]}"
                        prefixes_to_clean.add(prefix)
                except Exception as e:
                    logger.debug(f"Could not parse config_json for temp cleanup: {e}")

            if job.get("output_path"):
                out_base = os.path.splitext(os.path.basename(job["output_path"]))[0]
                prefixes_to_clean.add(out_base)

            if not prefixes_to_clean:
                return

            if os.path.exists(temp_root):
                for folder_name in os.listdir(temp_root):
                    folder_path = os.path.join(temp_root, folder_name)
                    if os.path.isdir(folder_path):
                        for pfx in prefixes_to_clean:
                            if folder_name == pfx or folder_name.startswith(pfx):
                                logger.info(f"Cleaning temp folder on job delete: {folder_path}")
                                shutil.rmtree(folder_path, ignore_errors=True)
                                break

            # Also clean any partial interrupted video files in outputs_dir
            if os.path.exists(outputs_dir):
                for fname in os.listdir(outputs_dir):
                    for pfx in prefixes_to_clean:
                        if fname.startswith(f"{pfx}_") and "%" in fname and fname.endswith(".mp4"):
                            try:
                                os.remove(os.path.join(outputs_dir, fname))
                            except Exception:
                                pass
        except Exception as e:
            logger.error(f"Error cleaning temp files: {e}")

    def delete_job(self, job_id: str) -> bool:
        job = db.get_job_record(job_id) or self.jobs.get(job_id)
        if job_id in self.cancel_events:
            self.cancel_events[job_id].set()
            del self.cancel_events[job_id]
        if job_id in self.jobs:
            del self.jobs[job_id]
        if job:
            platform = job.get("platform", "unknown")
            cleanup_job_workspace(platform, job_id, delete_output=True)
            self.clean_job_temp_dir(job)
        return db.delete_job_record(job_id)

    def retry_job(self, job_id: str) -> bool:
        """Retry a failed or cancelled job in-place using the same job_id."""
        logger.info(f"[RETRY] Processing in-place retry request for Job: {job_id}")
        job = db.get_job_record(job_id)
        if not job or not job.get("config_json"):
            logger.warning(f"[RETRY] Cannot retry job {job_id}: record or config_json not found")
            return False
            
        try:
            req = JobStartRequest.model_validate_json(job["config_json"])
            platform = job.get("platform", "unknown")
            
            # Always ensure skip_existing is True on retry to resume from checkpoints
            req.skip_existing = True
            logger.info(f"[RETRY] Loaded job config for {job_id}: {len(req.target_file_ids)} target(s), platform={platform}")
            
            # Reset cancel event
            self.cancel_events[job_id] = threading.Event()
            
            # Count actual existing output files on disk to reflect real state immediately
            ws = get_job_workspace(platform, job_id)
            out_dir = ws["output_dir"]
            actual_done = 0
            if os.path.exists(out_dir):
                actual_done = len([f for f in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, f)) and os.path.getsize(os.path.join(out_dir, f)) > 0])
                
            total_targets = len(req.target_file_ids)
            cur_progress = round((actual_done / total_targets) * 100, 2) if total_targets > 0 else 0.0
            
            # In-place update to pending, clearing error
            updates = {
                "status": "pending",
                "error": None,
                "preview_image": None,
                "frames_done": actual_done,
                "total_frames": total_targets,
                "progress": cur_progress
            }
            self.update_job(job_id, updates, force=True)
            logger.info(f"[RETRY] Job {job_id} status reset to 'pending' ({actual_done}/{total_targets} files verified on disk)")
            
            # Re-enqueue the existing job_id
            self.job_queue.put((job_id, req, platform))
            logger.info(f"[RETRY] Job {job_id} successfully re-enqueued for worker thread")
            return True
        except Exception as e:
            logger.error(f"[RETRY] Failed to retry job {job_id}: {e}", exc_info=True)
            return False

    def rerun_job(self, job_id: str) -> Optional[str]:
        job = db.get_job_record(job_id)
        if not job or not job.get("config_json"):
            return None
        try:
            req = JobStartRequest.model_validate_json(job["config_json"])
            new_job_id = self.create_job(job.get("platform", "unknown"), req)
            self.job_queue.put((new_job_id, req, job.get("platform", "unknown")))
            return new_job_id
        except Exception as e:
            logger.error(f"Failed to rerun job {job_id}: {e}")
            return None

    def get_active_job_for_platform(self, platform: str) -> Optional[Dict[str, Any]]:
        # Check in-memory first
        for job_id, job in reversed(list(self.jobs.items())):
            if job.get("platform") == platform and job.get("status") in ["pending", "processing"]:
                return job
        # Check DB
        active_list = db.list_job_records(platform=platform, status="active", limit=1)
        if active_list:
            return active_list[0]
        return None

job_manager = JobManager()

def run_job_background(job_id: str, req: JobStartRequest, x_client_platform: str):
    uploads_dir, root_outputs_dir = ensure_workspace(x_client_platform)
    ws = ensure_job_workspace(x_client_platform, job_id)
    setup_job_hardlinks(x_client_platform, job_id, req)
    
    source_dir = ws["source_dir"]
    target_dir = ws["target_dir"]
    job_temp_dir = ws["temp_dir"]
    job_output_dir = ws["output_dir"]
    
    # Resolve source path (prefer job sandbox, fallback to uploads)
    source_path = None
    if req.source_file_id:
        if req.source_type == "model":
            source_path = os.path.join(get_platform_dir(x_client_platform), req.source_file_id)
        else:
            cand = os.path.join(source_dir, os.path.basename(req.source_file_id))
            source_path = cand if os.path.exists(cand) else os.path.join(uploads_dir, req.source_file_id)
            
    cancel_event = job_manager.cancel_events.setdefault(job_id, threading.Event())
    
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
        reference_threshold=req.reference_threshold,
        face_detector_score=getattr(req, "face_detector_score", 0.65),
        face_landmark_score=getattr(req, "face_landmark_score", 0.50),
        stage1_restore=getattr(req, "stage1_restore", False),
        dual_swap=getattr(req, "dual_swap", False),
        swap_model_2=getattr(req, "swap_model_2", "hyperswap_high_512"),
        swap_weight_2=getattr(req, "swap_weight_2", 0.80),
        stage2_restore=getattr(req, "stage2_restore", True),
        restore_model_2=getattr(req, "restore_model_2", "gfpgan_1.4"),
        restore_weight_2=getattr(req, "restore_weight_2", 1.0),
        restore_blend_2=getattr(req, "restore_blend_2", 100),
        clean_source_face=getattr(req, "clean_source_face", False),
        mask_padding=list(getattr(req, "mask_padding", [0, 0, 0, 0])),
        mask_blur=float(getattr(req, "mask_blur", 0.3)),
        face_boost=str(getattr(req, "face_boost", "none")),
        restore_source_face=bool(getattr(req, "restore_source_face", False)),
        restore_source_face_model=str(getattr(req, "restore_source_face_model", "gfpgan_1.4")),
        restore_source_face_weight=float(getattr(req, "restore_source_face_weight", 0.8)),
        target_hair_protect=bool(getattr(req, "target_hair_protect", True))
    )
    
    logger.debug(f"Job {job_id} reference_face_ids: {len(job_config.reference_face_ids)}")
    logger.debug(f"Job {job_id} reference_threshold: {job_config.reference_threshold}")
    logger.debug(f"Job {job_id} face_detector_score: {job_config.face_detector_score}, landmark_score: {job_config.face_landmark_score}")
    logger.debug(f"Job {job_id} dual_swap: {job_config.dual_swap}, stage1_restore: {job_config.stage1_restore}, stage2_restore: {job_config.stage2_restore}")
    
    # Unload any models that are NOT needed for this specific job to free VRAM
    from uniface.core.model_manager import optimize_models_for_job
    optimize_models_for_job(job_config)
    
    job_completed_successfully = False
    try:
        if req.source_type == "model":
            from uniface.core.face_model import load_face_model
            source_face = load_face_model(req.source_file_id, get_platform_dir(x_client_platform))
            if not source_face or "embeddings" not in source_face or len(source_face["embeddings"]) == 0:
                raise ValueError(f"Face model '{req.source_file_id}' contains no valid embeddings.")
        else:
            from uniface.core.service import resolve_source_face
            source_img = cv2.imread(source_path)
            if source_img is None:
                raise Exception("Could not read source image")
                
            source_face = resolve_source_face(source_img, job_config=job_config)
            if source_face is None:
                raise Exception("No face detected in source image")
        
        total_targets = len(req.target_file_ids)
        logger.info(f"Starting job {job_id} with {total_targets} target files: {req.target_file_ids}")
        
        image_in_paths = []
        image_out_paths = []
        video_tasks = []
        generated_filenames = []
        last_output_path = ""
        
        for target_id in req.target_file_ids:
            if target_id.startswith("set:"):
                target_rel_path = target_id[4:]
                cand = os.path.join(target_dir, os.path.basename(target_rel_path))
                target_path = cand if os.path.exists(cand) else os.path.join(get_target_sets_dir(x_client_platform), target_rel_path)
            else:
                cand = os.path.join(target_dir, os.path.basename(target_id))
                target_path = cand if os.path.exists(cand) else os.path.join(uploads_dir, target_id)
                
            target_basename = os.path.basename(target_path)
            source_basename = os.path.basename(req.source_file_id) if req.source_file_id else "source"
            is_image = is_image_path(target_path)
            target_name, target_ext = os.path.splitext(target_basename)
            source_name, _ = os.path.splitext(source_basename)

            clean_source = re.sub(r'[^a-zA-Z0-9_\-]', '_', source_name)
            clean_target = re.sub(r'[^a-zA-Z0-9_\-]', '_', target_name)
            target_hash = hashlib.md5(target_id.encode('utf-8')).hexdigest()[:6]
            
            # Deterministic, unique output name per target inside outputs/<job_id>
            out_name = f"out_{clean_source[:12]}_{clean_target[:24]}_{target_hash}"
                
            if is_image:
                ext = target_ext or '.jpg'
                out_name += ext
                out_path = os.path.join(job_output_dir, out_name)
                image_in_paths.append(target_path)
                image_out_paths.append(out_path)
            else:
                if not out_name.endswith('.mp4'):
                    out_name += ".mp4"
                out_path = os.path.join(job_output_dir, out_name)
                video_tasks.append((target_path, out_path))
            
            generated_filenames.append(out_name)
            last_output_path = out_path
            
        job_manager.update_job(job_id, {"status": "processing"})
        logger.info(f"[JOB {job_id}] Processing started. Total targets to evaluate: {total_targets}")
        processed_total = 0
        
        # 1. Process images via SwarmEngine
        if image_in_paths:
            pending_in = []
            pending_out = []
            existing_out_files = set(os.listdir(job_output_dir)) if os.path.exists(job_output_dir) else set()
            
            for inp, outp in zip(image_in_paths, image_out_paths):
                # Rule 3: Target is ONLY complete if its exact output file exists on disk and has size > 0
                if req.skip_existing and os.path.exists(outp) and os.path.getsize(outp) > 0:
                    logger.info(f"[CHECKPOINT] Output exists on disk -> Skipping: {os.path.basename(outp)}")
                    processed_total += 1
                else:
                    pending_in.append(inp)
                    pending_out.append(outp)

            logger.info(f"[JOB {job_id}] Target check: {processed_total}/{len(image_in_paths)} already completed on disk, {len(pending_in)} pending to process")
            
            # Immediately update job with verified disk checkpoint
            init_pct = round((processed_total / total_targets) * 100, 2) if total_targets > 0 else 0.0
            job_manager.update_job(job_id, {
                "frames_done": processed_total,
                "total_frames": total_targets,
                "progress": init_pct
            }, force=True)

            if pending_in:
                from uniface.core.image_service import process_images_swarm
                def img_progress(current: int, total: int, frame: np.ndarray = None):
                    nonlocal processed_total
                    current_done = processed_total + current
                    overall_pct = ((current_done / total_targets) * 100) if total_targets > 0 else 100.0
                    
                    updates = {
                        "progress": round(overall_pct, 2),
                        "frames_done": current_done,
                        "total_frames": total_targets
                    }
                    if current <= len(pending_out):
                        updates["output_path"] = pending_out[current - 1]
                    
                    current_job = job_manager.get_job(job_id) or {}
                    preview_enabled = current_job.get("preview_enabled", req.preview_enabled)
                    preview_res = current_job.get("preview_resolution", req.preview_resolution)
                    
                    freq = max(1, req.preview_frequency)
                    if preview_enabled and frame is not None and (current == 1 or current % freq == 0 or current == total):
                        updates["preview_image"] = create_b64_preview(frame, preview_res)
                    job_manager.update_job(job_id, updates, force=True)
                    
                process_images_swarm(
                    source_face, 
                    pending_in, 
                    pending_out, 
                    progress_callback=img_progress, 
                    cancel_event=cancel_event,
                    job_config=job_config
                )
                if not cancel_event.is_set():
                    processed_total += len(pending_in)
            else:
                initial_pct = (processed_total / total_targets * 100) if total_targets > 0 else 100.0
                job_manager.update_job(job_id, {
                    "progress": round(initial_pct, 2),
                    "frames_done": processed_total,
                    "total_frames": total_targets
                })

        # 2. Process videos sequentially
        for v_in, v_out in video_tasks:
            if cancel_event.is_set():
                break
                
            v_basename = os.path.splitext(os.path.basename(v_out))[0]
            session_temp_dir = os.path.join(os.path.dirname(v_out), "temp", v_basename)
            
            # Skip if video output already exists, is non-empty, and temp dir was already removed (fully completed)
            if req.skip_existing and os.path.exists(v_out) and os.path.getsize(v_out) > 0 and not os.path.exists(session_temp_dir):
                logger.info(f"Skipping already completed video target: {v_out}")
                processed_total += 1
                cur_pct = (processed_total / total_targets * 100) if total_targets > 0 else 100.0
                job_manager.update_job(job_id, {
                    "progress": round(cur_pct, 2),
                    "output_path": v_out
                })
                continue

            job_manager.update_job(job_id, {"output_path": v_out})
            
            def vid_progress(current: int, total: int, frame: np.ndarray = None):
                file_pct = (current / total) if total > 0 else 0
                overall_pct = (((processed_total + file_pct) / total_targets) * 100) if total_targets > 0 else 100.0
                
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
                    updates["preview_image"] = create_b64_preview(frame, preview_res)
                job_manager.update_job(job_id, updates)
                
            process_video(
                source_face, 
                v_in, 
                v_out, 
                progress_callback=vid_progress, 
                cancel_event=cancel_event, 
                skip_existing=req.skip_existing,
                job_config=job_config,
                job_temp_dir=job_temp_dir
            )
            
            if cancel_event.is_set():
                v_dir = os.path.dirname(v_out)
                v_base = os.path.basename(v_out)
                cand_temp = os.path.join(v_dir, f"temp_{v_base}")
                if os.path.exists(cand_temp):
                    job_manager.update_job(job_id, {"output_path": cand_temp})
                break
                
            # If successfully completed, remove any leftover partial temporary videos (temp_ / retry_)
            v_dir, v_file = os.path.split(v_out)
            for pfx in ["temp_", "retry_"]:
                p_cand = os.path.join(v_dir, f"{pfx}{v_file}")
                if os.path.exists(p_cand):
                    try:
                        os.remove(p_cand)
                    except Exception:
                        pass

            processed_total += 1
                
        if not cancel_event.is_set():
            # Clean up ephemeral job sandbox (jobs/<job_id>)
            cleanup_job_workspace(x_client_platform, job_id, delete_output=False)
            
            final_output_path = job_output_dir
            if os.path.exists(job_output_dir):
                disk_files = [f for f in os.listdir(job_output_dir) if os.path.isfile(os.path.join(job_output_dir, f)) and os.path.getsize(os.path.join(job_output_dir, f)) > 0 and not f.startswith(("temp_", "retry_"))]
                if disk_files:
                    final_output_path = os.path.join(job_output_dir, sorted(disk_files)[-1])

            job_manager.update_job(job_id, {
                "status": "completed", 
                "progress": 100.0, 
                "frames_done": total_targets,
                "total_frames": total_targets,
                "output_path": final_output_path
            }, force=True)
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
                        outputs_dir=job_output_dir
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
    logger.info("[WORKER] Background job worker loop started and listening for tasks")
    while True:
        try:
            job_id, req, x_client_platform = job_manager.job_queue.get()
            logger.info(f"[WORKER] >>> Picked up Job {job_id} from queue (platform: {x_client_platform})")
            job = job_manager.get_job(job_id)
            
            # Skip if cancelled while in queue
            if job and job.get("status") == "failed" and job.get("error") == "Cancelled by user":
                logger.info(f"[WORKER] Job {job_id} was cancelled while in queue. Skipping.")
                job_manager.job_queue.task_done()
                continue
                
            run_job_background(job_id, req, x_client_platform)
            job_manager.job_queue.task_done()
            logger.info(f"[WORKER] <<< Finished processing Job {job_id}")
        except Exception as e:
            logger.error(f"[WORKER] Worker loop error: {e}", exc_info=True)

# Start background worker thread
worker_thread = threading.Thread(target=worker_loop, daemon=True)
worker_thread.start()
