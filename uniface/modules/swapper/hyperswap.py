from typing import Optional, List, Any
from uniface.core.config import MODEL_PATHS
from uniface.core.state import state
from uniface.modules.swapper.base import BaseOnnxSwapper

class Hyperswap(BaseOnnxSwapper):
    """
    Native implementation of Hyperswap 256.
    """
    def __init__(self, model_key: Optional[str] = None, providers: Optional[List[Any]] = None):
        key = model_key or getattr(state, "swap_model", "hyperswap_1a_256")
        if key not in MODEL_PATHS:
            key = "hyperswap_1a_256"
            
        super().__init__(
            model_key=key,
            template='ffhq_512',
            crop_size=(256, 256),
            mean=[0.5, 0.5, 0.5],
            std=[0.5, 0.5, 0.5],
            providers=providers
        )

