import time
import queue
import threading
import logging
from typing import Dict, Any, List, Optional
import cv2
import numpy as np

from uniface.core.types import Face, JobConfig
from uniface.core.state import state
from uniface.core.service import service_app
from uniface.modules.utils import face_math
from uniface.modules.parser import get_combined_mask

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
        
        # ONNX Runtime InferenceSession.Run() is thread-safe for all providers
        # (CPU, CUDA, TensorRT). No artificial serialization needed here.
        self.stage_concurrency = {
            "detect": max(1, max_workers // 2),
            "swap":   max(1, max_workers // 2),
            "restore": max(1, max_workers // 2),
            "color":  max(1, max_workers // 2)
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

    def safe_put(self, q_name: str, item: Any, timeout: float = 0.2) -> bool:
        """Puts item into specified queue without hanging forever if abort_event is set."""
        while not self.abort_event.is_set():
            try:
                self.queues[q_name].put(item, timeout=timeout)
                return True
            except queue.Full:
                continue
        return False

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

    def _paste_back_final(self, target_face: Face, crop: np.ndarray, affine_matrix: np.ndarray, frame: np.ndarray) -> np.ndarray:
        """Helper to perform single final paste-back to full frame at the end of the pipeline."""
        if crop is None or frame is None or affine_matrix is None:
            return frame

        boost_mode = getattr(self.config, "face_boost", "none")
        if boost_mode in ["256", "512"]:
            boost_size = int(boost_mode)
            scale = boost_size / float(crop.shape[0])
            if scale != 1.0:
                crop = cv2.resize(crop, (boost_size, boost_size), interpolation=cv2.INTER_CUBIC)
            scaled_matrix = affine_matrix.copy() * scale
            crop_mask = get_combined_mask(
                frame, crop, self.config.mask_types, target_face, scaled_matrix,
                mask_padding=getattr(self.config, "mask_padding", None),
                mask_blur=getattr(self.config, "mask_blur", None),
                mask_regions=getattr(self.config, "mask_regions", None),
                target_hair_protect=getattr(self.config, "target_hair_protect", True)
            )
            return face_math.paste_back(frame, crop, crop_mask, scaled_matrix)

        crop_mask = get_combined_mask(
            frame, crop, self.config.mask_types, target_face, affine_matrix,
            mask_padding=getattr(self.config, "mask_padding", None),
            mask_blur=getattr(self.config, "mask_blur", None),
            mask_regions=getattr(self.config, "mask_regions", None),
            target_hair_protect=getattr(self.config, "target_hair_protect", True)
        )
        return face_math.paste_back(frame, crop, crop_mask, affine_matrix)

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
                        # Single-Pass: Warp target face into 512x512 crop once
                        crop_512, affine_matrix = face_math.warp_face_by_face_landmark_5(
                            frame, target_face.landmark_5, 'ffhq_512', (512, 512)
                        )
                        if crop_512 is None or affine_matrix is None:
                            self.queues["out"].put((frame_idx, frame))
                        else:
                            orig_crop = crop_512.copy()
                            if 'swap' in self.processors:
                                self.queues["swap"].put((frame_idx, source_face, target_face, crop_512, orig_crop, affine_matrix, frame))
                            elif 'restore' in self.processors:
                                self.queues["restore"].put((frame_idx, target_face, crop_512, orig_crop, affine_matrix, frame))
                            elif 'color' in self.processors:
                                self.queues["color"].put((frame_idx, target_face, crop_512, orig_crop, affine_matrix, frame))
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
                
                frame_idx, source_face, target_face, crop, orig_crop, affine_matrix, frame = task
                try:
                    from uniface.modules.swapper.swap import swap_crop
                    # Stage 1 Swap in crop space
                    crop = swap_crop(
                        source_face=source_face,
                        crop=crop,
                        swap_model=self.config.swap_model,
                        swap_weight=self.config.swap_weight,
                        target_face=target_face,
                        providers=self.config.providers
                    )
                    
                    # Stage 1 Intermediate Restore (if enabled)
                    if getattr(self.config, "stage1_restore", False):
                        from uniface.modules.restorer import restore_crop
                        eff_blend = (self.config.restore_blend / 100.0) if self.config.restore_blend > 1.0 else self.config.restore_blend
                        crop = restore_crop(
                            crop_image=crop,
                            weight=self.config.restore_weight,
                            blend=eff_blend,
                            restore_model=self.config.restore_model,
                            providers=self.config.providers
                        )
                        
                    # Stage 2 Swap (if dual_swap enabled)
                    if getattr(self.config, "dual_swap", False):
                        crop = swap_crop(
                            source_face=source_face,
                            crop=crop,
                            swap_model=getattr(self.config, "swap_model_2", "hyperswap_high_512"),
                            swap_weight=getattr(self.config, "swap_weight_2", 0.8),
                            target_face=target_face,
                            providers=self.config.providers
                        )
                        
                    # Determine if final restore is needed
                    if getattr(self.config, "dual_swap", False):
                        need_final_restore = getattr(self.config, "stage2_restore", False)
                    else:
                        need_final_restore = (
                            'restore' in self.processors and 
                            not getattr(self.config, "stage1_restore", False) and 
                            getattr(self.config, "face_boost", "none") == "none"
                        )
                        
                    if need_final_restore:
                        self.queues["restore"].put((frame_idx, target_face, crop, orig_crop, affine_matrix, frame))
                    elif 'color' in self.processors:
                        self.queues["color"].put((frame_idx, target_face, crop, orig_crop, affine_matrix, frame))
                    else:
                        res_frame = self._paste_back_final(target_face, crop, affine_matrix, frame)
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
                
                frame_idx, target_face, crop, orig_crop, affine_matrix, frame = task
                try:
                    from uniface.modules.restorer import restore_crop
                    if getattr(self.config, "dual_swap", False):
                        m = getattr(self.config, "restore_model_2", "gfpgan_1.4")
                        w = getattr(self.config, "restore_weight_2", 1.0)
                        b = getattr(self.config, "restore_blend_2", 100)
                    else:
                        m = self.config.restore_model
                        w = self.config.restore_weight
                        b = self.config.restore_blend
                    eff_blend = (b / 100.0) if b > 1.0 else b
                    crop = restore_crop(
                        crop_image=crop,
                        weight=w,
                        blend=eff_blend,
                        restore_model=m,
                        providers=self.config.providers
                    )
                    
                    if 'color' in self.processors:
                        self.queues["color"].put((frame_idx, target_face, crop, orig_crop, affine_matrix, frame))
                    else:
                        res_frame = self._paste_back_final(target_face, crop, affine_matrix, frame)
                        self.queues["out"].put((frame_idx, res_frame))
                except Exception as e:
                    logger.error(f"Restore failed: {e}", exc_info=True)
                    self.queues["out"].put((frame_idx, frame))
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
                
                frame_idx, target_face, crop, orig_crop, affine_matrix, frame = task
                try:
                    from uniface.modules.compositor import compositor_app
                    crop = compositor_app.conditional_match_color(orig_crop, crop)
                    res_frame = self._paste_back_final(target_face, crop, affine_matrix, frame)
                    self.queues["out"].put((frame_idx, res_frame))
                except Exception as e:
                    logger.error(f"Color failed: {e}", exc_info=True)
                    self.queues["out"].put((frame_idx, frame))
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
        # Drain all queues so that any threads waiting on put() or get() unblock instantly
        for q in self.queues.values():
            try:
                while not q.empty():
                    q.get_nowait()
                    q.task_done()
            except Exception:
                pass
        for t in self.threads:
            if t.is_alive():
                t.join(timeout=0.5)
