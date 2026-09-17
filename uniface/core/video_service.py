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
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Union, Dict, Optional, Callable

from uniface.core.service import process_image
from uniface.core.config import ROOT_DIR, MODEL_PATHS
from uniface.core.state import state
from uniface.core.types import Face, JobConfig
from uniface.core.logging import get_logger

logger = get_logger(__name__)

# Use bundled ffmpeg/ffprobe when available; fall back to system PATH binaries.
_bundled_ffmpeg = Path(str(MODEL_PATHS.get("ffmpeg", "")))
if _bundled_ffmpeg.exists():
    FFMPEG_BIN = str(_bundled_ffmpeg)
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

def create_ffmpeg_encoder(
    output_path: str, 
    width: int, 
    height: int, 
    fps: float, 
    encoder: str = "libx264",
    audio_path: Optional[str] = None
) -> subprocess.Popen:
    """Create FFmpeg rawvideo pipe encoder writing directly to MP4 container with optional real-time audio."""
    # Hardware NVENC requires minimum 145x145 dimensions
    if encoder == "h264_nvenc" and (width < 145 or height < 145):
        logger.info(f"Dimensions {width}x{height} below NVENC minimum (145x145), using libx264.")
        encoder = "libx264"

    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "bgr24",
        "-r", str(fps),
        "-i", "-"
    ]
    if audio_path and os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
        cmd.extend([
            "-i", audio_path,
            "-c:a", "aac",
            "-shortest"
        ])

    cmd.extend([
        "-c:v", encoder,
        "-pix_fmt", "yuv420p",
        "-movflags", "+frag_keyframe+empty_moov+default_base_moof",
        "-f", "mp4",
        output_path
    ])
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time
        time.sleep(0.02)
        if proc.poll() is not None:
            if encoder != "libx264":
                logger.warning(f"Encoder {encoder} failed to start (exit code {proc.poll()}), falling back to libx264...")
                idx = cmd.index("-c:v")
                cmd[idx + 1] = "libx264"
                return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                logger.error("FFmpeg encoder failed to start.")
        return proc
    except Exception as e:
        if encoder != "libx264":
            logger.warning(f"Failed to start encoder {encoder} ({e}), falling back to libx264...")
            idx = cmd.index("-c:v")
            cmd[idx + 1] = "libx264"
            return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        raise

def stream_existing_frames_to_encoder(
    source_video: str, 
    num_frames: int, 
    writer_proc: subprocess.Popen, 
    width: int, 
    height: int
) -> int:
    """
    Stream exactly num_frames from source_video directly into writer_proc.stdin in RAM.
    Zero re-swapping, zero disk I/O bottleneck!
    """
    if not os.path.exists(source_video) or num_frames <= 0:
        return 0
    cmd = [
        FFMPEG_BIN, "-i", source_video,
        "-vframes", str(num_frames),
        "-f", "rawvideo",
        "-pix_fmt", "bgr24",
        "-"
    ]
    frame_bytes = width * height * 3
    stream_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    streamed = 0
    try:
        while streamed < num_frames:
            buf = stream_proc.stdout.read(frame_bytes)
            if not buf or len(buf) < frame_bytes:
                break
            try:
                writer_proc.stdin.write(buf)
            except (BrokenPipeError, OSError) as e:
                logger.warning(f"Pipe error writing existing frame: {e}")
                break
            streamed += 1
    except Exception as e:
        logger.warning(f"Error transferring existing frames: {e}")
    finally:
        if stream_proc.stdout:
            stream_proc.stdout.close()
        try:
            stream_proc.wait(timeout=5)
        except Exception:
            stream_proc.kill()
    return streamed

