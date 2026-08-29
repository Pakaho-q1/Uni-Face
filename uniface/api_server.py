import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn

# --- TRT Support: Auto-inject TensorRT libs into PATH ---
if sys.platform == 'win32':
    trt_path = os.path.join(sys.prefix, 'Lib', 'site-packages', 'tensorrt_libs')
    if os.path.exists(trt_path):
        os.environ['PATH'] = trt_path + os.pathsep + os.environ.get('PATH', '')
    else:
        python_id = f"python{sys.version_info.major}.{sys.version_info.minor}"
        trt_path = os.path.join(sys.prefix, 'lib', python_id, 'site-packages', 'tensorrt_libs')
        if os.path.exists(trt_path):
            os.environ['LD_LIBRARY_PATH'] = trt_path + os.pathsep + os.environ.get('LD_LIBRARY_PATH', '')

# --- Disable BLAS/OMP threading to prevent CPU thrashing during multi-thread processing ---
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

# Ensure we can import uniface modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from uniface.core.state import state
from uniface.core.db import init_db
from uniface.core.workspace import WORKSPACE_DIR
from uniface.core.job_manager import JobManager, job_manager
from uniface.api.middleware import BasicAuthMiddleware

# Load configurations from uni-face.ini
state.init(parse_args=False)

# Initialize Deduplication DB
init_db()

app = FastAPI(title="Uni-Face API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication & Connection Error Handling Middleware
app.add_middleware(BasicAuthMiddleware)

# --- Include Routers ---
from uniface.api.routers.upload import router as upload_router
from uniface.api.routers.target_sets import router as target_sets_router
from uniface.api.routers.jobs import router as jobs_router
from uniface.api.routers.face_models import router as face_models_router
from uniface.api.routers.history import router as history_router
from uniface.api.routers.immich import router as immich_router

app.include_router(upload_router)
app.include_router(target_sets_router)
app.include_router(jobs_router)
app.include_router(face_models_router)
app.include_router(history_router)
app.include_router(immich_router)

# --- Serve WebUI compiled dist ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
webui_dist = os.path.join(ROOT_DIR, "webui", "dist")

if os.path.exists(webui_dist):
    app.mount("/", StaticFiles(directory=webui_dist, html=True), name="webui")
else:
    static_dir = os.path.join(ROOT_DIR, "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    @app.get("/")
    async def root():
        return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    uvicorn.run("uniface.api_server:app", host="0.0.0.0", port=8000, reload=False)
