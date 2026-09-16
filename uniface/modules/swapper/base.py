from abc import ABC, abstractmethod
from typing import Optional
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
        
        Args:
            source_face: The Face object representing the identity to be swapped in.
            target_face: The Face object representing the destination face in the frame.
            temp_vision_frame: The full frame image (BGR) containing the target_face.
            swap_weight: Optional weight balance between source and target (0.0 to 1.0).
            mask_types: Optional list of mask types (e.g. ['box', 'occlusion', 'region']).
            mask_regions: Optional list of facial regions for region masking.
            
        Returns:
            np.ndarray: The modified full frame image with the swapped face.
        """
        pass
