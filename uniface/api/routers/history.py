import os
import uuid
import zipfile
import asyncio
import mimetypes
from typing import List, Optional
from fastapi import APIRouter, Header, HTTPException, BackgroundTasks, Query, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel

from uniface.core.workspace import ensure_workspace, get_platform_dir
from uniface.core.image_service import get_letterbox_thumbnail
from uniface.core.job_manager import is_image_path
from uniface.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["history"])

class DeleteHistoryRequest(BaseModel):
    filenames: List[str] = []
    delete_all: bool = False

class DownloadHistoryRequest(BaseModel):
    filenames: List[str]

def create_zip_sync(zip_path: str, filenames: List[str], outputs_dir: str) -> int:
    found = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in filenames:
            safe_rel = os.path.normpath(f).lstrip(os.sep).lstrip("/")
            path = os.path.abspath(os.path.join(outputs_dir, safe_rel))
            if path.startswith(os.path.abspath(outputs_dir)) and os.path.exists(path):
                zf.write(path, os.path.basename(f))
                found += 1
    return found

def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        logger.debug(f"Failed to cleanup file {path}: {e}")

@router.get("/api/v1/history")
async def get_history(x_client_platform: str = Header("unknown"), skip: int = 0, limit: int = 50):
    _, outputs_dir = ensure_workspace(x_client_platform)
    files = []
    if os.path.exists(outputs_dir):
        for root, dirs, f_list in os.walk(outputs_dir):
            # Ignore temp directories
            parts = os.path.relpath(root, outputs_dir).split(os.sep)
            if "temp" in parts:
                continue
            for f in f_list:
                path = os.path.join(root, f)
                if os.path.isfile(path):
                    rel_name = os.path.relpath(path, outputs_dir).replace("\\", "/")
                    if is_image_path(path):
                        mtype = 'image'
                    else:
                        mt, _ = mimetypes.guess_type(path)
                        mtype = 'video' if mt and mt.startswith('video') else 'image'
                    files.append({
                        "filename": rel_name,
                        "url": f"/api/v1/history/{rel_name}?platform={x_client_platform}",
                        "type": mtype,
                        "size": os.path.getsize(path),
                        "created_at": os.path.getmtime(path)
                    })
        files.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {"history": files[skip:skip+limit], "total": len(files)}

@router.get("/api/v1/history/{filename:path}")
async def serve_history_file(
    filename: str, 
    platform: str = "unknown",
    res: Optional[int] = Query(None, description="On-the-fly thumbnail resolution (256-720)")
):
    _, outputs_dir = ensure_workspace(platform)
    safe_rel = os.path.normpath(filename).lstrip(os.sep).lstrip("/")
    file_path = os.path.abspath(os.path.join(outputs_dir, safe_rel))
    
    # Path traversal protection
    if not file_path.startswith(os.path.abspath(outputs_dir)):
        raise HTTPException(status_code=403, detail="Access denied")
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        # Fallback: search recursively in outputs_dir for the filename (e.g. outputs/<job_id>/<filename>)
        fname = os.path.basename(filename)
        found_path = None
        if os.path.exists(outputs_dir):
            for root, dirs, files in os.walk(outputs_dir):
                if fname in files:
                    found_path = os.path.join(root, fname)
                    break
        if found_path and os.path.isfile(found_path):
            file_path = found_path
        else:
            raise HTTPException(status_code=404, detail="File not found")
        
    media_type, _ = mimetypes.guess_type(file_path)
    if is_image_path(file_path) and not media_type:
        media_type = "image/jpeg"
    
    if res is not None and (is_image_path(file_path) or (media_type and media_type.startswith("image/"))):
        target_res = min(max(int(res), 128), 1080)
        thumb_bytes = get_letterbox_thumbnail(file_path, target_size=target_res)
        if thumb_bytes:
            return Response(
                content=thumb_bytes,
                media_type="image/jpeg",
                headers={
                    "Cache-Control": "public, max-age=604800",
                    "Content-Disposition": f'inline; filename="thumb_{os.path.basename(filename)}.jpg"'
                }
            )
            
    return FileResponse(file_path, media_type=media_type or "application/octet-stream")

@router.delete("/api/v1/history")
async def delete_history(req: DeleteHistoryRequest, x_client_platform: str = Header("unknown")):
    _, outputs_dir = ensure_workspace(x_client_platform)
    deleted = 0
    
    if req.delete_all:
        if os.path.exists(outputs_dir):
            for root, dirs, files in os.walk(outputs_dir, topdown=False):
                for f in files:
                    path = os.path.join(root, f)
                    try:
                        os.remove(path)
                        deleted += 1
                    except Exception as e:
                        logger.warning(f"Failed to delete {path}: {e}")
                for d in dirs:
                    dpath = os.path.join(root, d)
                    try:
                        if os.path.exists(dpath) and not os.listdir(dpath):
                            os.rmdir(dpath)
                    except Exception:
                        pass
    else:
        for f in req.filenames:
            safe_rel = os.path.normpath(f).lstrip(os.sep).lstrip("/")
            path = os.path.abspath(os.path.join(outputs_dir, safe_rel))
            if path.startswith(os.path.abspath(outputs_dir)) and os.path.exists(path):
                try:
                    os.remove(path)
                    deleted += 1
                    parent = os.path.dirname(path)
                    if parent != os.path.abspath(outputs_dir) and os.path.exists(parent) and not os.listdir(parent):
                        os.rmdir(parent)
                except Exception as e:
                    logger.warning(f"Failed to delete {path}: {e}")
    return {"deleted": deleted}

@router.post("/api/v1/history/download")
async def download_history_bulk(
    req: DownloadHistoryRequest, 
    background_tasks: BackgroundTasks, 
    x_client_platform: str = Header("unknown")
):
    _, outputs_dir = ensure_workspace(x_client_platform)
    
    if len(req.filenames) == 1:
        safe_rel = os.path.normpath(req.filenames[0]).lstrip(os.sep).lstrip("/")
        path = os.path.abspath(os.path.join(outputs_dir, safe_rel))
        if not path.startswith(os.path.abspath(outputs_dir)) or not os.path.exists(path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(path, filename=os.path.basename(path))
        
    downloads_dir = os.path.join(get_platform_dir(x_client_platform), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    
    for f in os.listdir(downloads_dir):
        if f.endswith(".zip"):
            try:
                os.remove(os.path.join(downloads_dir, f))
            except Exception as e:
                logger.debug(f"Failed to remove stale zip {f}: {e}")

    zip_filename = f"uni_face_export_{uuid.uuid4().hex[:8]}.zip"
    zip_path = os.path.join(downloads_dir, zip_filename)
    
    found = await asyncio.to_thread(create_zip_sync, zip_path, req.filenames, outputs_dir)
                
    if found == 0:
        cleanup_file(zip_path)
        raise HTTPException(status_code=404, detail="No files found")
        
    return FileResponse(zip_path, media_type="application/zip", filename="uni-face-export.zip")

