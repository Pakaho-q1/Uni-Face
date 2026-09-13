import os
import re
from uniface.core.config import ROOT_DIR

WORKSPACE_DIR = os.path.join(ROOT_DIR, "workspace")

def get_platform_dir(platform: str) -> str:
    if not platform:
        platform = "unknown"
    # Use re.sub — str.replace() does not interpret regex patterns
    platform = re.sub(r'[^a-z0-9_]', '_', platform.lower())
    return os.path.join(WORKSPACE_DIR, platform)

def ensure_workspace(platform: str):
    p_dir = get_platform_dir(platform)
    uploads_dir = os.path.join(p_dir, "uploads")
    source_dir = os.path.join(uploads_dir, "source")
    target_dir = os.path.join(uploads_dir, "target")
    immich_dir = os.path.join(uploads_dir, "immich")
    outputs_dir = os.path.join(p_dir, "outputs")
    target_sets_dir = os.path.join(p_dir, "target_sets")
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(immich_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(target_sets_dir, exist_ok=True)
    return uploads_dir, outputs_dir

def get_target_sets_dir(platform: str) -> str:
    p_dir = get_platform_dir(platform)
    target_sets_dir = os.path.join(p_dir, "target_sets")
    pool_dir = os.path.join(target_sets_dir, ".pool")
    os.makedirs(target_sets_dir, exist_ok=True)
    os.makedirs(pool_dir, exist_ok=True)
    return target_sets_dir

def clear_temp_uploads(platform: str) -> dict:
    """
    Manually clear temporary files in uploads/ directory while protecting target_sets/.
    """
    p_dir = get_platform_dir(platform)
    uploads_dir = os.path.join(p_dir, "uploads")
    deleted_count = 0
    reclaimed_bytes = 0

    if os.path.exists(uploads_dir):
        for root, dirs, files in os.walk(uploads_dir):
            for f in files:
                fpath = os.path.join(root, f)
                try:
                    size = os.path.getsize(fpath)
                    os.remove(fpath)
                    deleted_count += 1
                    reclaimed_bytes += size
                except Exception:
                    pass

    return {
        "success": True,
        "deleted_count": deleted_count,
        "reclaimed_bytes": reclaimed_bytes
    }

def get_jobs_dir(platform: str) -> str:
    p_dir = get_platform_dir(platform)
    jobs_dir = os.path.join(p_dir, "jobs")
    os.makedirs(jobs_dir, exist_ok=True)
    return jobs_dir

def get_job_workspace(platform: str, job_id: str) -> dict:
    p_dir = get_platform_dir(platform)
    job_dir = os.path.join(p_dir, "jobs", job_id)
    output_dir = os.path.join(p_dir, "outputs", job_id)
    return {
        "job_dir": job_dir,
        "source_dir": os.path.join(job_dir, "source"),
        "target_dir": os.path.join(job_dir, "target"),
        "temp_dir": os.path.join(job_dir, "temp"),
        "output_dir": output_dir,
    }

def ensure_job_workspace(platform: str, job_id: str) -> dict:
    ws = get_job_workspace(platform, job_id)
    os.makedirs(ws["source_dir"], exist_ok=True)
    os.makedirs(ws["target_dir"], exist_ok=True)
    os.makedirs(ws["temp_dir"], exist_ok=True)
    os.makedirs(ws["output_dir"], exist_ok=True)
    return ws

def safe_hardlink(src: str, dst: str):
    """
    Create a zero-copy hardlink from src to dst.
    If dst already exists, it is left untouched.
    Falls back to copy2 if hardlink fails (e.g. cross-volume).
    """
    if os.path.exists(dst):
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        os.link(src, dst)
    except OSError:
        import shutil
        shutil.copy2(src, dst)

def cleanup_job_workspace(platform: str, job_id: str, delete_output: bool = False):
    """
    Clean up job workspace. Always deletes ephemeral jobs/<job_id>/.
    Optionally deletes outputs/<job_id>/ when deleting the job permanently.
    """
    import shutil
    ws = get_job_workspace(platform, job_id)
    if os.path.exists(ws["job_dir"]):
        shutil.rmtree(ws["job_dir"], ignore_errors=True)
    if delete_output and os.path.exists(ws["output_dir"]):
        shutil.rmtree(ws["output_dir"], ignore_errors=True)


