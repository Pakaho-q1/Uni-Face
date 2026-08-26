import time
import queue
import threading
import logging
from typing import Dict, Any, List

from uniface.core.state import state
from uniface.core.service import service_app

logger = logging.getLogger(__name__)

class SwarmEngine:
    def __init__(self, max_workers: int = 8, queue_size: int = 10):
        self.max_workers = max_workers
        self.queue_size = queue_size
        
        self.queues = {
            "detect": queue.Queue(maxsize=queue_size),
            "swap": queue.Queue(maxsize=queue_size),
            "restore": queue.Queue(maxsize=queue_size),
            "color": queue.Queue(maxsize=queue_size),
            "out": queue.Queue(maxsize=queue_size * 2)
        }
        
        self.stage_concurrency = {
            "detect": max(1, max_workers // 2),
            "swap": max(1, max_workers // 2),
            "restore": max(1, max_workers // 2),
            "color": max(1, max_workers // 2)
        }
        
        self.stage_active = {
            "detect": 0,
            "swap": 0,
            "restore": 0,
            "color": 0
        }
        
        self.recovery_mode = {
            "detect": False,
            "swap": False,
            "restore": False,
            "color": False
        }
        
        self.slot_cond = threading.Condition()
        self.abort_event = threading.Event()
        self.threads: List[threading.Thread] = []
        self.processors = state.processors.copy()

    def wait_for_slot(self, stage: str) -> bool:
        with self.slot_cond:
            while True:
                if self.abort_event.is_set():
                    return False
                if self.stage_active[stage] < self.stage_concurrency.get(stage, 1):
                    self.stage_active[stage] += 1
                    return True
                self.slot_cond.wait(timeout=1.0)

    def release_slot(self, stage: str):
        with self.slot_cond:
            self.stage_active[stage] = max(0, self.stage_active[stage] - 1)
            self.slot_cond.notify_all()

    def _forward_none(self, from_stage: str):
        """Forward a single poison-pill None to the next stage in the pipeline.

        Termination chain analysis (invariant: feeder sends exactly `max_workers` Nones):
          - Feeder → detect queue:   max_workers Nones
          - Each detect worker gets 1 None → calls _forward_none("detect") once → swap queue: max_workers Nones
          - Each swap worker gets 1 None   → calls _forward_none("swap") once   → restore queue: max_workers Nones
          - Each restore worker gets 1 None → calls _forward_none("restore") once → color queue: max_workers Nones
          - Each color worker gets 1 None  → puts 1 None in out queue directly  → out queue: max_workers Nones
          - Collector counts max_workers Nones from out queue → terminates ✓

        IMPORTANT: if you add or remove a stage, make sure _forward_none and the
        collector's termination condition (nones_received < engine.max_workers) stay in sync.
        """
        if from_stage == "detect":
            if 'swap' in self.processors: self.queues["swap"].put(None)
            elif 'restore' in self.processors: self.queues["restore"].put(None)
            elif 'color' in self.processors: self.queues["color"].put(None)
            else: self.queues["out"].put(None)
        elif from_stage == "swap":
            if 'restore' in self.processors: self.queues["restore"].put(None)
            elif 'color' in self.processors: self.queues["color"].put(None)
            else: self.queues["out"].put(None)
        elif from_stage == "restore":
            if 'color' in self.processors: self.queues["color"].put(None)
            else: self.queues["out"].put(None)

    def worker_detect(self):
        while not self.abort_event.is_set():
            if not self.wait_for_slot("detect"): break
            try:
                task = self.queues["detect"].get(timeout=1.0)
                if task is None:
                    self._forward_none("detect")
                    break
                
                frame_idx, source_data, frame = task
                try:
                    source_face, target_face = service_app.run_detect(source_data, frame, verbose=False)
                    if source_face is None or target_face is None:
                        self.queues["out"].put((frame_idx, frame))
                    else:
                        if 'swap' in self.processors:
                            self.queues["swap"].put((frame_idx, source_face, target_face, frame))
                        elif 'restore' in self.processors:
                            self.queues["restore"].put((frame_idx, target_face, frame, frame))
                        elif 'color' in self.processors:
                            self.queues["color"].put((frame_idx, target_face, frame, frame))
                        else:
                            self.queues["out"].put((frame_idx, frame))
                except Exception as e:
                    logger.error(f"Detect failed: {e}")
                    self.queues["out"].put((frame_idx, frame))
                self.queues["detect"].task_done()
            except queue.Empty:
                pass
            finally:
                self.release_slot("detect")

    def worker_swap(self):
        while not self.abort_event.is_set():
            if not self.wait_for_slot("swap"): break
            try:
                task = self.queues["swap"].get(timeout=1.0)
                if task is None:
                    self._forward_none("swap")
                    break
                
                frame_idx, source_face, target_face, frame = task
                try:
                    res_frame = service_app.run_swap(source_face, target_face, frame.copy())
                    
                    if 'restore' in self.processors:
                        self.queues["restore"].put((frame_idx, target_face, res_frame, frame))
                    elif 'color' in self.processors:
                        self.queues["color"].put((frame_idx, target_face, res_frame, frame))
                    else:
                        self.queues["out"].put((frame_idx, res_frame))
                except Exception as e:
                    logger.error(f"Swap failed: {e}")
                    self.queues["out"].put((frame_idx, frame))
                self.queues["swap"].task_done()
            except queue.Empty:
                pass
            finally:
                self.release_slot("swap")

    def worker_restore(self):
        while not self.abort_event.is_set():
            if not self.wait_for_slot("restore"): break
            try:
                task = self.queues["restore"].get(timeout=1.0)
                if task is None:
                    self._forward_none("restore")
                    break
                
                frame_idx, target_face, current_frame, orig_frame = task
                try:
                    res_frame = service_app.run_restore(target_face, current_frame, verbose=False)
                    if 'color' in self.processors:
                        self.queues["color"].put((frame_idx, target_face, res_frame, orig_frame))
                    else:
                        self.queues["out"].put((frame_idx, res_frame))
                except Exception as e:
                    logger.error(f"Restore failed: {e}")
                    self.queues["out"].put((frame_idx, orig_frame))
                self.queues["restore"].task_done()
            except queue.Empty:
                pass
            finally:
                self.release_slot("restore")
                
    def worker_color(self):
        while not self.abort_event.is_set():
            if not self.wait_for_slot("color"): break
            try:
                task = self.queues["color"].get(timeout=1.0)
                if task is None:
                    self.queues["out"].put(None)
                    break
                
                frame_idx, target_face, current_frame, orig_frame = task
                try:
                    res_frame = service_app.run_color(target_face, current_frame, orig_frame, verbose=False)
                    self.queues["out"].put((frame_idx, res_frame))
                except Exception as e:
                    logger.error(f"Color failed: {e}")
                    self.queues["out"].put((frame_idx, orig_frame))
                self.queues["color"].task_done()
            except queue.Empty:
                pass
            finally:
                self.release_slot("color")

    def tuner_loop(self):
        # A dynamic tuner based on queue pressure and hysteresis (recovery mode)
        while not self.abort_event.is_set():
            sizes = {
                "detect": self.queues["detect"].qsize(),
                "swap": self.queues["swap"].qsize(),
                "restore": self.queues["restore"].qsize() if 'restore' in self.processors else 0,
                "color": self.queues["color"].qsize() if 'color' in self.processors else 0
            }
            
            with self.slot_cond:
                for s in self.stage_concurrency:
                    # 1. Update Hysteresis State (Recovery Mode)
                    # If tank is nearly full (>= queue_size - 1), enter recovery
                    if sizes[s] >= self.queue_size - 1:
                        self.recovery_mode[s] = True
                    # If tank is drained to <= 3, exit recovery
                    elif sizes[s] <= 3:
                        self.recovery_mode[s] = False
                        
                    # 2. Apply Self-Throttling based on Recovery Mode
                    if self.recovery_mode[s]:
                        # Reduce own power to half
                        self.stage_concurrency[s] = max(1, self.max_workers // 2)
                    else:
                        # Normal condition: full power
                        self.stage_concurrency[s] = self.max_workers
                        
                # 3. Downstream Backpressure (Cascading)
                # We still need upstream stages to slow down if downstream is struggling
                if sizes["detect"] > int(self.queue_size * 0.7):
                    self.stage_concurrency["detect"] = 1
                    
                if sizes["swap"] > int(self.queue_size * 0.7):
                    self.stage_concurrency["detect"] = 1
                    if 'restore' in self.processors:
                        # Give restore a boost to clear the bottleneck faster
                        self.stage_concurrency["restore"] = self.max_workers
                        
                if 'restore' in self.processors and sizes["restore"] > int(self.queue_size * 0.7):
                    self.stage_concurrency["detect"] = 1
                    self.stage_concurrency["swap"] = max(1, self.max_workers // 4)
                    if 'color' in self.processors:
                        self.stage_concurrency["color"] = self.max_workers
                        
                if 'color' in self.processors and sizes["color"] > int(self.queue_size * 0.7):
                    self.stage_concurrency["detect"] = 1
                    self.stage_concurrency["swap"] = 1
                    self.stage_concurrency["restore"] = max(1, self.max_workers // 4)
                        
                self.slot_cond.notify_all()
                
            time.sleep(0.5)

    def start(self):
        # Pre-allocate workers per stage
        for _ in range(self.max_workers):
            self.threads.append(threading.Thread(target=self.worker_detect, daemon=True))
            if 'swap' in self.processors:
                self.threads.append(threading.Thread(target=self.worker_swap, daemon=True))
            if 'restore' in self.processors:
                self.threads.append(threading.Thread(target=self.worker_restore, daemon=True))
            if 'color' in self.processors:
                self.threads.append(threading.Thread(target=self.worker_color, daemon=True))
                
        self.threads.append(threading.Thread(target=self.tuner_loop, daemon=True))
        
        for t in self.threads:
            t.start()

    def stop(self):
        self.abort_event.set()
        with self.slot_cond:
            self.slot_cond.notify_all()
        for t in self.threads:
            if t.is_alive():
                t.join(timeout=1.0)
