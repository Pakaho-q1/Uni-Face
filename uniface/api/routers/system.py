import os
from fastapi import APIRouter, Header
from uniface.core.workspace import get_target_sets_dir
from uniface.core.db import remove_hash
from uniface.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/system", tags=["system"])

@router.post("/gc")
async def run_garbage_collection(x_client_platform: str = Header("unknown")):
    """Run garbage collection on unlinked target pool files."""
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
                try:
                    os.remove(file_path)
                    file_hash, _ = os.path.splitext(filename)
                    remove_hash(file_hash)
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"Failed to delete unlinked pool file {file_path}: {e}")

    return {
        "status": "ok",
        "deleted_files": deleted_count,
        "freed_bytes": freed_bytes
    }

@router.post("/unload-models")
async def unload_models_endpoint():
    """Unload all inactive ONNX model sessions to free GPU VRAM and RAM."""
    from uniface.core.model_manager import unload_all_models
    unload_all_models()
    return {"status": "ok", "message": "All inactive model sessions unloaded from memory"}
