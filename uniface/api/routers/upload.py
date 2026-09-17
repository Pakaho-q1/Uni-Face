import os
import hashlib
from fastapi import APIRouter, UploadFile, File, Form, Header
from uniface.core.workspace import ensure_workspace

router = APIRouter(prefix="/api/v1", tags=["upload"])

@router.post("/upload")
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

@router.post("/workspace/clear-temp")
async def clear_temp(x_client_platform: str = Header("unknown")):
    from uniface.core.workspace import clear_temp_uploads
    res = clear_temp_uploads(x_client_platform)
    return res

@router.get("/uploads/{file_path:path}")
async def serve_upload_file(file_path: str, x_client_platform: str = Header("unknown")):
    import mimetypes
    from fastapi import HTTPException
    from fastapi.responses import FileResponse
    uploads_dir, _ = ensure_workspace(x_client_platform)
    target = os.path.join(uploads_dir, file_path)
    if not os.path.exists(target):
        # Fallback to check default unknown platform
        target_fallback = os.path.join(os.path.dirname(uploads_dir), "unknown", "uploads", file_path)
        if os.path.exists(target_fallback):
            target = target_fallback
        else:
            raise HTTPException(status_code=404, detail="Uploaded file not found")
    media_type, _ = mimetypes.guess_type(target)
    return FileResponse(target, media_type=media_type or "image/jpeg")


