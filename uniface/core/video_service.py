import cv2
import os
import subprocess
import tempfile
from tqdm import tqdm
import shutil
import sys
import numpy as np
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from uniface.core.service import process_image
from uniface.core.config import ROOT_DIR, MODEL_PATHS
from uniface.core.state import state
from uniface.core.types import Face
from typing import Union, Dict

# Use bundled ffmpeg/ffprobe when available; fall back to system PATH binaries.
# MODEL_PATHS["ffmpeg"] points to models/ffmpeg.exe on Windows.
_bundled_ffmpeg = Path(str(MODEL_PATHS.get("ffmpeg", "")))
if _bundled_ffmpeg.exists():
    FFMPEG_BIN = str(_bundled_ffmpeg)
    # ffprobe lives alongside ffmpeg in the same directory
    _ffprobe_candidate = _bundled_ffmpeg.parent / (_bundled_ffmpeg.stem.replace("ffmpeg", "ffprobe") + _bundled_ffmpeg.suffix)
    FFPROBE_BIN = str(_ffprobe_candidate) if _ffprobe_candidate.exists() else "ffprobe"
else:
    FFMPEG_BIN = "ffmpeg"
    FFPROBE_BIN = "ffprobe"

def has_audio(video_path: str) -> bool:
    """Check if a video file has an audio stream."""
    cmd = [
        FFPROBE_BIN, 
        "-i", video_path, 
        "-show_streams", 
        "-select_streams", "a", 
        "-loglevel", "error"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return len(result.stdout.strip()) > 0


from typing import Union, Callable
import threading

def process_video(
    source: Union[np.ndarray, Face, Dict], 
    target_video_path: str, 
    output_video_path: str,
    progress_callback: Callable[[int, int, np.ndarray], None] = None,
    cancel_event: threading.Event = None,
    skip_existing: bool = True
):
    
    if not os.path.exists(target_video_path):
        raise FileNotFoundError(f"Target video not found: {target_video_path}")
        
    temp_dir = os.path.join(os.path.dirname(output_video_path), "temp")
    
    # Create a unique temp folder based on output filename
    base_name = os.path.splitext(os.path.basename(output_video_path))[0]
    session_temp_dir = os.path.join(temp_dir, base_name)
    temp_frames_in_dir = os.path.join(session_temp_dir, "frames_in")
    temp_frames_out_dir = os.path.join(session_temp_dir, "frames_out")
    temp_audio = os.path.join(session_temp_dir, "audio.aac")
    meta_json = os.path.join(session_temp_dir, "meta.json")
    
    # If not skipping existing (e.g. user wants to re-process with new params),
    # clear the output frames directory so they are all re-rendered.
    if not skip_existing and os.path.exists(temp_frames_out_dir):
        shutil.rmtree(temp_frames_out_dir)
        
    os.makedirs(temp_frames_in_dir, exist_ok=True)
    os.makedirs(temp_frames_out_dir, exist_ok=True)
    
    try:
        audio_exists = has_audio(target_video_path)
        
        # 1. Extract audio if exists
        if audio_exists and not os.path.exists(temp_audio):
            print("Extracting audio from target video...")
            subprocess.run([
                FFMPEG_BIN, "-y", "-i", target_video_path,
                "-vn", "-acodec", "copy", temp_audio
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Fallback if original audio codec can't be copied directly to .aac
            if not os.path.exists(temp_audio) or os.path.getsize(temp_audio) == 0:
                 subprocess.run([
                    FFMPEG_BIN, "-y", "-i", target_video_path,
                    "-vn", "-c:a", "aac", temp_audio
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
        # 2. Get/Detect source face ONCE
        if isinstance(source, np.ndarray):
            print("Detecting source face...")
            from uniface.modules.detector import detect
            source_faces = detect(source)
            if not source_faces:
                print("Error: No source face detected!")
                return
            source_faces.sort(key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
            source_face = source_faces[0]
        else:
            source_face = source
        
        # 3. Extract frames
        cap = cv2.VideoCapture(target_video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        
        # Smart Retry Logic: Check if frames already extracted
        need_extract = True
        total_frames = 0
        if os.path.exists(meta_json):
            try:
                with open(meta_json, 'r') as f:
                    meta = json.load(f)
                if meta.get("total_frames", 0) > 0:
                    need_extract = False
                    total_frames = meta["total_frames"]
            except Exception:
                pass
                
        if need_extract:
            print("Extracting frames from target video...")
            extract_cmd = [
                FFMPEG_BIN, "-y", "-i", target_video_path,
                "-q:v", "2",
                os.path.join(temp_frames_in_dir, "%06d.jpg")
            ]
            subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            frame_files = sorted([f for f in os.listdir(temp_frames_in_dir) if f.endswith('.jpg')])
            total_frames = len(frame_files)
            
            if total_frames > 0:
                with open(meta_json, 'w') as f:
                    json.dump({"total_frames": total_frames}, f)
        
        if total_frames == 0:
            print("Error: No frames extracted from video.")
            return
            
        # 4. Prepare pending frames for processing
        pending_frames = []
        for i in range(1, total_frames + 1):
            frame_name = f"{i:06d}.jpg"
            out_path = os.path.join(temp_frames_out_dir, frame_name)
            if not os.path.exists(out_path):
                pending_frames.append(frame_name)
                
        if not pending_frames:
            print("All frames already processed! Skipping directly to merge.")
        else:
            print(f"Processing {len(pending_frames)} pending frames (out of {total_frames}) using {state.execution_thread_count} threads...")
            
            # Warmup/Initialize models sequentially to avoid ONNX Runtime thread-safety issues during initialization
            # Find an available frame for warmup
            warmup_img = None
            if isinstance(source, np.ndarray):
                _ = process_image(source_face, source, verbose=False)
            elif pending_frames:
                for p_frame in pending_frames:
                    p_path = os.path.join(temp_frames_in_dir, p_frame)
                    if os.path.exists(p_path):
                        warmup_img = cv2.imread(p_path)
                        break
                if warmup_img is not None:
                    _ = process_image(source_face, warmup_img, verbose=False)
            
            interrupted = False
            try:
                from uniface.core.swarm import SwarmEngine
                import queue
                import threading
                
                engine = SwarmEngine(max_workers=state.execution_thread_count, queue_size=15)
                engine.start()

                # Feeder thread
                def feed_frames():
                    for frame_file in pending_frames:
                        if engine.abort_event.is_set():
                            break
                        in_path = os.path.join(temp_frames_in_dir, frame_file)
                        if os.path.exists(in_path):
                            frame = cv2.imread(in_path)
                            if frame is not None:
                                engine.queues["detect"].put((frame_file, source_face, frame))
                    # Poison pills to shut down all detect workers
                    for _ in range(engine.max_workers):
                        engine.queues["detect"].put(None)

                feeder_thread = threading.Thread(target=feed_frames, daemon=True)
                feeder_thread.start()

                # Collector loop
                with tqdm(total=len(pending_frames), desc="Frames (Swarm)") as pbar:
                    nones_received = 0
                    while nones_received < engine.max_workers:
                        if cancel_event and cancel_event.is_set():
                            raise KeyboardInterrupt("Cancelled via API")
                            
                        try:
                            result = engine.queues["out"].get(timeout=0.5)
                        except queue.Empty:
                            if not feeder_thread.is_alive() and engine.queues["out"].empty():
                                # Check if any active threads are deadlocked or still processing
                                pass
                            continue
                            
                        if result is None:
                            nones_received += 1
                            engine.queues["out"].task_done()
                            continue
                            
                        frame_file, res_frame = result
                        out_path = os.path.join(temp_frames_out_dir, frame_file)
                        in_path = os.path.join(temp_frames_in_dir, frame_file)
                        cv2.imwrite(out_path, res_frame)
                        try:
                            os.remove(in_path)
                        except Exception:
                            pass
                            
                        pbar.update(1)
                        
                        # Update Swarm Tuner Metrics
                        d_act, d_q = engine.stage_active["detect"], engine.queues["detect"].qsize()
                        s_act, s_q = engine.stage_active["swap"], engine.queues["swap"].qsize()
                        r_act, r_q = engine.stage_active["restore"], engine.queues["restore"].qsize()
                        c_act, c_q = engine.stage_active["color"], engine.queues["color"].qsize()
                        pbar.set_postfix_str(f"D:{d_act}/{d_q} S:{s_act}/{s_q} R:{r_act}/{r_q} C:{c_act}/{c_q}")
                        
                        if progress_callback:
                            try:
                                c = len(os.listdir(temp_frames_out_dir))
                                progress_callback(c, total_frames, res_frame)
                            except: pass
                            
                        engine.queues["out"].task_done()
                        
                feeder_thread.join()
                engine.stop()
                
            except KeyboardInterrupt:
                interrupted = True
                if 'engine' in locals():
                    engine.stop()
                print("\n[!] Processing interrupted by user (Ctrl+C).")
                print("Generating partial video from completed frames...")
                
        # 5. Merge audio and video with NVENC (fallback to libx264)
        print(f"Merging frames into video (Encoder: {state.video_encoder})...")
        
        # Calculate percentage for suffix if interrupted
        final_output_path = output_video_path
        if 'interrupted' in locals() and interrupted:
            processed_count = len([f for f in os.listdir(temp_frames_out_dir) if f.endswith('.jpg')])
            percent = int((processed_count / total_frames) * 100) if total_frames > 0 else 0
            
            base, ext = os.path.splitext(output_video_path)
            final_output_path = f"{base}_{percent}%{ext}"
            print(f"Saving partial output to: {final_output_path}")

        merge_cmd = [
            FFMPEG_BIN, "-y", 
            "-framerate", str(fps),
            "-i", os.path.join(temp_frames_out_dir, "%06d.jpg")
        ]
        
        if audio_exists and os.path.exists(temp_audio) and os.path.getsize(temp_audio) > 0:
            merge_cmd.extend(["-i", temp_audio])
            
        merge_cmd.extend(["-c:v", state.video_encoder, "-pix_fmt", "yuv420p"])
        if audio_exists:
            merge_cmd.extend(["-c:a", "aac", "-shortest"])
            
        merge_cmd.append(final_output_path)
        
        result = subprocess.run(merge_cmd, capture_output=True, text=True)
        
        if result.returncode != 0 and state.video_encoder != "libx264":
            print(f"Warning: Encoder '{state.video_encoder}' failed. Falling back to libx264...")
            fallback_cmd = merge_cmd.copy()
            idx = fallback_cmd.index("-c:v") + 1
            fallback_cmd[idx] = "libx264"
            result = subprocess.run(fallback_cmd, capture_output=True, text=True)
            
        if result.returncode == 0:
            print("Video processing complete!")
            if 'interrupted' in locals() and interrupted:
                print("Temp files preserved for future resume. You can re-run the same command to continue.")
            else:
                print("Cleaning up temp files...")
                shutil.rmtree(session_temp_dir, ignore_errors=True)
        else:
            print("Error: Merging video failed. Temp files are preserved for retry.")
            print(result.stderr)
            
    except Exception as e:
        print(f"Exception during video processing: {e}")
        # DO NOT cleanup temp_dir here so user can resume later!
        raise