def process_video(
    source: Union[np.ndarray, Face, Dict], 
    target_video_path: str, 
    output_video_path: str,
    progress_callback: Optional[Callable[[int, int, np.ndarray], None]] = None,
    cancel_event: Optional[threading.Event] = None,
    skip_existing: bool = True,
    job_config: Optional[JobConfig] = None,
    job_temp_dir: Optional[str] = None
):
    cfg = job_config or JobConfig.from_state(state)
    if not os.path.exists(target_video_path):
        raise FileNotFoundError(f"Target video not found: {target_video_path}")
        
    out_dir = os.path.dirname(output_video_path)
    final_file_name = os.path.basename(output_video_path)
    base_name, ext = os.path.splitext(final_file_name)
    if not ext:
        ext = ".mp4"
        output_video_path += ext
        final_file_name += ext

    # User requirement:
    # 1.1: Active working file is temp_<file_name>.mp4
    # 1.2: Retrying working file is retry_<file_name>.mp4
    # 1.3: Completed working file is <file_name>.mp4
    temp_output_path = os.path.join(out_dir, f"temp_{final_file_name}")
    retry_output_path = os.path.join(out_dir, f"retry_{final_file_name}")

    # 1.4: Job internal data strictly in jobs/<job_id>/temp/<base_name> (NOT in outputs/<job_id>/)
    if job_temp_dir:
        session_temp_dir = os.path.join(job_temp_dir, base_name)
    else:
        session_temp_dir = os.path.join(out_dir, ".temp", base_name)

    temp_audio = os.path.join(session_temp_dir, "audio.aac")
    meta_json = os.path.join(session_temp_dir, "meta.json")

    os.makedirs(session_temp_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    
    try:
        audio_exists = has_audio(target_video_path)
        
        # 1. Extract audio if exists into session_temp_dir
        if audio_exists and not os.path.exists(temp_audio):
            logger.info("Extracting audio from target video...")
            subprocess.run([
                FFMPEG_BIN, "-y", "-i", target_video_path,
                "-vn", "-acodec", "copy", temp_audio
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if not os.path.exists(temp_audio) or os.path.getsize(temp_audio) == 0:
                subprocess.run([
                    FFMPEG_BIN, "-y", "-i", target_video_path,
                    "-vn", "-c:a", "aac", temp_audio
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
        # 2. Resolve source face / face model once (SSOT)
        from uniface.core.service import resolve_source_face
        if isinstance(source, Face):
            source_face = source
        elif isinstance(source, dict) and "embeddings" in source:
            source_face = source
        else:
            logger.info("Resolving source face...")
            source_face = resolve_source_face(source, cfg)
            if not source_face:
                logger.error("No source face detected in source image")
                raise ValueError("No source face detected in source image")
        
        # 3. Read video metadata
        cap = cv2.VideoCapture(target_video_path)
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 25.0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        if total_frames <= 0 or width <= 0 or height <= 0:
            logger.error(f"Invalid target video dimensions ({width}x{height}) or frame count ({total_frames}).")
            raise ValueError(f"Invalid target video dimensions ({width}x{height}) or frame count ({total_frames})")

        # 4. Check existing progress for Retry / Resume
        start_frame_idx = 1
        prev_done = 0
        if os.path.exists(meta_json):
            try:
                with open(meta_json, 'r') as f:
                    meta = json.load(f)
                prev_done = meta.get("frames_done", 0)
            except Exception as e:
                logger.debug(f"Failed to read meta.json: {e}")

        # If previous complete final output file already exists and skip_existing is True
        if skip_existing and os.path.exists(output_video_path) and os.path.getsize(output_video_path) > 0 and not os.path.exists(temp_output_path):
            logger.info(f"Output video already completely exists: {output_video_path}")
            return output_video_path

        # Determine if we can resume from existing frames
        resuming = False
        partial_source_video = None
        if skip_existing and prev_done > 0 and prev_done < total_frames:
            if os.path.exists(temp_output_path) and os.path.getsize(temp_output_path) > 0:
                partial_source_video = temp_output_path
            elif os.path.exists(output_video_path) and os.path.getsize(output_video_path) > 0:
                partial_source_video = output_video_path

        encoder_target = temp_output_path
        if partial_source_video is not None:
            resuming = True
            encoder_target = retry_output_path

        logger.info(f"Opening in-memory FFmpeg stream (Encoder: {cfg.video_encoder}, {width}x{height} @ {fps:.2f}fps)...")
        audio_for_encoder = temp_audio if (audio_exists and os.path.exists(temp_audio) and os.path.getsize(temp_audio) > 0) else None
        writer_proc = create_ffmpeg_encoder(encoder_target, width, height, fps, cfg.video_encoder, audio_path=audio_for_encoder)

        if resuming and partial_source_video is not None:
            logger.info(f"[RESUME] Fast-streaming {prev_done} already completed frames directly into {os.path.basename(encoder_target)}...")
            transferred = stream_existing_frames_to_encoder(partial_source_video, prev_done, writer_proc, width, height)
            start_frame_idx = transferred + 1
            logger.info(f"[RESUME] Resuming swap starting from frame {start_frame_idx}/{total_frames} (Skipped {transferred} frames!)")

        interrupted = False
        next_write_idx = start_frame_idx
        
        # Warmup models on first pending frame
        if start_frame_idx <= total_frames:
            warmup_cap = cv2.VideoCapture(target_video_path)
            if start_frame_idx > 1:
                warmup_cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_idx - 1)
            ret, warmup_frame = warmup_cap.read()
            warmup_cap.release()
            if ret and warmup_frame is not None:
                _ = process_image(source_face, warmup_frame, job_config=cfg, verbose=False)

        try:
            from uniface.core.swarm import SwarmEngine
            import queue
            
            engine = SwarmEngine(max_workers=cfg.execution_thread_count, queue_size=15, job_config=cfg)
            engine.start()

            # Feeder thread: read from target video in RAM, push to Swarm
            def feed_frames():
                f_cap = cv2.VideoCapture(target_video_path)
                if start_frame_idx > 1:
                    f_cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_idx - 1)
                
                for f_idx in range(start_frame_idx, total_frames + 1):
                    if engine.abort_event.is_set() or (cancel_event and cancel_event.is_set()):
                        break
                    f_ret, f_mat = f_cap.read()
                    if not f_ret or f_mat is None:
                        break
                    if not engine.safe_put("detect", (f_idx, source_face, f_mat)):
                        break
                f_cap.release()

                for _ in range(engine.max_workers):
                    if engine.abort_event.is_set() or (cancel_event and cancel_event.is_set()):
                        break
                    if not engine.safe_put("detect", None):
                        break

            feeder_thread = threading.Thread(target=feed_frames, daemon=True)
            feeder_thread.start()

            # Collector loop: receive swapped frames, guarantee chronological order, stream into FFmpeg stdin
            pending_frames_map = {}
            with tqdm(total=total_frames, initial=start_frame_idx - 1, desc="Frames (Swarm Stream)") as pbar:
                nones_received = 0
                while nones_received < engine.max_workers:
                    if cancel_event and cancel_event.is_set():
                        raise KeyboardInterrupt("Cancelled via API")
                        
                    try:
                        result = engine.queues["out"].get(timeout=0.5)
                    except queue.Empty:
                        continue
                        
                    if result is None:
                        nones_received += 1
                        engine.queues["out"].task_done()
                        continue
                        
                    f_idx, res_frame = result
                    pending_frames_map[f_idx] = res_frame
                    engine.queues["out"].task_done()
                    
                    while next_write_idx in pending_frames_map:
                        out_mat = pending_frames_map.pop(next_write_idx)
                        try:
                            writer_proc.stdin.write(out_mat.tobytes())
                        except (BrokenPipeError, OSError) as e:
                            logger.error(f"FFmpeg stdin pipe closed or broken ({e}). Encoding aborted.")
                            raise
                            
                        pbar.update(1)
                        
                        if progress_callback:
                            try:
                                progress_callback(next_write_idx, total_frames, out_mat)
                            except Exception as e:
                                logger.debug(f"Video progress callback error: {e}")
                                
                        next_write_idx += 1
                        
                        if next_write_idx % 20 == 0:
                            with open(meta_json, 'w') as f:
                                json.dump({"total_frames": total_frames, "fps": fps, "width": width, "height": height, "frames_done": next_write_idx - 1}, f)

            engine.stop()
            if feeder_thread.is_alive():
                feeder_thread.join(timeout=1.0)

        except KeyboardInterrupt:
            interrupted = True
            if 'engine' in locals():
                engine.stop()
            if 'feeder_thread' in locals() and feeder_thread.is_alive():
                feeder_thread.join(timeout=1.0)
            logger.warning("Video processing interrupted by user. Finalizing partial stream...")

        # 5. Flush and close FFmpeg encoder
        if writer_proc.stdin:
            try:
                writer_proc.stdin.close()
            except Exception:
                pass
        try:
            writer_proc.wait(timeout=30)
        except Exception:
            writer_proc.kill()

        frames_completed = next_write_idx - 1
        with open(meta_json, 'w') as f:
            json.dump({
                "total_frames": total_frames, 
                "fps": fps, 
                "width": width, 
                "height": height, 
                "frames_done": frames_completed
            }, f)

        # 6. Finalize output files
        if resuming:
            # writer_proc was writing to retry_output_path
            if os.path.exists(temp_output_path):
                try:
                    os.remove(temp_output_path)
                except Exception as e:
                    logger.debug(f"Error removing old temp: {e}")

            if interrupted:
                # Cancelled during retry: rename retry_ -> temp_ so it is ready for next resume
                if os.path.exists(retry_output_path):
                    os.rename(retry_output_path, temp_output_path)
                logger.info(f"Interrupted during retry. Playable partial output saved to: {temp_output_path}")
                return temp_output_path
            else:
                # 100% Completed: rename retry_ -> output_video_path (strip temp_/retry_)
                if os.path.exists(output_video_path):
                    try:
                        os.remove(output_video_path)
                    except Exception:
                        pass
                if os.path.exists(retry_output_path):
                    os.rename(retry_output_path, output_video_path)
                logger.info(f"Video processing complete: {output_video_path}")
                shutil.rmtree(session_temp_dir, ignore_errors=True)
                return output_video_path
        else:
            # writer_proc was writing directly to temp_output_path
            if interrupted:
                # Cancelled: temp_output_path is already on disk, intact and playable with audio!
                logger.info(f"Interrupted. Playable partial output saved to: {temp_output_path}")
                return temp_output_path
            else:
                # 100% Completed: rename temp_ -> output_video_path
                if os.path.exists(output_video_path):
                    try:
                        os.remove(output_video_path)
                    except Exception:
                        pass
                if os.path.exists(temp_output_path):
                    os.rename(temp_output_path, output_video_path)
                logger.info(f"Video processing complete: {output_video_path}")
                shutil.rmtree(session_temp_dir, ignore_errors=True)
                return output_video_path

    except Exception as e:
        logger.error(f"Exception during video processing: {e}", exc_info=True)
        raise

