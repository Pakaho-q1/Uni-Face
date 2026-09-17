from typing import Optional, List, Any
import onnx
from uniface.core.config import MODEL_PATHS
from uniface.core.state import state
from uniface.modules.swapper.base import BaseOnnxSwapper

class Inswapper(BaseOnnxSwapper):
    """
    Native implementation of Inswapper 128.
    """
    def __init__(self, model_key: Optional[str] = None, providers: Optional[List[Any]] = None):
        key = model_key or getattr(state, "swap_model", "inswapper_128")
        if key not in MODEL_PATHS:
            key = "inswapper_128"
            
        super().__init__(
            model_key=key,
            template='arcface_128',
            crop_size=(128, 128),
            mean=[0.0, 0.0, 0.0],
            std=[1.0, 1.0, 1.0],
            providers=providers
        )
        
        # Inswapper requires projecting embedding with model initializer
        model = onnx.load(str(MODEL_PATHS[self.model_key]))
        self.model_initializer = onnx.numpy_helper.to_array(model.graph.initializer[-1])

