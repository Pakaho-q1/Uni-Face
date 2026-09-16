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

@router.post("/face/clean-preview")
async def face_clean_preview(
    file: UploadFile = File(None),
    file_id: str = Form(None),
    x_client_platform: str = Header("unknown")
):
    import cv2
    import numpy as np
    import base64
    from uniface.modules.detector import detect, NativeDetector
    
    img = None
    if file:
        content = await file.read()
        nparr = np.frombuffer(content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    elif file_id:
        uploads_dir, _ = ensure_workspace(x_client_platform)
        target = os.path.join(uploads_dir, file_id)
        if not os.path.exists(target):
            target_fallback = os.path.join(os.path.dirname(uploads_dir), "unknown", "uploads", file_id)
            if os.path.exists(target_fallback):
                target = target_fallback
        if os.path.exists(target):
            img = cv2.imread(target)
            
    if img is None:
        return {"success": False, "error": "No valid image provided"}
        
    faces = detect(img, extract_embedding=False, extract_gender_age=False)
    if not faces:
        return {"success": False, "error": "No face detected in the image"}
        
    faces.sort(key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
    best_face = faces[0]
    
    from uniface.modules.utils import face_math
    orig_crop, _ = face_math.warp_face_by_face_landmark_5(
        img, best_face.landmark_5, 'ffhq_512', (512, 512)
    )
    
    if orig_crop is None:
        # Fallback to arcface template if ffhq template fails
        orig_crop, _ = face_math.warp_face_by_face_landmark_5(
            img, best_face.landmark_5, 'arcface_112_v2', (512, 512)
        )
        
    if orig_crop is None:
        return {"success": False, "error": "Failed to crop face"}
        
    _, orig_buf = cv2.imencode('.jpg', orig_crop, [cv2.IMWRITE_JPEG_QUALITY, 92])
    orig_b64 = base64.b64encode(orig_buf).decode('utf-8')
    
    return {
        "success": True,
        "has_face": True,
        "has_forehead_hair": False,
        "original_crop": f"data:image/jpeg;base64,{orig_b64}",
        "hair_mask": None,
        "cleaned_crop": f"data:image/jpeg;base64,{orig_b64}"
    }


