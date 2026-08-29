import os
import asyncio
import hashlib
import mimetypes
from fastapi import APIRouter, Header, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from uniface.core.job_manager import job_manager, JobStartRequest, PreviewSettings
from uniface.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["jobs"])

@router.post("/api/v1/jobs")
async def create_job(
    req: JobStartRequest,
    x_client_platform: str = Header("unknown")
):
    job_id = job_manager.create_job(x_client_platform)
    job_manager.update_job(job_id, {
        "preview_enabled": req.preview_enabled,
        "preview_resolution": req.preview_resolution
    })
    
    # Enqueue job into background worker loop
    job_manager.job_queue.put((job_id, req, x_client_platform))
    
    return {"job_id": job_id, "status": "pending"}

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
            
            if job["status"] in ["completed", "failed"]:
                break
                
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        logger.debug(f"Client disconnected. Job {job_id} will continue in background.")
    except Exception as e:
        logger.error(f"WebSocket error for job {job_id}: {e}")
    finally:
        if job_id in job_manager.active_websockets:
            del job_manager.active_websockets[job_id]
