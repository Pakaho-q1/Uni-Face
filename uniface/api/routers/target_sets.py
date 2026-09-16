import os
import re
import cv2
import json
import uuid
import shutil
import hashlib
import mimetypes
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, Header, HTTPException, Query, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel

from uniface.core.workspace import get_target_sets_dir, WORKSPACE_DIR
from uniface.core.db import get_hash_path, register_hash, remove_hash
from uniface.core.image_service import get_letterbox_thumbnail
from uniface.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["target-sets"])

def get_video_duration(file_path: str) -> Optional[float]:
    try:
        cap = cv2.VideoCapture(file_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        cap.release()
        if fps > 0 and frames > 0:
            return float(frames / fps)
    except Exception as e:
        logger.debug(f"Failed to get video duration for {file_path}: {e}")
    return None

def update_set_meta(set_path: str, filename: str, info: dict):
    meta_path = os.path.join(set_path, ".meta.json")
    meta = {}
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception as e:
            logger.debug(f"Failed to load meta file {meta_path}: {e}")
    if filename not in meta:
        meta[filename] = {}
    meta[filename].update(info)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f)

class FileHashInfo(BaseModel):
    filename: str
    hash: str

class PreflightRequest(BaseModel):
    files: List[FileHashInfo]

class LinkRequest(BaseModel):
    files: List[FileHashInfo]

class DeleteFilesRequest(BaseModel):
    filenames: List[str]

@router.get("/api/v1/target-sets")
async def get_target_sets(x_client_platform: str = Header("unknown")):
    sets_dir = get_target_sets_dir(x_client_platform)
    result = []
    for set_name in os.listdir(sets_dir):
        if set_name == ".pool":
            continue
            
        set_path = os.path.join(sets_dir, set_name)
        if os.path.isdir(set_path):
            meta_path = os.path.join(set_path, ".meta.json")
            meta = {}
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                except Exception as e:
                    logger.debug(f"Error reading meta for set {set_name}: {e}")

            files = []
            for f in os.listdir(set_path):
                if f == ".meta.json":
                    continue
                if os.path.isfile(os.path.join(set_path, f)):
                    file_info = {
                        "filename": f,
                        "file_id": f"set:{set_name}/{f}",
                        "url": f"/api/v1/target-sets/media/{set_name}/{f}?platform={x_client_platform}"
                    }
                    if f in meta and "duration" in meta[f] and meta[f]["duration"] is not None:
                        file_info["duration"] = meta[f]["duration"]
                    files.append(file_info)
            result.append({"name": set_name, "files": files})
    return {"target_sets": result}

@router.post("/api/v1/target-sets")
async def create_target_set(name: str = Form(...), x_client_platform: str = Header("unknown")):
    safe_name = re.sub(r'[^a-zA-Z0-9_\-\s]', '', name).strip()
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid set name")
        
    sets_dir = get_target_sets_dir(x_client_platform)
    set_path = os.path.join(sets_dir, safe_name)
    if os.path.exists(set_path):
        raise HTTPException(status_code=400, detail="Target set already exists")
        
    os.makedirs(set_path)
    return {"status": "ok", "name": safe_name}

@router.delete("/api/v1/target-sets/{set_name}")
async def delete_target_set(set_name: str, x_client_platform: str = Header("unknown")):
    sets_dir = get_target_sets_dir(x_client_platform)
    set_path = os.path.join(sets_dir, set_name)
    if os.path.exists(set_path) and os.path.isdir(set_path):
        shutil.rmtree(set_path)
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="Target set not found")

@router.post("/api/v1/target-sets/preflight")
async def target_sets_preflight(req: PreflightRequest):
    results = []
    for f in req.files:
        pool_path = get_hash_path(f.hash)
        if pool_path and os.path.exists(pool_path):
            results.append({"filename": f.filename, "hash": f.hash, "status": "exists"})
        else:
            if pool_path:
                remove_hash(f.hash)
            results.append({"filename": f.filename, "hash": f.hash, "status": "new"})
    return {"results": results}

@router.post("/api/v1/target-sets/{set_name}/link")
async def link_to_target_set(
    set_name: str,
    req: LinkRequest,
    x_client_platform: str = Header("unknown")
):
    sets_dir = get_target_sets_dir(x_client_platform)
    set_path = os.path.join(sets_dir, set_name)
    if not os.path.exists(set_path) or not os.path.isdir(set_path):
        raise HTTPException(status_code=404, detail="Target set not found")
        
    linked = []
    for f in req.files:
        pool_path = get_hash_path(f.hash)
        if not pool_path or not os.path.exists(pool_path):
            continue
            
        target_file_path = os.path.join(set_path, f.filename)
        if os.path.exists(target_file_path):
            continue
            
        try:
            os.link(pool_path, target_file_path)
            
            _, ext = os.path.splitext(f.filename)
            if ext.lower() in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
                duration = get_video_duration(pool_path)
                update_set_meta(set_path, f.filename, {"duration": duration})
            
            linked.append({
                "filename": f.filename,
                "file_id": f"set:{set_name}/{f.filename}",
                "url": f"/api/v1/target-sets/media/{set_name}/{f.filename}?platform={x_client_platform}"
            })
        except Exception as e:
            logger.error(f"Error hardlinking {pool_path} to {target_file_path}: {e}")
            
    return {"linked": linked}

