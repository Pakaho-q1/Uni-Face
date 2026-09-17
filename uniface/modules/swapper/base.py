import threading
import cv2
from abc import ABC, abstractmethod
from typing import Optional, List, Any
import numpy as np
from uniface.core.types import Face

class BaseSwapper(ABC):
    """
    Abstract interface for all face swapper backends.
    Any new backend (e.g. simswap, hyperswap) must implement this interface.
    """
    
    @abstractmethod
    def swap(
        self,
        source_face: Face,
        target_face: Face,
        temp_vision_frame: np.ndarray,
        swap_weight: Optional[float] = None,
        mask_types: Optional[list[str]] = None,
        mask_regions: Optional[list[str]] = None,
        mask_padding: Optional[list[int]] = None,
        mask_blur: Optional[float] = None,
        clean_source_face: Optional[bool] = None,
        face_boost: Optional[str] = None,
        restore_model: Optional[str] = None,
        restore_weight: Optional[float] = None,
        restore_blend: Optional[float] = None,
        target_hair_protect: Optional[bool] = None
    ) -> np.ndarray:
        """
        Swap the target_face in temp_vision_frame with the source_face.
        """
        pass


class BaseOnnxSwapper(BaseSwapper):
    """
    Common base class for ONNX-based face swappers (Inswapper, Hyperswap, etc.).
    Eliminates duplicated tensor preparation, interpolation blending, Face Boost, and paste-back.
    """
    def __init__(
        self,
        model_key: str,
        template: str,
        crop_size: tuple[int, int],
        mean: list[float],
        std: list[float],
        providers: Optional[list[Any]] = None
    ):
        import onnxruntime
        from uniface.core.config import MODEL_PATHS
        from uniface.core.state import state
        from uniface.core.logging import get_logger
        logger = get_logger(__name__)

        if providers:
            self.providers = [p for p in providers if p is not None]
        else:
            self.providers = [p for p in state.providers if p is not None] if getattr(state, "providers", None) else ["CPUExecutionProvider"]
        if not self.providers:
            self.providers = ["CPUExecutionProvider"]
            
        self.model_key = model_key
        if self.model_key not in MODEL_PATHS:
            raise KeyError(f"Model key '{model_key}' not found in MODEL_PATHS")
            
        model_path = str(MODEL_PATHS[self.model_key])
        provider_names = [p if isinstance(p, str) else p[0] for p in self.providers if p is not None and (isinstance(p, str) or (isinstance(p, (list, tuple)) and len(p) > 0))]
        
        sess_options = getattr(state, "session_options", None)
        self.session = onnxruntime.InferenceSession(model_path, providers=self.providers, sess_options=sess_options)
        logger.debug(f"Loading Swapper Model: {self.model_key} {provider_names} (Active Providers: {self.session.get_providers()})")
        
        self.template = template
        self.crop_size = crop_size
        self.mean = mean
        self.std = std
        self.model_initializer = None

    def _project_embedding(self, balanced_embedding: np.ndarray) -> np.ndarray:
        """Project or normalize embedding according to model requirements."""
        balanced_norm = np.linalg.norm(balanced_embedding)
        if self.model_initializer is not None:
            if balanced_norm > 0:
                return np.dot(balanced_embedding, self.model_initializer) / balanced_norm
            return np.dot(balanced_embedding, self.model_initializer)
        else:
            if balanced_norm > 0:
                return balanced_embedding / balanced_norm
            return balanced_embedding

    def swap_crop(
        self,
        source_face: Face,
        crop_vision_frame: np.ndarray,
        swap_weight: Optional[float] = None,
        target_face: Optional[Face] = None
    ) -> np.ndarray:
        """
        Pure crop-space swapping (SRP compliant).
        Takes source face embedding and target face aligned crop -> returns swapped face crop.
        ONNX Runtime InferenceSession.Run() is thread-safe for all providers (CPU/CUDA/TRT).
        """
        if crop_vision_frame is None or source_face is None or source_face.embedding is None:
            return crop_vision_frame

        from uniface.core.state import state
        if swap_weight is None:
            swap_weight = getattr(state, "swap_weight", 0.65)

        h, w = crop_vision_frame.shape[:2]
        if (w, h) != self.crop_size:
            prep_crop = cv2.resize(crop_vision_frame, self.crop_size, interpolation=cv2.INTER_AREA)
        else:
            prep_crop = crop_vision_frame

        crop_tensor = prep_crop[:, :, ::-1] / 255.0
        crop_tensor = (crop_tensor - self.mean) / self.std
        crop_tensor = crop_tensor.transpose(2, 0, 1)
        crop_tensor = np.expand_dims(crop_tensor, axis=0).astype(np.float32)

        weight = float(np.interp(swap_weight, [0, 1], [0.35, -0.35]))
        source_embedding = source_face.embedding.copy().reshape(1, -1)
        if target_face is not None and getattr(target_face, "embedding", None) is not None and weight != 0:
            target_embedding = target_face.embedding.copy().reshape(1, -1)
            target_norm = np.linalg.norm(target_embedding)
            if target_norm > 0:
                target_embedding = target_embedding / target_norm
            balanced_embedding = source_embedding * (1 - weight) + target_embedding * weight
        else:
            balanced_embedding = source_embedding

        source_embedding_proj = self._project_embedding(balanced_embedding)

        inputs = {
            'source': source_embedding_proj,
            'target': crop_tensor
        }
        swapped_crop = self.session.run(None, inputs)[0][0]

        swapped_crop = swapped_crop.transpose(1, 2, 0)
        swapped_crop = swapped_crop * self.std + self.mean
        swapped_crop = swapped_crop.clip(0, 1)
        swapped_crop = (swapped_crop[:, :, ::-1] * 255.0).astype(np.uint8)

        if (w, h) != self.crop_size:
            swapped_crop = cv2.resize(swapped_crop, (w, h), interpolation=cv2.INTER_CUBIC)

        return swapped_crop

    def swap(
        self,
        source_face: Face,
        target_face: Face,
        temp_vision_frame: np.ndarray,
        swap_weight: Optional[float] = None,
        mask_types: Optional[list[str]] = None,
        mask_regions: Optional[list[str]] = None,
        mask_padding: Optional[list[int]] = None,
        mask_blur: Optional[float] = None,
        clean_source_face: Optional[bool] = None,
        face_boost: Optional[str] = None,
        restore_model: Optional[str] = None,
        restore_weight: Optional[float] = None,
        restore_blend: Optional[float] = None,
        target_hair_protect: Optional[bool] = None
    ) -> np.ndarray:
        import cv2
        from uniface.core.state import state
        from uniface.core.logging import get_logger
        from uniface.modules.utils import face_math
        from uniface.modules.parser import get_combined_mask
        logger = get_logger(__name__)

        if temp_vision_frame is None:
            return temp_vision_frame
            
        if source_face is None or source_face.embedding is None:
            logger.warning(f"{self.__class__.__name__}: Source face or embedding is None.")
            return temp_vision_frame
            
        if target_face is None or not hasattr(target_face, "landmark_5") or target_face.landmark_5 is None:
            logger.warning(f"{self.__class__.__name__}: Target face or landmarks are None.")
            return temp_vision_frame
            
        if swap_weight is None:
            swap_weight = getattr(state, "swap_weight", 0.65)
        if mask_types is None:
            mask_types = getattr(state, "mask_types", ["box"])
            
        # 1. Warp target face
        crop_vision_frame, affine_matrix = face_math.warp_face_by_face_landmark_5(
            temp_vision_frame, 
            target_face.landmark_5, 
            self.template, 
            self.crop_size
        )
        
        if crop_vision_frame is None or affine_matrix is None:
            logger.warning(f"{self.__class__.__name__}: Failed to warp target face.")
            return temp_vision_frame
        
        original_crop_vision_frame = crop_vision_frame.copy()
        
        # Check if target face is close-up/large or touching boundaries
        need_padding = face_math.check_face_needs_padding(target_face, temp_vision_frame.shape)
        if need_padding:
            prep_crop, swap_pad_info = face_math.pad_and_resize_crop(crop_vision_frame, padding_ratio=0.15)
        else:
            prep_crop = crop_vision_frame
            swap_pad_info = (0, 0, 0, 0)
        
        # 2. Swap crop using pure swap_crop
        swapped_crop = self.swap_crop(
            source_face=source_face,
            crop_vision_frame=prep_crop,
            swap_weight=swap_weight,
            target_face=target_face
        )
        
        # Reverse adaptive padding if applied
        if swap_pad_info != (0, 0, 0, 0):
            swapped_crop = face_math.unpad_crop(swapped_crop, swap_pad_info, self.crop_size)
            if swapped_crop.dtype != np.uint8:
                swapped_crop = np.clip(swapped_crop, 0, 255).astype(np.uint8)
        
        # 6. Check Face Boost (in-crop enhancement & scaled paste-back)
        boost_mode = face_boost or getattr(state, "face_boost", "none")
        if boost_mode in ["256", "512"]:
            boost_size = int(boost_mode)
            scale = boost_size / float(self.crop_size[0])
            
            if scale != 1.0:
                boosted_crop = cv2.resize(swapped_crop, (boost_size, boost_size), interpolation=cv2.INTER_CUBIC)
            else:
                boosted_crop = swapped_crop.copy()
            
            # Apply in-crop restoration if a restorer is configured
            eff_restore_model = restore_model or getattr(state, "restore_model", "gfpgan_1.4")
            if eff_restore_model and eff_restore_model != "none":
                from uniface.modules.restorer import restore_crop
                eff_weight = restore_weight if restore_weight is not None else getattr(state, "restore_weight", 1.0)
                eff_blend = (restore_blend / 100.0) if (restore_blend is not None and restore_blend > 1.0) else (restore_blend if restore_blend is not None else getattr(state, "restore_blend", 100) / 100.0)
                boosted_crop = restore_crop(
                    boosted_crop, 
                    weight=eff_weight, 
                    blend=eff_blend, 
                    restore_model=eff_restore_model, 
                    providers=self.providers,
                    padding_ratio=0.15 if need_padding else 0.0
                )
                
            # Scaled affine matrix (local copy, target_face.landmark_5 remains completely untouched!)
            scaled_affine_matrix = affine_matrix.copy() * scale
            
            crop_mask = get_combined_mask(
                temp_vision_frame, 
                boosted_crop, 
                mask_types, 
                target_face, 
                scaled_affine_matrix, 
                mask_padding=mask_padding, 
                mask_blur=mask_blur, 
                mask_regions=mask_regions,
                target_hair_protect=target_hair_protect
            )
            
            return face_math.paste_back(temp_vision_frame, boosted_crop, crop_mask, scaled_affine_matrix)

        # Standard paste-back
        crop_mask = get_combined_mask(
            temp_vision_frame, 
            original_crop_vision_frame, 
            mask_types, 
            target_face, 
            affine_matrix, 
            mask_padding=mask_padding, 
            mask_blur=mask_blur, 
            mask_regions=mask_regions,
            target_hair_protect=target_hair_protect
        )
        
        return face_math.paste_back(temp_vision_frame, swapped_crop, crop_mask, affine_matrix)
