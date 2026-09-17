import os
import cv2
import numpy as np
from typing import Optional
from uniface.core.logging import get_logger

logger = get_logger(__name__)

def get_letterbox_thumbnail(file_path: str, target_size: int = 384, quality: int = 80) -> Optional[bytes]:
    """
    Generates an on-the-fly thumbnail in memory maintaining the original aspect ratio
    and centering it on a target_size x target_size 1:1 square canvas with black letterbox padding.
    """
    try:
        if not os.path.exists(file_path):
            return None
            
        # Support Unicode/UTF-8 filenames safely on Windows
        data = np.fromfile(file_path, dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if img is None:
            return None
            
        h, w = img.shape[:2]
        if h == 0 or w == 0:
            return None
            
        scale = target_size / max(h, w)
        new_w, new_h = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
        
        interpolation = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR
        resized = cv2.resize(img, (new_w, new_h), interpolation=interpolation)
        
        # Create black square canvas (1:1 aspect ratio)
        padded = np.zeros((target_size, target_size, 3), dtype=np.uint8)
        pad_x = (target_size - new_w) // 2
        pad_y = (target_size - new_h) // 2
        padded[pad_y:pad_y + new_h, pad_x:pad_x + new_w] = resized
        
        # Encode to JPEG in RAM
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), max(10, min(100, quality))]
        success, encoded = cv2.imencode('.jpg', padded, encode_param)
        if success:
            return encoded.tobytes()
    except Exception as e:
        logger.debug(f"Failed to generate letterbox thumbnail for {file_path}: {e}")
    return None
