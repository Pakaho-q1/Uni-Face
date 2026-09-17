import numpy as np
from typing import Optional, List, Any
from uniface.core.types import Face
from uniface.core.logging import get_logger
from uniface.modules.utils import face_math

logger = get_logger(__name__)

def enhance_source_face_embedding(
    source_img: np.ndarray,
    face: Face,
    restore_model: str = "gfpgan_1.4",
    restore_weight: float = 0.8,
    providers: Optional[List[Any]] = None
) -> Optional[np.ndarray]:
    """
    Enhance face crop via Restorer (GFPGAN/GPEN) and extract high-quality ArcFace embedding.
    Single Source of Truth (SSOT) shared by FaceService and FaceModelsRouter.
    """
    if source_img is None or face is None or getattr(face, "landmark_5", None) is None:
        return None

    try:
        from uniface.modules.restorer import restore_crop
        src_crop, _ = face_math.warp_face_by_face_landmark_5(
            source_img, face.landmark_5, 'ffhq_512', (512, 512)
        )
        if src_crop is None:
            return None

        need_padding = face_math.check_face_needs_padding(face, source_img.shape)
        pad_ratio = 0.15 if need_padding else 0.0

        enhanced_src = restore_crop(
            src_crop,
            weight=restore_weight,
            blend=1.0,
            restore_model=restore_model,
            providers=providers,
            padding_ratio=pad_ratio
        )

        from uniface.modules.detector import get_detector
        det_inst = get_detector()
        new_emb = det_inst._calculate_embedding(
            enhanced_src, face_math.WARP_TEMPLATE_SET['ffhq_512'] * 512.0
        )
        if new_emb is not None:
            face.embedding = new_emb
            return new_emb
    except Exception as e:
        logger.debug(f"enhance_source_face_embedding skipped: {e}")

    return getattr(face, "embedding", None)
