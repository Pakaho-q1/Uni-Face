import os
import sys
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def run_command(command, cwd=None):
    cmd_str = ' '.join(command) if isinstance(command, list) else command
    print(f"> {cmd_str}")
    try:
        subprocess.check_call(command, cwd=cwd, shell=isinstance(command, str))
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error executing command: {e}")
        sys.exit(1)

def install_dependencies():
    print("\n--- 📦 Upgrading pip ---")
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # Check hardware args
    args_str = " ".join(sys.argv).lower()
    is_gpu = "cuda" in args_str or "tensorrt" in args_str or "gpu" in args_str

    if is_gpu:
        print("\n--- ⚡ Hardware Acceleration (GPU/CUDA) Selected ---")
        run_command([sys.executable, "-m", "pip", "install", "onnxruntime-gpu"])
    else:
        print("\n--- 💻 Standard CPU Installation (Run 'python install.py cuda' for NVIDIA GPU acceleration) ---")

    print("\n--- 📥 Installing Core Requirements ---")
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=str(ROOT_DIR))

    # Install local immich SDK package
    immich_sdk_dir = ROOT_DIR / "immich_sdk_repo"
    if immich_sdk_dir.exists():
        print("\n--- ☁️ Installing Immich SDK Integration ---")
        run_command([sys.executable, "-m", "pip", "install", "-e", "immich_sdk_repo"], cwd=str(ROOT_DIR))

    # Ensure required runtime folders exist
    (ROOT_DIR / "models").mkdir(parents=True, exist_ok=True)
    (ROOT_DIR / "workspace").mkdir(parents=True, exist_ok=True)

def main():
    print("=====================================================")
    print("        ⚡ Uni-Face Native Installer ⚡             ")
    print("=====================================================")
    install_dependencies()
    print("\n=====================================================")
    print(" 🎉 Installation Complete!                           ")
    print("=====================================================")
    print(" Next steps:")
    print(" 1. Download neural network models:")
    print("    python uni-face.py models install")
    print("")
    print(" 2. Launch the Web Interface:")
    print("    run_uniface.bat")
    print("    (or: python uni-face.py webui)")
    print("=====================================================\n")

if __name__ == "__main__":
    main()
