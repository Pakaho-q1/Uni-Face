import numpy as np
import cv2
import base64
import copy
from typing import Union, Dict, Optional
from uniface.core.types import Face, JobConfig
from uniface.core.state import state
from uniface.core.logging import get_logger

from uniface.modules import detector

def detect(*args, **kwargs):
    return detector.detect(*args, **kwargs)

from uniface.modules.swapper.swap import swap
from uniface.modules.restorer import restore
from uniface.modules.compositor import composite

logger = get_logger(__name__)

def filter_and_sort_target_faces(
    target_faces: list[Face], 
    gender_filter: str = "all", 
    face_order: str = "largest"
) -> list[Face]:
    """
    Filter target faces by gender and sort them according to the selected selection priority.
    """
    if not target_faces:
        return []
        
    candidates = list(target_faces)
    
    # 1. Gender Filter (0 = Female, 1 = Male)
    if gender_filter == "female":
        filtered = [f for f in candidates if f.gender == 0]
        if filtered:
            candidates = filtered
    elif gender_filter == "male":
        filtered = [f for f in candidates if f.gender == 1]
        if filtered:
            candidates = filtered
            
    # 2. Face Selection Order / Strategy
    if face_order == "smallest":
        candidates.sort(key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
    elif face_order == "highest_score":
        candidates.sort(key=lambda x: x.score, reverse=True)
    elif face_order == "left_to_right":
        candidates.sort(key=lambda x: x.bbox[0])
    elif face_order == "right_to_left":
        candidates.sort(key=lambda x: x.bbox[0], reverse=True)
    elif face_order == "top_to_bottom":
        candidates.sort(key=lambda x: x.bbox[1])
    elif face_order == "bottom_to_top":
        candidates.sort(key=lambda x: x.bbox[1], reverse=True)
    else:  # "largest" (default)
        candidates.sort(key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]), reverse=True)
        
    return candidates

_SOURCE_FACE_CACHE: dict[tuple, Face] = {}

def clear_source_face_cache():
    global _SOURCE_FACE_CACHE
    _SOURCE_FACE_CACHE.clear()

