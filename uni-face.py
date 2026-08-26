import cv2
import sys
import os
import sys

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

import numpy as np
import onnxruntime
# Suppress C++ warnings (e.g. Missing TensorRT DLL) to keep console clean
onnxruntime.set_default_logger_severity(3)

from uniface.core.state import state
from uniface.core.service import process_image
from uniface.core.video_service import process_video

# --- CLI Intercepts ---
if len(sys.argv) > 1:
    cmd = sys.argv[1]
    if cmd == "models":
        import argparse
        models_parser = argparse.ArgumentParser(prog="uni-face.py models")
        models_parser.add_argument("subcommand", choices=["install"], help="Models subcommand (e.g. install)")
        models_parser.add_argument("--force", action="store_true", help="Force redownload all models")
        models_args = models_parser.parse_args(sys.argv[2:])
        
        if models_args.subcommand == "install":
            from uniface.core.model_manager import install_models
            install_models(force=models_args.force)
        sys.exit(0)
        
    elif cmd in ["serve", "webui"]:
        import argparse
        import uvicorn
        serve_parser = argparse.ArgumentParser(prog=f"uni-face.py {cmd}")
        serve_parser.add_argument("--port", type=int, default=8000, help="Port to run the API server on")
        serve_args = serve_parser.parse_args(sys.argv[2:])
        
        # Start the real FastAPI server with the WebUI
        print(f"Starting Uni-Face WebUI on port {serve_args.port}...")
        uvicorn.run("uniface.api_server:app", host="0.0.0.0", port=serve_args.port, reload=False)
        sys.exit(0)
# ----------------------

def process_single_target(source_face, source_img, target_path, output_path):
    is_video = target_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))
    
    if is_video:
        process_video(source_face, target_path, output_path)
        print(f"Success! Video output saved to {output_path}")
    else:
        target_img = cv2.imread(target_path)
        if target_img is None:
            print(f"Error: Could not read target image {target_path}")
            return
            
        result_img = process_image(source_face, target_img)
        cv2.imwrite(output_path, result_img)
        
        sim_text = ""
        if state.similarity:
            from uniface.modules.detector import detect
            result_faces = detect(result_img)
            
            if source_face and result_faces:
                result_faces.sort(key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
                source_emb = source_face.embedding
                result_emb = result_faces[0].embedding
                similarity = np.dot(source_emb, result_emb)
                sim_percentage = max(0.0, float(similarity)) * 100
                sim_text = f" [similarity: {sim_percentage:.2f}%]"
            else:
                sim_text = " [similarity: failed to detect face]"
                
        print(f"Success! Output saved to {output_path}{sim_text}")

def main():
    state.init()
    
    if not os.path.exists(state.source_path):
        print(f"Error: Source image not found at {state.source_path}")
        sys.exit(1)
        
    if not os.path.exists(state.target_path):
        print(f"Error: Target path not found at {state.target_path}")
        sys.exit(1)
        
    print(f"Loading Source: {state.source_path}")
    source_img = cv2.imread(state.source_path)
    if source_img is None:
        print("Error: Could not read source image.")
        sys.exit(1)
        
    print("Detecting source face...")
    from uniface.modules.detector import detect
    source_faces = detect(source_img)
    if not source_faces:
        print("Error: No face detected in source image.")
        sys.exit(1)
    source_faces.sort(key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
    source_face = source_faces[0]
            
    print(f"Starting Uni-Face Pipeline... Processors: {state.processors}")
    try:
        if os.path.isdir(state.target_path):
            print(f"Batch Processing Directory: {state.target_path}")
            os.makedirs(state.output_path, exist_ok=True)
            valid_exts = ('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi', '.mkv', '.webm')
            target_files = [f for f in os.listdir(state.target_path) if f.lower().endswith(valid_exts)]
            
            if not target_files:
                print("No valid image or video files found in target directory.")
                return
                
            target_in_paths = []
            target_out_paths = []
            for idx, file_name in enumerate(target_files):
                in_path = os.path.join(state.target_path, file_name)
                out_path = os.path.join(state.output_path, file_name)
                if not os.path.exists(out_path):
                    target_in_paths.append(in_path)
                    target_out_paths.append(out_path)
            
            if not target_in_paths:
                print("All files already processed or no valid files found.")
                return
                
            # If batch size >= Threads * 2, and they are images, we can use SwarmEngine
            # We assume all valid_exts are images for simplicity if we don't handle videos here.
            # Wait, the CLI targets could be videos too.
            import mimetypes
            image_ins = []
            image_outs = []
            video_tasks = []
            
            for t_in, t_out in zip(target_in_paths, target_out_paths):
                mime, _ = mimetypes.guess_type(t_in)
                if mime and mime.startswith('image'):
                    image_ins.append(t_in)
                    image_outs.append(t_out)
                else:
                    video_tasks.append((t_in, t_out))
                    
            if len(image_ins) >= state.execution_thread_count * 2:
                print(f"Large image batch detected ({len(image_ins)} images). Using SwarmEngine!")
                from uniface.core.image_service import process_images_swarm
                process_images_swarm(source_face, image_ins, image_outs)
            else:
                for idx, (t_in, t_out) in enumerate(zip(image_ins, image_outs)):
                    print(f"[{idx+1}/{len(image_ins)}] Processing {os.path.basename(t_in)} (Sequential)...")
                    process_single_target(source_face, source_img, t_in, t_out)
                    
            for idx, (v_in, v_out) in enumerate(video_tasks):
                print(f"[{idx+1}/{len(video_tasks)}] Processing Video {os.path.basename(v_in)}...")
                process_single_target(source_face, source_img, v_in, v_out)
                
        else:
            print(f"Processing Target: {state.target_path}")
            process_single_target(source_face, source_img, state.target_path, state.output_path)
            
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
