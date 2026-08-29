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