@router.post("/api/v1/target-sets/{set_name}/upload")
async def upload_to_target_set(
    set_name: str,
    files: List[UploadFile] = File(...),
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
            with open(temp_pool_path, "wb") as buffer:
                while chunk := await file.read(1024 * 1024 * 5):  # 5MB chunks
                    md5.update(chunk)
                    buffer.write(chunk)
                    size += len(chunk)
                    
            file_hash = md5.hexdigest()
            _, ext = os.path.splitext(file.filename)
            pool_path = os.path.join(pool_dir, f"{file_hash}{ext}")
            
            if not os.path.exists(pool_path):
                os.rename(temp_pool_path, pool_path)
                register_hash(file_hash, pool_path, size)
            else:
                os.remove(temp_pool_path)
                
            target_file_path = os.path.join(set_path, file.filename)
            
            if not os.path.exists(target_file_path):
                try:
                    os.link(pool_path, target_file_path)
                except Exception:
                    shutil.copy2(pool_path, target_file_path)
            
            if ext.lower() in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
                duration = get_video_duration(pool_path)
                update_set_meta(set_path, file.filename, {"duration": duration})
                    
            uploaded.append({
                "filename": file.filename,
                "file_id": f"set:{set_name}/{file.filename}",
                "url": f"/api/v1/target-sets/media/{set_name}/{file.filename}?platform={x_client_platform}"
            })
        except Exception as e:
            if os.path.exists(temp_pool_path):
                os.remove(temp_pool_path)
            logger.error(f"Upload to target set failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
            
    return {"uploaded": uploaded}

@router.post("/api/v1/system/gc")
async def run_garbage_collection(x_client_platform: str = Header("unknown")):
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
            if stat.st_nlink == 1:
                freed_bytes += stat.st_size
                os.remove(file_path)
                file_hash, _ = os.path.splitext(filename)
                remove_hash(file_hash)
                deleted_count += 1
                
    return {
        "status": "ok", 
        "deleted_files": deleted_count, 
        "freed_bytes": freed_bytes
    }

@router.post("/api/v1/system/unload-models")
async def unload_models_endpoint():
    from uniface.core.model_manager import unload_all_models
    unload_all_models()
    return {"status": "ok", "message": "All inactive model sessions unloaded from memory"}

@router.post("/api/v1/target-sets/{set_name}/delete-files")
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
            
            meta_path = os.path.join(set_path, ".meta.json")
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    if filename in meta:
                        del meta[filename]
                        with open(meta_path, "w", encoding="utf-8") as f:
                            json.dump(meta, f)
                except Exception as e:
                    logger.debug(f"Failed to update meta during file delete: {e}")
            
    return {"status": "ok", "deleted": deleted}

@router.get("/api/v1/target-sets/media/{set_name}/{filename}")
async def get_target_set_media(
    set_name: str, 
    filename: str, 
    platform: Optional[str] = None,
    x_client_platform: str = Header("unknown"),
    res: Optional[int] = Query(None, description="On-the-fly thumbnail resolution (256-720)")
):
    actual_platform = platform if platform else x_client_platform
    sets_dir = get_target_sets_dir(actual_platform)
    file_path = os.path.join(sets_dir, set_name, filename)
    
    if not os.path.exists(file_path):
        for p in os.listdir(WORKSPACE_DIR):
            alt_path = os.path.join(WORKSPACE_DIR, p, "target_sets", set_name, filename)
            if os.path.exists(alt_path):
                file_path = alt_path
                break
                
    if os.path.exists(file_path):
        media_type, _ = mimetypes.guess_type(file_path)
        if res is not None and media_type and media_type.startswith("image/"):
            target_res = min(max(int(res), 128), 1080)
            thumb_bytes = get_letterbox_thumbnail(file_path, target_size=target_res)
            if thumb_bytes:
                return Response(
                    content=thumb_bytes,
                    media_type="image/jpeg",
                    headers={
                        "Cache-Control": "public, max-age=604800",
                        "Content-Disposition": f'inline; filename="thumb_{filename}.jpg"'
                    }
                )
        return FileResponse(file_path, media_type=media_type or "application/octet-stream")
    raise HTTPException(status_code=404, detail="File not found")
