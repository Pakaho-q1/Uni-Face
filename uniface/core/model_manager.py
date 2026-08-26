import os
import requests
import hashlib
from pathlib import Path
from tqdm import tqdm
from uniface.core.config import MODEL_PATHS, MODELS_DIR

HF_REPO_URL = "https://huggingface.co/Pakaho-q1/Uni-Face/resolve/main"

def calculate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def download_file(url, dest_path, desc):
    try:
        response = requests.get(url, stream=True, timeout=15)
        if response.status_code == 404:
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
        print(f"\nError downloading {desc}: {e}")
        return False

def install_models(force=False):
    print(f"Checking {len(MODEL_PATHS)} models from Hugging Face...")
    
    success_count = 0
    fail_count = 0
    
    for model_name, local_path in MODEL_PATHS.items():
        if model_name == "ffmpeg":
            continue # Skip ffmpeg since it's an exe and usually bundled separately, but we uploaded it so let's check it anyway?
            # Actually, we can download ffmpeg.exe too since we uploaded it!
            
        try:
            rel_path = local_path.relative_to(MODELS_DIR)
        except ValueError:
            # Fallback if path manipulation fails
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
        except:
            pass # Use local hash if HF is unreachable or hash missing
            
        # 2. Check local file
        if not need_download and os.path.exists(local_path):
            if expected_hash:
                local_hash = calculate_hash(local_path)
                if local_hash != expected_hash:
                    print(f"[!] Hash mismatch for {model_name}. Marking for download...")
                    need_download = True
        else:
            need_download = True
            
        # 3. Download if needed
        if need_download:
            print(f"Downloading {model_name}...")
            if download_file(model_url, local_path, desc=model_name):
                print(f"[✓] {model_name} downloaded successfully.")
                success_count += 1
            else:
                print(f"[x] Failed to download {model_name}.")
                fail_count += 1
        else:
            print(f"[✓] {model_name} is up-to-date.")
            success_count += 1
            
    print("-" * 40)
    print(f"Installation Complete. Success: {success_count} | Failed: {fail_count}")
