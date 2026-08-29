import time
import queue
import threading
import logging
from typing import Dict, Any, List, Optional

from uniface.core.types import JobConfig
from uniface.core.state import state
from uniface.core.service import service_app

logger = logging.getLogger(__name__)

class SwarmEngine:
    def __init__(self, max_workers: int = 8, queue_size: int = 10, job_config: Optional[JobConfig] = None):
        self.max_workers = max_workers
        self.queue_size = queue_size
        self.config = job_config or JobConfig.from_state(state)
        
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
        self.processors = self.config.processors.copy()

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
        """Forward a single poison-pill None to the next stage in the pipeline."""
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
                    source_face, target_face = service_app.run_detect(source_data, frame, job_config=self.config, verbose=False)
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
                    logger.error(f"Detect failed: {e}", exc_info=True)
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
                    res_frame = service_app.run_swap(source_face, target_face, frame.copy(), job_config=self.config)
                    
                    if 'restore' in self.processors:
                        self.queues["restore"].put((frame_idx, target_face, res_frame, frame))
                    elif 'color' in self.processors:
                        self.queues["color"].put((frame_idx, target_face, res_frame, frame))
                    else:
                        self.queues["out"].put((frame_idx, res_frame))
                except Exception as e:
                    logger.error(f"Swap failed: {e}", exc_info=True)
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
                    res_frame = service_app.run_restore(target_face, current_frame, job_config=self.config, verbose=False)
                    if 'color' in self.processors:
                        self.queues["color"].put((frame_idx, target_face, res_frame, orig_frame))
                    else:
                        self.queues["out"].put((frame_idx, res_frame))
                except Exception as e:
                    logger.error(f"Restore failed: {e}", exc_info=True)
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
                    res_frame = service_app.run_color(target_face, current_frame, orig_frame, job_config=self.config, verbose=False)
                    self.queues["out"].put((frame_idx, res_frame))
                except Exception as e:
                    logger.error(f"Color failed: {e}", exc_info=True)
                    self.queues["out"].put((frame_idx, orig_frame))
                self.queues["color"].task_done()
            except queue.Empty:
                pass
            finally:
                self.release_slot("color")

    def tuner_loop(self):
        while not self.abort_event.is_set():
            sizes = {
                "detect": self.queues["detect"].qsize(),
                "swap": self.queues["swap"].qsize(),
                "restore": self.queues["restore"].qsize() if 'restore' in self.processors else 0,
                "color": self.queues["color"].qsize() if 'color' in self.processors else 0
            }
            
            with self.slot_cond:
                for s in self.stage_concurrency:
                    if sizes[s] >= self.queue_size - 1:
                        self.recovery_mode[s] = True
                    elif sizes[s] <= 3:
                        self.recovery_mode[s] = False
                        
                    if self.recovery_mode[s]:
                        self.stage_concurrency[s] = max(1, self.max_workers // 2)
                    else:
                        self.stage_concurrency[s] = self.max_workers
                        
                if sizes["detect"] > int(self.queue_size * 0.7):
                    self.stage_concurrency["detect"] = 1
                    
                if sizes["swap"] > int(self.queue_size * 0.7):
                    self.stage_concurrency["detect"] = 1
                    if 'restore' in self.processors:
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
