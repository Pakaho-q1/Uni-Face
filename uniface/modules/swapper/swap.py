import numpy as np
import threading
from typing import Optional, List, Any
from uniface.core.types import Face
from uniface.core.state import state

_swapper_cache = {}
_lock = threading.Lock()

def get_swapper(model_key: Optional[str] = None, providers: Optional[List[Any]] = None):
    model_key = model_key or getattr(state, "swap_model", "inswapper_128")
    cache_key = (model_key, str(providers))
    with _lock:
        if cache_key not in _swapper_cache:
            if 'hyperswap' in model_key:
                from uniface.modules.swapper.hyperswap import Hyperswap
                _swapper_cache[cache_key] = Hyperswap(model_key=model_key, providers=providers)
            else:
                from uniface.modules.swapper.inswapper import Inswapper
                _swapper_cache[cache_key] = Inswapper(model_key=model_key, providers=providers)
        return _swapper_cache[cache_key]

def swap(
    source_face: Face,
    target_face: Face,
    frame: np.ndarray,
    swap_model: Optional[str] = None,
    swap_weight: Optional[float] = None,
    mask_types: Optional[List[str]] = None,
    mask_regions: Optional[List[str]] = None,
    providers: Optional[List[Any]] = None
) -> np.ndarray:
    swapper_instance = get_swapper(model_key=swap_model, providers=providers)
    return swapper_instance.swap(
        source_face=source_face,
        target_face=target_face,
        temp_vision_frame=frame,
        swap_weight=swap_weight,
        mask_types=mask_types,
        mask_regions=mask_regions
    )
