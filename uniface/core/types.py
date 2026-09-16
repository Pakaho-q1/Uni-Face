import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Face:
    """
    Data Contract: แหล่งเก็บข้อมูลของ 1 ใบหน้าที่หาเจอในรูปภาพ
    ใช้แชร์ไปให้ทุกโมดูล (Parser, Swaper, Restorer) โดยไม่ต้องสร้าง Schema ใหม่
    """
    bbox: np.ndarray  # Bounding box [x1, y1, x2, y2]
    score: float = 0.0 # ความมั่นใจ (Confidence score)
    landmark_5: Optional[np.ndarray] = None  # จุด 5 จุดบนหน้า (ตา, จมูก, ปาก)
    landmark_106: Optional[np.ndarray] = None # จุด 106 จุดบนหน้า (โครงหน้าละเอียด)
    embedding: Optional[np.ndarray] = None  # Vector เอกลักษณ์ใบหน้า (สำหรับจำแนก หรือ swap)
    gender: Optional[int] = None  # 0 or 1
    age: Optional[int] = None
    
    # สำหรับเก็บค่าแปลกๆ เพิ่มเติมจากโมดูลอื่นๆ โดยไม่ต้องแก้ Schema
    attributes: Dict[str, Any] = field(default_factory=dict)

# ตัวแทน Output ของ Swapper/Restorer ที่ต้องมีรูปและ Mask
FrameResult = tuple[np.ndarray, np.ndarray] # (frame, mask)

@dataclass
class JobConfig:
    """
    Execution context encapsulating all job-specific runtime configurations.
    Enables isolated, thread-safe concurrent pipeline executions.
    """
    processors: list[str] = field(default_factory=lambda: ["swap", "restore"])
    swap_model: str = "inswapper_128"
    swap_weight: float = 0.65
    restore_model: str = "gfpgan_1.4"
    restore_weight: float = 1.0
    restore_blend: int = 100
    mask_types: list[str] = field(default_factory=lambda: ["box"])
    mask_regions: list[str] = field(default_factory=lambda: ['skin', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 'nose', 'mouth', 'u_lip', 'l_lip'])
    occlusion_model: str = "xseg_1"
    target_gender: str = "all"
    face_order: str = "largest"
    similarity: bool = False
    providers: list[Any] = field(default_factory=lambda: ["CPUExecutionProvider"])
    execution_thread_count: int = 4
    video_encoder: str = "h264_nvenc"
    reference_face_ids: list[str] = field(default_factory=list)
    reference_threshold: float = 0.6
    face_detector_score: float = 0.65
    face_landmark_score: float = 0.50
    
    # Dual-Stage Swap & Staged Restore Settings
    stage1_restore: bool = False
    dual_swap: bool = False
    swap_model_2: str = "hyperswap_high_512"
    swap_weight_2: float = 0.80
    stage2_restore: bool = True
    restore_model_2: str = "gfpgan_1.4"
    restore_weight_2: float = 1.0
    restore_blend_2: int = 100
    
    # Clean Source Face & Mask Padding
    clean_source_face: bool = False
    mask_padding: list[int] = field(default_factory=lambda: [0, 0, 0, 0])
    mask_blur: float = 0.3
    
    # ReActor Enhancements & Face Boost
    face_boost: str = "none"  # "none", "256", "512"
    restore_source_face: bool = False
    target_hair_protect: bool = True
    
    _cached_ref_embs: Optional[list[np.ndarray]] = field(default=None, repr=False, compare=False)

    def get_reference_embeddings(self) -> list[np.ndarray]:
        if self._cached_ref_embs is not None:
            return self._cached_ref_embs
        if not self.reference_face_ids:
            self._cached_ref_embs = []
            return self._cached_ref_embs
        import base64
        embs = []
        for b64_emb in self.reference_face_ids:
            try:
                emb_bytes = base64.b64decode(b64_emb)
                emb = np.frombuffer(emb_bytes, dtype=np.float32)
                embs.append(emb / (np.linalg.norm(emb) + 1e-8))
            except Exception:
                continue
        self._cached_ref_embs = embs
        return self._cached_ref_embs

    @classmethod
    def from_state(cls, state_obj) -> 'JobConfig':
        """Construct JobConfig snapshot from the current StateManager."""
        return cls(
            processors=list(getattr(state_obj, "processors", ["swap", "restore"])),
            swap_model=getattr(state_obj, "swap_model", "inswapper_128"),
            swap_weight=float(getattr(state_obj, "swap_weight", 0.65)),
            restore_model=getattr(state_obj, "restore_model", "gfpgan_1.4"),
            restore_weight=float(getattr(state_obj, "restore_weight", 1.0)),
            restore_blend=int(getattr(state_obj, "restore_blend", 100)),
            mask_types=list(getattr(state_obj, "mask_types", ["box"])),
            mask_regions=list(getattr(state_obj, "mask_regions", ['skin', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 'nose', 'mouth', 'u_lip', 'l_lip'])),
            occlusion_model=getattr(state_obj, "occlusion_model", "xseg_1"),
            target_gender=getattr(state_obj, "target_gender", "all"),
            face_order=getattr(state_obj, "face_order", "largest"),
            similarity=bool(getattr(state_obj, "similarity", False)),
            providers=list(getattr(state_obj, "providers", ["CPUExecutionProvider"])),
            execution_thread_count=int(getattr(state_obj, "execution_thread_count", 4)),
            video_encoder=str(getattr(state_obj, "video_encoder", "h264_nvenc")),
            reference_face_ids=list(getattr(state_obj, "reference_face_ids", [])),
            reference_threshold=float(getattr(state_obj, "reference_threshold", 0.6)),
            face_detector_score=float(getattr(state_obj, "face_detector_score", 0.65)),
            face_landmark_score=float(getattr(state_obj, "face_landmark_score", 0.50)),
            stage1_restore=bool(getattr(state_obj, "stage1_restore", False)),
            dual_swap=bool(getattr(state_obj, "dual_swap", False)),
            swap_model_2=str(getattr(state_obj, "swap_model_2", "hyperswap_high_512")),
            swap_weight_2=float(getattr(state_obj, "swap_weight_2", 0.80)),
            stage2_restore=bool(getattr(state_obj, "stage2_restore", True)),
            restore_model_2=str(getattr(state_obj, "restore_model_2", "gfpgan_1.4")),
            restore_weight_2=float(getattr(state_obj, "restore_weight_2", 1.0)),
            restore_blend_2=int(getattr(state_obj, "restore_blend_2", 100)),
            clean_source_face=bool(getattr(state_obj, "clean_source_face", False)),
            mask_padding=list(getattr(state_obj, "mask_padding", [0, 0, 0, 0])),
            mask_blur=float(getattr(state_obj, "mask_blur", 0.3)),
            face_boost=str(getattr(state_obj, "face_boost", "none")),
            restore_source_face=bool(getattr(state_obj, "restore_source_face", False)),
            target_hair_protect=bool(getattr(state_obj, "target_hair_protect", True))
        )

