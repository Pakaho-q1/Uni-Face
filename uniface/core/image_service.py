import cv2
import os
import queue
import threading
from tqdm import tqdm
from typing import List, Callable, Union, Dict, Optional
import numpy as np

from uniface.core.state import state
from uniface.core.swarm import SwarmEngine
from uniface.core.types import Face, JobConfig
from uniface.core.logging import get_logger

logger = get_logger(__name__)

def process_images_swarm(
    source_face: Face, 
    target_in_paths: List[str], 
    target_out_paths: List[str], 
    progress_callback: Optional[Callable[[int, int, np.ndarray], None]] = None,
    cancel_event: Optional[threading.Event] = None,
    job_config: Optional[JobConfig] = None
):
    total = len(target_in_paths)
    if total == 0:
        return
        
    cfg = job_config or JobConfig.from_state(state)
    engine = SwarmEngine(max_workers=cfg.execution_thread_count, queue_size=15, job_config=cfg)
    engine.start()

    def feed_frames():
        for i, in_path in enumerate(target_in_paths):
            if engine.abort_event.is_set() or (cancel_event and cancel_event.is_set()):
                break
            frame = cv2.imread(in_path)
            if frame is not None:
                if not engine.safe_put("detect", (str(i), source_face, frame)):
                    break
            else:
                logger.warning(f"Could not read image file: {in_path}")
        
        for _ in range(engine.max_workers):
            if engine.abort_event.is_set() or (cancel_event and cancel_event.is_set()):
                break
            if not engine.safe_put("detect", None):
                break

    feeder_thread = threading.Thread(target=feed_frames, daemon=True)
    feeder_thread.start()

    with tqdm(total=total, desc="Images (Swarm)") as pbar:
        nones_received = 0
        processed = 0
        
        while nones_received < engine.max_workers:
            if cancel_event and cancel_event.is_set():
                logger.info("[SWARM] Image processing cancelled by user, shutting down engine...")
                engine.stop()
                break
                
            try:
                result = engine.queues["out"].get(timeout=0.5)
            except queue.Empty:
                continue
                
            if result is None:
                nones_received += 1
                engine.queues["out"].task_done()
                continue
                
            idx_str, res_frame = result
            idx = int(idx_str)
            out_path = target_out_paths[idx]
            
            cv2.imwrite(out_path, res_frame)
            processed += 1
            
            pbar.update(1)
            
            d_act, d_q = engine.stage_active["detect"], engine.queues["detect"].qsize()
            s_act, s_q = engine.stage_active["swap"], engine.queues["swap"].qsize()
            r_act, r_q = engine.stage_active["restore"], engine.queues["restore"].qsize()
            c_act, c_q = engine.stage_active["color"], engine.queues["color"].qsize()
            pbar.set_postfix_str(f"D:{d_act}/{d_q} S:{s_act}/{s_q} R:{r_act}/{r_q} C:{c_act}/{c_q}")
            
            if progress_callback:
                try:
                    progress_callback(processed, total, res_frame)
                except Exception as e:
                    logger.debug(f"Progress callback raised exception: {e}")
                
            engine.queues["out"].task_done()
            
    engine.stop()
    if feeder_thread.is_alive():
        feeder_thread.join(timeout=1.0)


def get_letterbox_thumbnail(file_path: str, target_size: int = 384, quality: int = 80) -> Optional[bytes]:
    """
    Generates an on-the-fly thumbnail in memory maintaining the original aspect ratio
    and centering it on a target_size x target_size 1:1 square canvas with black letterbox padding.
    """
    try:
        if not os.path.exists(file_path):
            return None
            
        # Support Unicode/UTF-8 filenames safely on Windows
        data = np.fromfile(file_path, dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if img is None:
            return None
            
        h, w = img.shape[:2]
        if h == 0 or w == 0:
            return None
            
        scale = target_size / max(h, w)
        new_w, new_h = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
        
        interpolation = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR
        resized = cv2.resize(img, (new_w, new_h), interpolation=interpolation)
        
        # Create black square canvas (1:1 aspect ratio)
        padded = np.zeros((target_size, target_size, 3), dtype=np.uint8)
        pad_x = (target_size - new_w) // 2
        pad_y = (target_size - new_h) // 2
        padded[pad_y:pad_y + new_h, pad_x:pad_x + new_w] = resized
        
        # Encode to JPEG in RAM
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), max(10, min(100, quality))]
        success, encoded = cv2.imencode('.jpg', padded, encode_param)
        if success:
            return encoded.tobytes()
    except Exception as e:
        logger.debug(f"Failed to generate letterbox thumbnail for {file_path}: {e}")
    return None

