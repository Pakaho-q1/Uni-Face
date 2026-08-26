import os
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def run_command(command, cwd=None):
    cmd_str = ' '.join(command) if isinstance(command, list) else command
    print(f"> {cmd_str}")
    try:
        subprocess.check_call(command, cwd=cwd, shell=isinstance(command, str))
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

def install_python_deps():
    print("--- Installing Python Dependencies ---")
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Check hardware args
    args_str = " ".join(sys.argv).lower()
    if "cuda" in args_str or "tensorrt" in args_str:
        print("Hardware acceleration requested. Installing onnxruntime-gpu...")
        run_command([sys.executable, "-m", "pip", "install", "onnxruntime-gpu"])
    
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=str(ROOT_DIR))

def main():
    print("===========================================")
    print("      Uni-Face Native Installer")
    print("===========================================")
    install_python_deps()
    print("===========================================")
    print(" Installation Complete! 🎉")
    print(" You can now run the web interface with:")
    print(" run_uniface.bat")
    print("===========================================")

if __name__ == "__main__":
    main()
