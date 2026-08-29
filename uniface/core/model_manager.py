import os
import requests
import hashlib
from pathlib import Path
from tqdm import tqdm
from typing import Optional, Union, Dict

from uniface.core.config import MODEL_PATHS, MODELS_DIR
from uniface.core.logging import get_logger

logger = get_logger(__name__)
HF_REPO_URL = "https://huggingface.co/Pakaho-q1/Uni-Face/resolve/main"

def calculate_hash(file_path: Union[str, Path]) -> str:
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def download_file(url: str, dest_path: Union[str, Path], desc: str) -> bool:
    try:
        response = requests.get(url, stream=True, timeout=15)
        if response.status_code == 404:
            logger.warning(f"File not found on remote (404): {url}")
            return False
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        with open(dest_path, 'wb') as f, tqdm(
            desc=desc,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
            leave=False
        ) as bar:
            for data in response.iter_content(chunk_size=8192):
                size = f.write(data)
                bar.update(size)
        return True
    except Exception as e:
        logger.error(f"Error downloading {desc}: {e}")
        return False

def install_models(force: bool = False) -> Dict[str, int]:
    logger.info(f"Checking {len(MODEL_PATHS)} models from Hugging Face...")
    
    success_count = 0
    fail_count = 0
    
    for model_name, local_path in MODEL_PATHS.items():
        try:
            rel_path = local_path.relative_to(MODELS_DIR)
        except ValueError:
            rel_path = Path(local_path.name)
            
        url_path = str(rel_path).replace("\\", "/")
        model_url = f"{HF_REPO_URL}/{url_path}"
        hash_url = f"{HF_REPO_URL}/{url_path.replace('.onnx', '.hash').replace('.exe', '.hash')}"
        
        hash_path = local_path.with_suffix('.hash')
        expected_hash = None
        need_download = force
        
        # 1. Try to fetch the hash from HF
        try:
            r = requests.get(hash_url, timeout=5)
            if r.status_code == 200:
                expected_hash = r.text.strip()
                os.makedirs(os.path.dirname(hash_path), exist_ok=True)
                with open(hash_path, 'w') as f:
                    f.write(expected_hash)
        except Exception as e:
            logger.debug(f"Could not fetch remote hash for {model_name}: {e}")
            
        # 2. Check local file
        if not need_download and os.path.exists(local_path):
            if expected_hash:
                local_hash = calculate_hash(local_path)
                if local_hash != expected_hash:
                    logger.warning(f"Hash mismatch for {model_name}. Marking for download...")
                    need_download = True
        else:
            need_download = True
            
        # 3. Download if needed
        if need_download:
            logger.info(f"Downloading {model_name}...")
            if download_file(model_url, local_path, desc=model_name):
                logger.info(f"[OK] {model_name} downloaded successfully.")
                success_count += 1
            else:
                logger.error(f"[FAIL] Failed to download {model_name}.")
                fail_count += 1
        else:
            logger.info(f"[OK] {model_name} is up-to-date.")
            success_count += 1
            
    logger.info("-" * 40)
    logger.info(f"Installation Complete. Success: {success_count} | Failed: {fail_count}")
    return {"success": success_count, "failed": fail_count}
