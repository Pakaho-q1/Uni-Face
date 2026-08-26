import cv2
import os
import queue
import threading
from tqdm import tqdm
from typing import List, Callable, Union, Dict
import numpy as np

from uniface.core.state import state
from uniface.core.swarm import SwarmEngine
from uniface.core.types import Face

def process_images_swarm(
    source_face: Face, 
    target_in_paths: List[str], 
    target_out_paths: List[str], 
    progress_callback: Callable[[int, int, np.ndarray], None] = None,
    cancel_event: threading.Event = None
):
    total = len(target_in_paths)
    if total == 0:
        return
        
    engine = SwarmEngine(max_workers=state.execution_thread_count, queue_size=15)
    engine.start()

    def feed_frames():
        for i, in_path in enumerate(target_in_paths):
            if engine.abort_event.is_set():
                break
            frame = cv2.imread(in_path)
            if frame is not None:
                engine.queues["detect"].put((str(i), source_face, frame))
            else:
                print(f"Warning: Could not read {in_path}")
        
        for _ in range(engine.max_workers):
            engine.queues["detect"].put(None)

    feeder_thread = threading.Thread(target=feed_frames, daemon=True)
    feeder_thread.start()

    with tqdm(total=total, desc="Images (Swarm)") as pbar:
        nones_received = 0
        processed = 0
        
        while nones_received < engine.max_workers:
            if cancel_event and cancel_event.is_set():
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
                except: pass
                
            engine.queues["out"].task_done()
            
    feeder_thread.join()
    engine.stop()