def resolve_source_face(
    source: Union[np.ndarray, Face, Dict], 
    job_config: Optional[JobConfig] = None,
    verbose: bool = True
) -> Optional[Face]:
    """
    Resolve, detect, and enhance source face once (SSOT).
    Caches detection on the source ndarray or returns pre-computed Face instances.
    """
    if source is None:
        return None
        
    if isinstance(source, Face):
        return source
        
    if isinstance(source, dict):
        if "embeddings" in source and len(source["embeddings"]) > 0:
            embs = source["embeddings"]
            mean_emb = np.mean(embs, axis=0).astype(np.float32)
            return Face(bbox=np.array([0, 0, 0, 0]), embedding=mean_emb)
        return None

    if isinstance(source, str):
        if os.path.exists(source):
            img = cv2.imread(source)
            if img is not None:
                source = img
            else:
                return None
        else:
            return None
        
    cfg = job_config or JobConfig.from_state(state)
    det_score = getattr(cfg, "face_detector_score", 0.65)
    lm_score = getattr(cfg, "face_landmark_score", 0.50)
    res_src = bool(getattr(cfg, "restore_source_face", False))
    res_model = str(getattr(cfg, "restore_source_face_model", "gfpgan_1.4"))
    res_weight = float(getattr(cfg, "restore_source_face_weight", 0.8))
    
    if isinstance(source, np.ndarray):
        cache_key = (id(source), res_src, res_model, res_weight, det_score, lm_score)
        if cache_key in _SOURCE_FACE_CACHE:
            return _SOURCE_FACE_CACHE[cache_key]

        source_faces = detect(
            source,
            extract_embedding=True,
            extract_gender_age=False,
            detector_score=det_score,
            landmark_score=lm_score,
            clean_source_face=False
        )
        if not source_faces:
            if verbose:
                logger.debug("No face detected in source image.")
            return None
            
        source_faces.sort(key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
        source_face = source_faces[0]

        # ReActor Source Face Enhancement (restore source face before ArcFace embedding)
        if res_src and getattr(source_face, "landmark_5", None) is not None:
            from uniface.modules.utils.face_helpers import enhance_source_face_embedding
            new_emb = enhance_source_face_embedding(
                source, source_face,
                restore_model=res_model,
                restore_weight=res_weight,
                providers=cfg.providers
            )
            if new_emb is not None and verbose:
                logger.debug(f"Source face successfully enhanced with restorer ({res_model}, weight={res_weight}) prior to embedding extraction.")
                
        if len(_SOURCE_FACE_CACHE) > 32:
            _SOURCE_FACE_CACHE.clear()
        _SOURCE_FACE_CACHE[cache_key] = source_face
            
        return source_face
        
    return None

class FaceService:
    def __init__(self):
        pass

    def run_detect(
        self,
        source: Union[np.ndarray, Face, Dict],
        target_img: np.ndarray,
        job_config: Optional[JobConfig] = None,
        verbose: bool = True
    ):
        """
        Detect faces in target and source. Handles dynamic source selection.
        Returns: (source_face, target_face) or (None, None) if detection fails.
        """
        cfg = job_config or JobConfig.from_state(state)
        
        # 1. Detect Target Faces
        need_gender = getattr(cfg, "target_gender", "all") != "all"
        need_ref = bool(getattr(cfg, "reference_face_ids", None))
        need_weight_blend = (getattr(cfg, "swap_weight", 1.0) < 0.99) or (getattr(cfg, "dual_swap", False) and getattr(cfg, "swap_weight_2", 1.0) < 0.99)
        need_embedding = need_ref or (isinstance(source, dict) and "embeddings" in source) or need_weight_blend
        need_gender_age = need_gender
        
        det_score = getattr(cfg, "face_detector_score", 0.65)
        lm_score = getattr(cfg, "face_landmark_score", 0.50)
        
        target_faces = detect(
            target_img,
            extract_embedding=need_embedding,
            extract_gender_age=need_gender_age,
            detector_score=det_score,
            landmark_score=lm_score
        )
        if not target_faces:
            if verbose:
                logger.debug("No face detected in target image.")
            return None, None
            
        target_face = None
        
        # Reference Face Filtering
        ref_embs = cfg.get_reference_embeddings() if hasattr(cfg, "get_reference_embeddings") else []
        if ref_embs:
            best_sim = -1.0
            best_face = None
            
            for face in target_faces:
                if face.embedding is None:
                    continue
                face_norm = face.embedding / (np.linalg.norm(face.embedding) + 1e-8)
                
                for ref_emb in ref_embs:
                    sim = float(np.dot(face_norm, ref_emb))
                    if sim > best_sim:
                        best_sim = sim
                        best_face = face
            
            # Check threshold
            threshold = cfg.reference_threshold
            if best_face is not None and best_sim >= threshold:
                target_face = best_face
            else:
                logger.debug(f"Best face match similarity ({best_sim:.3f}) below threshold ({threshold:.3f})")
                return None, None
                
        if not target_face:
            # Sort & filter target faces based on gender and order strategy
            sorted_faces = filter_and_sort_target_faces(
                target_faces, 
                gender_filter=getattr(cfg, "target_gender", "all"), 
                face_order=getattr(cfg, "face_order", "largest")
            )
            target_face = sorted_faces[0] if sorted_faces else target_faces[0]
        
        # 2. Get/Detect Source Face
        if isinstance(source, dict) and "embeddings" in source:
            # Dynamic Selection Logic
            target_emb = target_face.embedding
            if target_emb is None:
                if verbose:
                    logger.debug("Target face has no embedding.")
                return None, None
            
            source_embs = source["embeddings"]
            
            # Compute Cosine Similarity
            target_norm = target_emb / (np.linalg.norm(target_emb) + 1e-8)
            
            if "norms" not in source:
                source["norms"] = source_embs / (np.linalg.norm(source_embs, axis=1, keepdims=True) + 1e-8)
            source_norms = source["norms"]
            
            sims = np.dot(source_norms, target_norm)
            best_idx = int(np.argmax(sims))
            best_emb = source_embs[best_idx]
            
            # Create a dummy Face object with the best embedding
            source_face = Face(bbox=np.array([0,0,0,0]), embedding=best_emb)
        elif isinstance(source, Face):
            source_face = source
        else:
            source_face = resolve_source_face(source, cfg, verbose=verbose)
            if source_face is None:
                return None, None
            
        return source_face, target_face

    def run_swap(
        self,
        source_face: Face,
        target_face: Face,
        target_img: np.ndarray,
        swap_model: Optional[str] = None,
        swap_weight: Optional[float] = None,
        job_config: Optional[JobConfig] = None,
        restore_model: Optional[str] = None,
        restore_weight: Optional[float] = None,
        restore_blend: Optional[float] = None
    ) -> np.ndarray:
        cfg = job_config or JobConfig.from_state(state)
        model = swap_model or cfg.swap_model
        weight = swap_weight if swap_weight is not None else cfg.swap_weight
        eff_restore_model = restore_model or cfg.restore_model
        eff_restore_weight = restore_weight if restore_weight is not None else cfg.restore_weight
        eff_restore_blend = restore_blend if restore_blend is not None else cfg.restore_blend
        return swap(
            source_face=source_face,
            target_face=target_face,
            frame=target_img,
            swap_model=model,
            swap_weight=weight,
            mask_types=cfg.mask_types,
            mask_regions=cfg.mask_regions,
            providers=cfg.providers,
            mask_padding=getattr(cfg, "mask_padding", None),
            mask_blur=getattr(cfg, "mask_blur", None),
            clean_source_face=getattr(cfg, "clean_source_face", False),
            face_boost=getattr(cfg, "face_boost", "none"),
            restore_model=eff_restore_model,
            restore_weight=eff_restore_weight,
            restore_blend=eff_restore_blend,
            target_hair_protect=getattr(cfg, "target_hair_protect", True)
        )

    def run_restore(
        self,
        target_face: Face,
        current_img: np.ndarray,
        restore_model: Optional[str] = None,
        weight: Optional[float] = None,
        blend: Optional[float] = None,
        job_config: Optional[JobConfig] = None,
        verbose: bool = True
    ) -> np.ndarray:
        cfg = job_config or JobConfig.from_state(state)
        model = restore_model or cfg.restore_model
        res_weight = weight if weight is not None else cfg.restore_weight
        res_blend = blend if blend is not None else (cfg.restore_blend / 100.0)
        if isinstance(res_blend, (int, float)) and res_blend > 1.0:
            res_blend = res_blend / 100.0
            
        if verbose:
            logger.debug(f"Starting Restorer (model: {model}, blend: {res_blend})...")
        return restore(
            target_face=target_face,
            frame=current_img,
            weight=res_weight,
            blend=res_blend,
            restore_model=model,
            mask_types=cfg.mask_types,
            providers=cfg.providers
        )

    def run_color(
        self,
        target_face: Face,
        current_img: np.ndarray,
        original_img: np.ndarray,
        job_config: Optional[JobConfig] = None,
        verbose: bool = True
    ) -> np.ndarray:
        cfg = job_config or JobConfig.from_state(state)
        if verbose:
            logger.debug("Starting Compositor (Color Match & Blend)...")
        return composite(
            target_face=target_face,
            swapped_frame=current_img,
            original_frame=original_img,
            mask_types=cfg.mask_types
        )

    def process_image(
        self,
        source: Union[np.ndarray, Face, Dict],
        target_img: np.ndarray,
        job_config: Optional[JobConfig] = None,
        verbose: bool = True
    ) -> np.ndarray:
        cfg = job_config or JobConfig.from_state(state)
        source_face, target_face = self.run_detect(source, target_img, job_config=cfg, verbose=verbose)
        if source_face is None or target_face is None:
            return target_img
        
        result_img = target_img.copy()
        
        # --- STAGE 1: Primary Pass ---
        if 'swap' in cfg.processors:
            result_img = self.run_swap(
                source_face, target_face, result_img,
                swap_model=cfg.swap_model,
                swap_weight=cfg.swap_weight,
                job_config=cfg,
                restore_model=cfg.restore_model,
                restore_weight=cfg.restore_weight,
                restore_blend=cfg.restore_blend
            )
            
            # Intermediate restore in Stage 1
            # (skip redundant full-frame restore if face_boost already enhanced the crop, unless explicitly toggled)
            need_stage1_full_restore = getattr(cfg, "stage1_restore", False) or (
                not getattr(cfg, "dual_swap", False) and 'restore' in cfg.processors and getattr(cfg, "face_boost", "none") == "none"
            )
            if need_stage1_full_restore:
                result_img = self.run_restore(
                    target_face, result_img,
                    restore_model=cfg.restore_model,
                    weight=cfg.restore_weight,
                    blend=cfg.restore_blend,
                    job_config=cfg,
                    verbose=verbose
                )
            
        # --- STAGE 2: Refinement Pass (Dual-Stage) ---
        if getattr(cfg, "dual_swap", False):
            result_img = self.run_swap(
                source_face, target_face, result_img,
                swap_model=cfg.swap_model_2,
                swap_weight=cfg.swap_weight_2,
                job_config=cfg,
                restore_model=cfg.restore_model_2,
                restore_weight=cfg.restore_weight_2,
                restore_blend=cfg.restore_blend_2
            )
            
            if getattr(cfg, "stage2_restore", False):
                result_img = self.run_restore(
                    target_face, result_img,
                    restore_model=cfg.restore_model_2,
                    weight=cfg.restore_weight_2,
                    blend=cfg.restore_blend_2,
                    job_config=cfg,
                    verbose=verbose
                )
                
        # --- Compositor (Color Match) ---
        if 'color' in cfg.processors:
            result_img = self.run_color(target_face, result_img, target_img, job_config=cfg, verbose=verbose)
            
        return result_img

service_app = FaceService()

def run_detect(source: Union[np.ndarray, Face, Dict], target_img: np.ndarray, job_config: Optional[JobConfig] = None, verbose: bool = True):
    return service_app.run_detect(source, target_img, job_config=job_config, verbose=verbose)

def run_swap(
    source_face: Face,
    target_face: Face,
    target_img: np.ndarray,
    swap_model: Optional[str] = None,
    swap_weight: Optional[float] = None,
    job_config: Optional[JobConfig] = None,
    restore_model: Optional[str] = None,
    restore_weight: Optional[float] = None,
    restore_blend: Optional[float] = None
) -> np.ndarray:
    return service_app.run_swap(
        source_face, target_face, target_img,
        swap_model=swap_model,
        swap_weight=swap_weight,
        job_config=job_config,
        restore_model=restore_model,
        restore_weight=restore_weight,
        restore_blend=restore_blend
    )

def run_restore(
    target_face: Face,
    current_img: np.ndarray,
    restore_model: Optional[str] = None,
    weight: Optional[float] = None,
    blend: Optional[float] = None,
    job_config: Optional[JobConfig] = None,
    verbose: bool = True
) -> np.ndarray:
    return service_app.run_restore(
        target_face, current_img,
        restore_model=restore_model,
        weight=weight,
        blend=blend,
        job_config=job_config,
        verbose=verbose
    )

def run_color(target_face: Face, current_img: np.ndarray, original_img: np.ndarray, job_config: Optional[JobConfig] = None, verbose: bool = True) -> np.ndarray:
    return service_app.run_color(target_face, current_img, original_img, job_config=job_config, verbose=verbose)

def process_image(source: Union[np.ndarray, Face, Dict], target_img: np.ndarray, job_config: Optional[JobConfig] = None, verbose: bool = True) -> np.ndarray:
    return service_app.process_image(source, target_img, job_config=job_config, verbose=verbose)
