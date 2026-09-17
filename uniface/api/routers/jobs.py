import os
import asyncio
import hashlib
import mimetypes
from typing import Optional
from fastapi import APIRouter, Header, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import FileResponse

from uniface.core.job_manager import job_manager, JobStartRequest, PreviewSettings
from uniface.core.logging import get_logger
from uniface.core import db

logger = get_logger(__name__)
router = APIRouter(tags=["jobs"])

@router.post("/api/v1/jobs")
async def create_job(
    req: JobStartRequest,
    x_client_platform: str = Header("unknown")
):
    job_id = job_manager.create_job(x_client_platform, req)
    job_manager.update_job(job_id, {
        "preview_enabled": req.preview_enabled,
        "preview_resolution": req.preview_resolution
    })
    
    # Enqueue job into background worker loop
    job_manager.job_queue.put((job_id, req, x_client_platform))
    
    return {"job_id": job_id, "status": "pending"}

@router.get("/api/v1/jobs")
async def list_jobs(
    status: Optional[str] = Query(None, description="Filter by status: active, pending, processing, completed, failed, cancelled"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    x_client_platform: str = Header("unknown")
):
    records = db.list_job_records(platform=x_client_platform, status=status, limit=limit, offset=offset)
    total = db.get_jobs_count(platform=x_client_platform, status=status)
    active_count = db.get_active_jobs_count(platform=x_client_platform)
    return {"jobs": records, "total": total, "active_count": active_count}

@router.get("/api/v1/jobs/active-count")
async def get_active_count(x_client_platform: str = Header("unknown")):
    count = db.get_active_jobs_count(platform=x_client_platform)
    return {"active_count": count}

@router.post("/api/v1/jobs/{job_id}/rerun")
async def rerun_job_endpoint(job_id: str):
    new_job_id = job_manager.rerun_job(job_id)
    if not new_job_id:
        raise HTTPException(status_code=400, detail="Unable to rerun job. Missing config or job not found.")
    return {"status": "enqueued", "new_job_id": new_job_id}

@router.post("/api/v1/jobs/{job_id}/retry")
async def retry_job_endpoint(job_id: str):
    logger.info(f"[API] >>> Received retry request for Job ID: {job_id}")
    success = job_manager.retry_job(job_id)
    if not success:
        logger.warning(f"[API] <<< Retry rejected for Job ID: {job_id}")
        raise HTTPException(status_code=400, detail="Unable to retry job. Missing config or job not found.")
    logger.info(f"[API] <<< Retry accepted for Job ID: {job_id}")
    return {"status": "pending", "job_id": job_id}

@router.get("/api/v1/jobs/debug")
async def get_jobs_debug(x_client_platform: str = Header("unknown")):
    from uniface.core.job_manager import worker_thread
    recent = db.list_job_records(platform=x_client_platform, limit=5)
    return {
        "worker_thread_alive": worker_thread.is_alive() if worker_thread else False,
        "job_queue_size": job_manager.job_queue.qsize(),
        "active_cancel_events": list(job_manager.cancel_events.keys()),
        "recent_jobs": [
            {
                "id": j.get("id"),
                "status": j.get("status"),
                "progress": j.get("progress"),
                "error": j.get("error"),
                "frames_done": j.get("frames_done"),
                "total_frames": j.get("total_frames"),
                "target_count": j.get("target_count")
            } for j in recent
        ]
    }

@router.delete("/api/v1/jobs/{job_id}")
async def delete_single_job(job_id: str):
    success = job_manager.delete_job(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "deleted", "job_id": job_id}

@router.delete("/api/v1/jobs")
async def clear_completed_jobs(x_client_platform: str = Header("unknown")):
    # Clean temp folders for finished/cancelled jobs
    records = db.list_job_records(platform=x_client_platform, limit=1000)
    for r in records:
        if r.get("status") in ['completed', 'failed', 'cancelled']:
            job_manager.clean_job_temp_dir(r)
    cleared = db.clear_completed_job_records(platform=x_client_platform)
    return {"status": "cleared", "count": cleared}

@router.post("/api/v1/jobs/{job_id}/preview")
async def update_preview_settings(job_id: str, settings: PreviewSettings):
    job_manager.update_job(job_id, {
        "preview_enabled": settings.enabled,
        "preview_resolution": settings.resolution
    })
    return {"status": "success"}

@router.get("/api/v1/jobs/active")
async def get_active_job(x_client_platform: str = Header("unknown")):
    job = job_manager.get_active_job_for_platform(x_client_platform)
    if not job:
        return {"job_id": None}
    
    resp = job.copy()
    resp.pop("preview_image", None)
    return {"job_id": job["id"], "job": resp}

@router.get("/api/v1/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    resp = job.copy()
    resp.pop("preview_image", None)
    return resp

@router.post("/api/v1/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job_manager.cancel_job(job_id)
    return {"status": "cancelling"}

@router.get("/api/v1/jobs/{job_id}/download")
async def download_job(job_id: str):
    job = job_manager.get_job(job_id)
    if not job or not job.get("output_path"):
        raise HTTPException(status_code=404, detail="Job output not found")
        
    output_path = job["output_path"]
    if not os.path.exists(output_path):
        d = os.path.dirname(output_path)
        b = os.path.basename(output_path)
        temp_cand = os.path.join(d, f"temp_{b}")
        if os.path.exists(temp_cand):
            output_path = temp_cand
        else:
            base, ext = os.path.splitext(output_path)
            percent = int(job.get("progress", 0))
            partial_path = f"{base}_{percent}%{ext}"
            if os.path.exists(partial_path):
                output_path = partial_path
            else:
                raise HTTPException(status_code=404, detail="File not ready")
            
    media_type, _ = mimetypes.guess_type(output_path)
    if not media_type:
        media_type = "application/octet-stream"
        
    return FileResponse(output_path, media_type=media_type, filename=os.path.basename(output_path))

@router.websocket("/api/v1/ws/jobs/{job_id}")
async def websocket_job_status(websocket: WebSocket, job_id: str):
    await websocket.accept()
    job_manager.active_websockets[job_id] = websocket
    last_preview_hash: str = ""
    
    try:
        while True:
            job = job_manager.get_job(job_id)
            if not job:
                await websocket.send_json({"error": "Job not found"})
                break
            
            resp = {k: v for k, v in job.items() if k != "preview_image"}
            preview = job.get("preview_image")
            if preview:
                mid = len(preview) // 2
                preview_hash = hashlib.md5(
                    (preview[mid : mid + 256] + preview[-128:]).encode()
                ).hexdigest()
                if preview_hash != last_preview_hash:
                    resp["preview_image"] = preview
                    last_preview_hash = preview_hash
                
            await websocket.send_json(resp)
            
            if job["status"] in ["completed", "failed", "cancelled"]:
                break
                
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        logger.debug(f"Client disconnected. Job {job_id} will continue in background.")
    except Exception as e:
        logger.error(f"WebSocket error for job {job_id}: {e}")
    finally:
        if job_id in job_manager.active_websockets:
            del job_manager.active_websockets[job_id]
