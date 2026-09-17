import cv2
import numpy as np
import onnxruntime
import threading
from typing import Optional, List, Any

from uniface.core.types import Face
from uniface.core.config import MODEL_PATHS
from uniface.core.state import state
from uniface.core.logging import get_logger
from uniface.modules.utils import face_math
from uniface.modules.parser import get_combined_mask

logger = get_logger(__name__)

class FaceRestorer:
    """
    Native implementation for Face Enhancement (Restoration).
    Supports GFPGAN and GPEN.
    """
    def __init__(self, model_key: Optional[str] = None, providers: Optional[List[Any]] = None):
        if providers:
            self.providers = [p for p in providers if p is not None]
        else:
            self.providers = [p for p in state.providers if p is not None] if getattr(state, "providers", None) else ["CPUExecutionProvider"]
        if not self.providers:
            self.providers = ["CPUExecutionProvider"]
            
        model_key = model_key or getattr(state, "restore_model", "gfpgan_1.4")
        if model_key not in MODEL_PATHS:
            model_key = 'gfpgan_1.4'
            
        provider_names = [p if isinstance(p, str) else p[0] for p in self.providers if p is not None and (isinstance(p, str) or (isinstance(p, (list, tuple)) and len(p) > 0))]
        sess_options = getattr(state, "session_options", None)
        self.session = onnxruntime.InferenceSession(str(MODEL_PATHS[model_key]), providers=self.providers, sess_options=sess_options)
        logger.debug(f"Loading Restorer Model: {model_key} {provider_names} (Active Providers: {self.session.get_providers()})")
        
        # Set crop size based on model
        self.template = 'ffhq_512'
        if '256' in model_key:
            self.crop_size = (256, 256)
        elif '1024' in model_key:
            self.crop_size = (1024, 1024)
        else:
            self.crop_size = (512, 512)
            
        # Check if model has a 'weight' input (some enhancers support blending weight)
        self.has_weight = any(inp.name == 'weight' for inp in self.session.get_inputs())
        self.input_name = self.session.get_inputs()[0].name
        self.weight_name = 'weight' if self.has_weight else None



    def restore(
        self,
        target_face: Face,
        temp_vision_frame: np.ndarray,
        weight: float = 0.5,
        blend: float = 0.8,
        mask_types: Optional[List[str]] = None
    ) -> np.ndarray:
        """
        Enhance/restore a face in the full frame.
        """
        if temp_vision_frame is None:
            return temp_vision_frame
            
        if target_face is None or not hasattr(target_face, "landmark_5") or target_face.landmark_5 is None:
            return temp_vision_frame
            
        if mask_types is None:
            mask_types = getattr(state, "mask_types", ["box"])
            
        # 1. Warp face to crop
        crop_vision_frame, affine_matrix = face_math.warp_face_by_face_landmark_5(
            temp_vision_frame, 
            target_face.landmark_5, 
            self.template, 
            self.crop_size
        )
        
        if crop_vision_frame is None or affine_matrix is None:
            return temp_vision_frame
        
        # 2. Check if face is close-up/large or touching boundaries
        need_padding = face_math.check_face_needs_padding(target_face, temp_vision_frame.shape)
        pad_ratio = 0.15 if need_padding else 0.0

        # 3. Enhance crop via restore_crop
        enhanced_crop = self.restore_crop(crop_vision_frame, weight=weight, blend=blend, padding_ratio=pad_ratio)
            
        # 4. Generate precise mask using Parser
        crop_mask = get_combined_mask(temp_vision_frame, crop_vision_frame, mask_types, target_face, affine_matrix)
        
        # 5. Paste back into original frame
        paste_vision_frame = face_math.paste_back(temp_vision_frame, enhanced_crop, crop_mask, affine_matrix)
        return paste_vision_frame

    def restore_crop(
        self,
        crop_image: np.ndarray,
        weight: float = 0.5,
        blend: float = 0.8,
        padding_ratio: float = 0.0
    ) -> np.ndarray:
        """
        Directly enhance an aligned face crop (used by Face Boost and Restore Source Face).
        Supports adaptive padding for close-up/large faces touching boundaries.
        """
        if crop_image is None:
            return crop_image
            
        if crop_image.dtype != np.uint8:
            crop_image = np.clip(crop_image, 0, 255).astype(np.uint8)
            
        h, w = crop_image.shape[:2]
        
        # 1. Apply adaptive padding if requested
        if padding_ratio > 0.0:
            padded_input, pad_info = face_math.pad_and_resize_crop(crop_image, padding_ratio=padding_ratio)
        else:
            padded_input = crop_image
            pad_info = (0, 0, 0, 0)
            
        cur_h, cur_w = padded_input.shape[:2]
        need_resize = (cur_w != self.crop_size[0] or cur_h != self.crop_size[1])
        if need_resize:
            input_crop = cv2.resize(padded_input, self.crop_size, interpolation=cv2.INTER_CUBIC)
        else:
            input_crop = padded_input
            
        prepare_vision_frame = input_crop[:, :, ::-1] / 255.0
        prepare_vision_frame = (prepare_vision_frame - 0.5) / 0.5
        prepare_vision_frame = np.expand_dims(prepare_vision_frame.transpose(2, 0, 1), axis=0).astype(np.float32)
        
        inputs = {self.input_name: prepare_vision_frame}
        if self.has_weight:
            inputs[self.weight_name] = np.array([weight], dtype=np.float64)
            
        enhanced_crop = self.session.run(None, inputs)[0][0]

        enhanced_crop = np.clip(enhanced_crop, -1, 1)
        enhanced_crop = (enhanced_crop + 1) / 2
        enhanced_crop = enhanced_crop.transpose(1, 2, 0)
        enhanced_crop = (enhanced_crop[:, :, ::-1] * 255.0).astype(np.uint8)
        
        if enhanced_crop.shape[:2] != (cur_h, cur_w):
            enhanced_crop = cv2.resize(enhanced_crop, (cur_w, cur_h), interpolation=cv2.INTER_CUBIC)
            
        # 2. Reverse adaptive padding
        if pad_info != (0, 0, 0, 0):
            enhanced_crop = face_math.unpad_crop(enhanced_crop, pad_info, (h, w))
            if enhanced_crop.dtype != np.uint8:
                enhanced_crop = np.clip(enhanced_crop, 0, 255).astype(np.uint8)
            
        if blend < 1.0:
            if crop_image.dtype != enhanced_crop.dtype:
                crop_image = crop_image.astype(enhanced_crop.dtype)
            if crop_image.shape[:2] != enhanced_crop.shape[:2]:
                crop_image = cv2.resize(crop_image, (enhanced_crop.shape[1], enhanced_crop.shape[0]))
            enhanced_crop = cv2.addWeighted(crop_image, 1 - blend, enhanced_crop, blend, 0)
            
        return enhanced_crop

