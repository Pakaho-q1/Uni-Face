import cv2
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from uniface.core.service import FaceService

app = FastAPI(title="Uni-Face API", description="Simple path-based face swap endpoint")

_service = FaceService()

class SwapRequest(BaseModel):
    source_path: str
    target_path: str
    output_path: str

@app.post("/swap")
def swap_faces(request: SwapRequest):
    source_img = cv2.imread(request.source_path)
    if source_img is None:
        raise HTTPException(status_code=400, detail=f"Cannot read source: {request.source_path}")

    target_img = cv2.imread(request.target_path)
    if target_img is None:
        raise HTTPException(status_code=400, detail=f"Cannot read target: {request.target_path}")

    try:
        result_img = _service.process_image(source_img, target_img)
        out_path = Path(request.output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out_path), result_img)
        return {"status": "ok", "output": str(out_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_server(port: int = 8000):
    uvicorn.run("api.adapter:app", host="0.0.0.0", port=port, reload=False)
