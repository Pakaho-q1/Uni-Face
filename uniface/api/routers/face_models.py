import os
import cv2
import uuid
import base64
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form, Header, HTTPException

from uniface.core.workspace import get_platform_dir, get_target_sets_dir
from uniface.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["face-models"])

@router.get("/api/v1/face-models")
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

@router.delete("/api/v1/face-models/{model_name}")
async def delete_face_model(
    model_name: str,
    x_client_platform: str = Header("unknown")
):
    platform_dir = get_platform_dir(x_client_platform)
    models_dir = os.path.join(platform_dir, "face_models")
    
    clean_name = os.path.basename(model_name)
    if not clean_name.endswith(".safetensors"):
        clean_name += ".safetensors"
        
    model_path = os.path.join(models_dir, clean_name)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model file not found")
        
    try:
        os.remove(model_path)
        return {"status": "success", "deleted": clean_name}
    except Exception as e:
        logger.error(f"Failed to delete face model {clean_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/face-models/build")
async def build_face_model(
    name: str = Form(...),
    files: list[UploadFile] = File(...),
    x_client_platform: str = Header("unknown")
):
    platform_dir = get_platform_dir(x_client_platform)
    from uniface.core.face_model import save_face_model
    from uniface.modules.detector import detect
    
    faces = []
    for file in files:
        content = await file.read()
        nparr = np.frombuffer(content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None:
            detected = detect(img)
            if detected:
                detected.sort(key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
                faces.append(detected[0])
                
    if not faces:
        raise HTTPException(status_code=400, detail="No faces detected in the provided images.")
        
    try:
        filepath = save_face_model(name, faces, platform_dir)
        return {"status": "success", "model_name": os.path.basename(filepath), "faces_extracted": len(faces)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/extract-faces")
async def extract_faces(
    x_client_platform: str = Header("unknown"),
    target_type: str = Form(...),
    sample_count: int = Form(5),
    files: list[UploadFile] = File(default=[]),
    file_ids: list[str] = Form(default=[])
):
    from uniface.modules.detector import detect
    
    extracted_faces = []
    seen_embeddings = []
    
    def add_faces_from_image(img_arr, limit):
        if img_arr is None: return 0
        faces = detect(img_arr)
        if not faces: return 0
        
        added = 0
        for f in faces:
            if seen_embeddings:
                sims = [np.dot(f.embedding, prev_emb)/(np.linalg.norm(f.embedding)*np.linalg.norm(prev_emb)+1e-8) for prev_emb in seen_embeddings]
                if max(sims) > 0.85:
                    continue
                    
            seen_embeddings.append(f.embedding)
            
            box = f.bbox.astype(int)
            x1, y1, x2, y2 = max(0, box[0]), max(0, box[1]), min(img_arr.shape[1], box[2]), min(img_arr.shape[0], box[3])
            crop = img_arr[y1:y2, x1:x2]
            
            if crop.size == 0: continue
            
            _, buffer = cv2.imencode('.jpg', crop)
            b64 = base64.b64encode(buffer).decode('utf-8')
            emb_b64 = base64.b64encode(f.embedding.tobytes()).decode('utf-8')
            
            extracted_faces.append({
                "id": emb_b64,
                "url": f"data:image/jpeg;base64,{b64}"
            })
            added += 1
            if len(extracted_faces) >= limit:
                break
        return added

    uploads_dir = os.path.join(get_platform_dir(x_client_platform), "uploads")
    target_sets_dir = get_target_sets_dir(x_client_platform)
    
    try:
        if target_type == "upload":
            for uf in files:
                ext = os.path.splitext(uf.filename)[1].lower()
                if ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
                    temp_path = os.path.join(uploads_dir, f"temp_scan_{uuid.uuid4().hex}{ext}")
                    os.makedirs(uploads_dir, exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(await uf.read())
                    try:
                        cap = cv2.VideoCapture(temp_path)
                        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        if total_frames > 0:
                            num_samples = min(sample_count, total_frames)
                            frame_indices = np.random.choice(total_frames, num_samples, replace=False)
                            for frame_idx in frame_indices:
                                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                                ret, frame = cap.read()
                                if ret:
                                    add_faces_from_image(frame, sample_count)
                                    if len(extracted_faces) >= sample_count:
                                        break
                        cap.release()
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                else:
                    contents = await uf.read()
                    nparr = np.frombuffer(contents, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    if img is not None:
                        add_faces_from_image(img, sample_count)
                
                if len(extracted_faces) >= sample_count:
                    break
        else:
            for fid in file_ids:
                if fid.startswith("set:"):
                    path = os.path.join(target_sets_dir, fid[4:])
                else:
                    path = os.path.join(uploads_dir, fid)
                    
                if os.path.exists(path):
                    import mimetypes
                    mt, _ = mimetypes.guess_type(path)
                    if mt and mt.startswith('video'):
                        cap = cv2.VideoCapture(path)
                        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        if total_frames > 0:
                            num_samples = min(sample_count, total_frames)
                            frame_indices = np.random.choice(total_frames, num_samples, replace=False)
                            for frame_idx in frame_indices:
                                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                                ret, frame = cap.read()
                                if ret:
                                    add_faces_from_image(frame, sample_count)
                                    if len(extracted_faces) >= sample_count:
                                        break
                        cap.release()
                    else:
                        img = cv2.imread(path)
                        if img is not None:
                            add_faces_from_image(img, sample_count)
                            
                if len(extracted_faces) >= sample_count:
                    break
    except Exception as e:
        logger.error(f"Error extracting faces: {e}", exc_info=True)
        
    return {
        "faces": extracted_faces
    }