# Thread-safe multi-model cache
_restorer_cache: dict = {}
_lock = threading.Lock()

def get_restorer(restore_model: Optional[str] = None, providers: Optional[List[Any]] = None) -> FaceRestorer:
    model_key = restore_model or getattr(state, "restore_model", "gfpgan_1.4")
    if model_key not in _restorer_cache:
        with _lock:
            if model_key not in _restorer_cache:
                _restorer_cache[model_key] = FaceRestorer(model_key=model_key, providers=providers)
    return _restorer_cache[model_key]

def unload_unused_restorers(keep_models: List[str] = None):
    with _lock:
        if keep_models is None:
            _restorer_cache.clear()
            return
        to_del = [k for k in list(_restorer_cache.keys()) if not any(m in k for m in keep_models)]
        for k in to_del:
            del _restorer_cache[k]

def restore(
    target_face: Face, 
    frame: np.ndarray, 
    weight: Optional[float] = None, 
    blend: Optional[float] = None, 
    restore_model: Optional[str] = None, 
    mask_types: Optional[List[str]] = None,
    providers: Optional[List[Any]] = None
) -> np.ndarray:
    if weight is None:
        weight = getattr(state, "restore_weight", 1.0)
    if blend is None:
        blend = getattr(state, "restore_blend", 100) / 100.0
    if mask_types is None:
        mask_types = getattr(state, "mask_types", ["box"])
        
    restorer_instance = get_restorer(restore_model=restore_model, providers=providers)
    return restorer_instance.restore(target_face, frame, weight, blend, mask_types=mask_types)

def restore_crop(
    crop_image: np.ndarray,
    weight: Optional[float] = None,
    blend: Optional[float] = None,
    restore_model: Optional[str] = None,
    providers: Optional[List[Any]] = None,
    padding_ratio: float = 0.0
) -> np.ndarray:
    if weight is None:
        weight = getattr(state, "restore_weight", 1.0)
    if blend is None:
        blend = getattr(state, "restore_blend", 100) / 100.0
    restorer_instance = get_restorer(restore_model=restore_model, providers=providers)
    return restorer_instance.restore_crop(crop_image, weight=weight, blend=blend, padding_ratio=padding_ratio)


