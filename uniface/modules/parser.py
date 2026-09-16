import cv2
import numpy as np
import onnxruntime
import threading
from typing import List

from uniface.core.config import MODEL_PATHS, DEFAULT_EXECUTION_PROVIDERS
from uniface.core.state import state
from uniface.core.logging import get_logger

logger = get_logger(__name__)

class MaskParser:
    """
    Native implementation of Face Masking (Occlusion, Region, Box).
    """
    def __init__(self):
        self.providers = state.providers
        self.xseg_sessions = {}
        self.bisenet_session = None
        
        # Region mappings for BiseNet
        self.region_mapping = {
            'skin': 1, 'l_brow': 2, 'r_brow': 3, 'l_eye': 4, 'r_eye': 5,
            'eye_g': 6, 'l_ear': 7, 'r_ear': 8, 'ear_r': 9, 'nose': 10,
            'mouth': 11, 'u_lip': 12, 'l_lip': 13, 'neck': 14, 'neck_l': 15,
            'cloth': 16, 'hair': 17, 'hat': 18
        }
        
    def _get_xseg_session(self, model_name: str = None):
        target_model = model_name or getattr(state, "occlusion_model", "xseg_1") or "xseg_1"
        if target_model not in MODEL_PATHS:
            target_model = "xseg_1"
            
        if target_model not in self.xseg_sessions:
            sess_options = getattr(state, "session_options", None)
            model_path = str(MODEL_PATHS[target_model])
            self.xseg_sessions[target_model] = onnxruntime.InferenceSession(model_path, providers=self.providers, sess_options=sess_options)
            logger.debug(f"Loading Occlusion Model: {target_model} (Active Providers: {self.xseg_sessions[target_model].get_providers()})")
        return self.xseg_sessions[target_model]
        
    def _get_bisenet_session(self):
        if self.bisenet_session is None:
            sess_options = getattr(state, "session_options", None)
            self.bisenet_session = onnxruntime.InferenceSession(str(MODEL_PATHS["bisenet_resnet_34"]), providers=self.providers, sess_options=sess_options)
            logger.debug(f"Loading Region Model: bisenet_resnet_34 (Active Providers: {self.bisenet_session.get_providers()})")
        return self.bisenet_session

    def unload_bisenet(self):
        if self.bisenet_session is not None:
            logger.info("Unloading BiSeNet model from memory")
            self.bisenet_session = None

    def unload_xseg(self, keep_model: str = None):
        to_del = [k for k in list(self.xseg_sessions.keys()) if k != keep_model]
        for k in to_del:
            logger.info(f"Unloading XSeg model {k} from memory")
            del self.xseg_sessions[k]
        
    def create_occlusion_mask(self, crop_vision_frame: np.ndarray, model_name: str = None) -> np.ndarray:
        """
        Create a mask of occlusions (e.g. hands, hair over face) using selected xseg model.
        """
        model_size = (256, 256)
        
        # Prepare tensor for xseg (expects NHWC, BGR, 0-1)
        prepare_vision_frame = cv2.resize(crop_vision_frame, model_size)
        prepare_vision_frame = np.expand_dims(prepare_vision_frame, axis=0).astype(np.float32) / 255.0
        
        # Run Inference
        session = self._get_xseg_session(model_name)
        occlusion_mask = session.run(None, {session.get_inputs()[0].name: prepare_vision_frame})[0][0]
        
        # Ensure it's (H, W)
        if occlusion_mask.ndim == 3 and occlusion_mask.shape[-1] == 1:
            occlusion_mask = np.squeeze(occlusion_mask, axis=-1)
            
        occlusion_mask = occlusion_mask.clip(0, 1).astype(np.float32)
        occlusion_mask = cv2.resize(occlusion_mask, crop_vision_frame.shape[:2][::-1])
        
        # Soften edges
        occlusion_mask = (cv2.GaussianBlur(occlusion_mask.clip(0, 1), (0, 0), 5).clip(0.5, 1) - 0.5) * 2
        return occlusion_mask
        
    def create_region_mask(self, temp_vision_frame: np.ndarray, target_face, affine_matrix, crop_shape, regions: List[str] = None) -> np.ndarray:
        """
        Create a mask for specific facial regions using bisenet_resnet_34.
        BiseNet expects ffhq_512 alignment. We warp the full frame to ffhq_512,
        segment, and then project the mask back to the requested crop space (e.g. arcface_128).
        """
        if regions is None:
            from uniface.core.state import state
            regions = state.mask_regions
            
        if target_face is None or affine_matrix is None:
            return np.ones(crop_shape[:2], dtype=np.float32)
            
        from uniface.modules.utils import face_math
        
        # 1. Warp full frame to ffhq_512
        model_size = (512, 512)
        ffhq_crop, ffhq_matrix = face_math.warp_face_by_face_landmark_5(
            temp_vision_frame, target_face.landmark_5, 'ffhq_512', model_size
        )
        if ffhq_crop is None or ffhq_matrix is None or affine_matrix is None:
            return np.ones(crop_shape[:2], dtype=np.float32)
        
        # 2. Prepare tensor (expects NCHW, RGB, normalized with mean/std)
        prepare_vision_frame = ffhq_crop[:, :, ::-1].astype(np.float32) / 255.0
        prepare_vision_frame = np.subtract(prepare_vision_frame, np.array([0.485, 0.456, 0.406], dtype=np.float32))
        prepare_vision_frame = np.divide(prepare_vision_frame, np.array([0.229, 0.224, 0.225], dtype=np.float32))
        
        prepare_vision_frame = np.expand_dims(prepare_vision_frame, axis=0)
        prepare_vision_frame = prepare_vision_frame.transpose(0, 3, 1, 2)
        
        # 3. Run Inference
        region_prediction = self._get_bisenet_session().run(None, {self._get_bisenet_session().get_inputs()[0].name: prepare_vision_frame})[0][0]
        
        # Output is (19, 512, 512)
        class_indices = region_prediction.argmax(axis=0)
        target_indices = [self.region_mapping[r] for r in regions if r in self.region_mapping]
        ffhq_mask = np.isin(class_indices, target_indices).astype(np.float32)
        
        # 4. Project ffhq_mask back to full frame
        box_mask, paste_matrix = face_math.calculate_paste_area(temp_vision_frame, ffhq_crop, ffhq_matrix)
        x1, y1, x2, y2 = box_mask
        full_mask = np.zeros(temp_vision_frame.shape[:2], dtype=np.float32)
        if x2 > x1 and y2 > y1 and paste_matrix is not None:
            inverse_mask = cv2.warpAffine(ffhq_mask, paste_matrix, (x2 - x1, y2 - y1), flags=cv2.INTER_LINEAR)
            full_mask[y1:y2, x1:x2] = inverse_mask
        
        # 5. Project full frame mask to the target crop space (e.g. arcface_128)
        crop_mask = cv2.warpAffine(full_mask, affine_matrix, (crop_shape[1], crop_shape[0]), flags=cv2.INTER_LINEAR)
        
        crop_mask = (cv2.GaussianBlur(crop_mask.clip(0, 1), (0, 0), 5).clip(0.5, 1) - 0.5) * 2
        return crop_mask
        
    def create_box_mask(self, crop_vision_frame: np.ndarray, padding: List[int] = [0, 0, 0, 0], blur: float = 0.3) -> np.ndarray:
        """
        Create a rectangular box mask with blurred edges to seamlessly blend the crop.
        padding: [top, right, bottom, left] in percentages.
        """
        crop_size = crop_vision_frame.shape[:2][::-1]
        blur_amount = int(crop_size[0] * 0.5 * blur)
        blur_area = max(blur_amount // 2, 1)
        
        box_mask = np.ones((crop_size[1], crop_size[0]), dtype=np.float32)
        
        # Apply padding (percentage based)
        box_mask[:max(blur_area, int(crop_size[1] * padding[0] / 100)), :] = 0
        box_mask[-max(blur_area, int(crop_size[1] * padding[2] / 100)):, :] = 0
        box_mask[:, :max(blur_area, int(crop_size[0] * padding[3] / 100))] = 0
        box_mask[:, -max(blur_area, int(crop_size[0] * padding[1] / 100)):] = 0
        
        if blur_amount > 0:
            box_mask = cv2.GaussianBlur(box_mask, (0, 0), blur_amount * 0.25)
            
        return box_mask

    def create_eyes_mask(self, crop_vision_frame: np.ndarray, target_face, affine_matrix) -> np.ndarray:
        """
        Create a priority mask for eyes to force them to be pasted, overriding subtractive masks.
        Transforms target landmarks into the crop space.
        """
        crop_size = crop_vision_frame.shape[:2][::-1]
        mask = np.zeros((crop_size[1], crop_size[0]), dtype=np.float32)
        
        if target_face is None or not hasattr(target_face, "landmark_5") or affine_matrix is None:
            return mask
            
        landmarks = target_face.landmark_5
        crop_landmarks = cv2.transform(np.array([landmarks]), affine_matrix)[0]
        
        left_eye = crop_landmarks[0]
        right_eye = crop_landmarks[1]
        
        eye_dist = float(np.linalg.norm(left_eye - right_eye))
        radius_x = max(10, int(eye_dist * 0.42))
        radius_y = max(8, int(radius_x * 0.65))
        
        for eye in (left_eye, right_eye):
            center = (int(eye[0]), int(eye[1]))
            cv2.ellipse(mask, center, (radius_x, radius_y), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
            
        # Adaptive blur based on crop size
        blur_amount = max(3, int(crop_size[0] * 0.05))
        if blur_amount % 2 == 0: blur_amount += 1
        
        mask = cv2.GaussianBlur(mask, (blur_amount, blur_amount), blur_amount * 0.2)
        mask = np.clip(mask, 0.0, 1.0)
        return mask

    def create_oval_mask(self, crop_shape, blur: float = 0.3) -> np.ndarray:
        """
        Create a natural elliptical/oval gradient mask (ReActor HyperSwap style)
        to eliminate rectangular box cut lines.
        """
        h, w = crop_shape[:2]
        mask = np.zeros((h, w), dtype=np.float32)
        center = (w // 2, h // 2)
        axes = (int(w * 0.38), int(h * 0.44))
        cv2.ellipse(mask, center, axes, 0, 0, 360, 1.0, -1)
        
        blur_k = max(15, int(min(h, w) * blur * 0.5))
        if blur_k % 2 == 0: blur_k += 1
        mask = cv2.GaussianBlur(mask, (blur_k, blur_k), 0)
        return np.clip(mask, 0.0, 1.0)

    def create_target_bisenet_mask(
        self,
        temp_vision_frame: np.ndarray,
        target_face,
        affine_matrix,
        crop_shape
    ) -> np.ndarray:
        """
        ReActor formula: Segment face vs hair on the TARGET face using BiSeNet.
        Mask values:
          - Skin (1), Brows (2,3), Eyes (4,5), Nose (10), Mouth/Lips (11,12,13), Neck_l (15) = 1.0
          - Background (0), Neck (14), Cloth (16), Hair (17), Hat (18) = 0.0
        Apply double Gaussian blur (101x101, sigma 11) for ultra-soft, seamless blending with target bangs.
        """
        if target_face is None or not hasattr(target_face, "landmark_5") or affine_matrix is None:
            return np.ones(crop_shape[:2], dtype=np.float32)
            
        from uniface.modules.utils import face_math
        
        # 1. Warp full frame to ffhq_512
        model_size = (512, 512)
        ffhq_crop, ffhq_matrix = face_math.warp_face_by_face_landmark_5(
            temp_vision_frame, target_face.landmark_5, 'ffhq_512', model_size
        )
        if ffhq_crop is None or ffhq_matrix is None:
            return np.ones(crop_shape[:2], dtype=np.float32)
            
        # 2. Prepare tensor for BiSeNet
        prepare_crop = ffhq_crop[:, :, ::-1].astype(np.float32) / 255.0
        prepare_crop = np.subtract(prepare_crop, np.array([0.485, 0.456, 0.406], dtype=np.float32))
        prepare_crop = np.divide(prepare_crop, np.array([0.229, 0.224, 0.225], dtype=np.float32))
        prepare_crop = np.expand_dims(prepare_crop, axis=0).transpose(0, 3, 1, 2)
        
        bisenet = self._get_bisenet_session()
        pred = bisenet.run(None, {bisenet.get_inputs()[0].name: prepare_crop})[0][0]
        class_map = pred.argmax(axis=0) # 512x512
        
        # Exact ReActor colormap:
        # Skin and facial features are kept, hair (17), hat (18), cloth (16), neck (14), bg (0) are 0
        keep_classes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15]
        face_mask_512 = np.isin(class_map, keep_classes).astype(np.float32)
        
        # ReActor's double Gaussian blur (101, 101) with sigma 11
        face_mask_512 = cv2.GaussianBlur(face_mask_512, (101, 101), 11)
        face_mask_512 = cv2.GaussianBlur(face_mask_512, (101, 101), 11)
        
        # Remove border artifacts
        thres = 10
        face_mask_512[:thres, :] = 0
        face_mask_512[-thres:, :] = 0
        face_mask_512[:, :thres] = 0
        face_mask_512[:, -thres:] = 0
        
        # 3. Project face_mask back to full frame
        box_mask, paste_matrix = face_math.calculate_paste_area(temp_vision_frame, ffhq_crop, ffhq_matrix)
        x1, y1, x2, y2 = box_mask
        full_mask = np.zeros(temp_vision_frame.shape[:2], dtype=np.float32)
        if x2 > x1 and y2 > y1 and paste_matrix is not None:
            inverse_mask = cv2.warpAffine(face_mask_512, paste_matrix, (x2 - x1, y2 - y1), flags=cv2.INTER_LINEAR)
            full_mask[y1:y2, x1:x2] = inverse_mask
            
        # 4. Project full frame mask to the target crop space (e.g. 128x128, 256x256, or 512x512)
        crop_target_mask = cv2.warpAffine(full_mask, affine_matrix, (crop_shape[1], crop_shape[0]), flags=cv2.INTER_LINEAR)
        return np.clip(crop_target_mask, 0.0, 1.0)

    # Keep create_hair_mask for backward compatibility
    def create_hair_mask(self, temp_vision_frame: np.ndarray, target_face, affine_matrix, crop_shape, blur: float = 0.3) -> np.ndarray:
        return self.create_target_bisenet_mask(temp_vision_frame, target_face, affine_matrix, crop_shape)

    def get_combined_mask(
        self,
        temp_vision_frame: np.ndarray,
        crop_vision_frame: np.ndarray,
        mask_types: List[str] = None,
        target_face = None,
        affine_matrix = None,
        occlusion_model: str = None,
        mask_padding: List[int] = None,
        mask_blur: float = None,
        clean_source_face: bool = None,
        mask_regions: List[str] = None,
        target_hair_protect: bool = None
    ) -> np.ndarray:
        """
        Unified mask combination with ReActor-style target hair protection,
        4-way boundary padding, optional oval mask, occlusion, and facial regions.
        """
        if mask_types is None:
            mask_types = ['box']
            
        if mask_padding is None:
            mask_padding = getattr(state, "mask_padding", [0, 0, 0, 0]) or [0, 0, 0, 0]
            
        blur_val = mask_blur if mask_blur is not None else getattr(state, "mask_blur", 0.3)
        do_protect = target_hair_protect if target_hair_protect is not None else getattr(state, "target_hair_protect", True)
            
        crop_masks = []
        
        # Apply oval mask if requested
        if 'oval' in mask_types:
            crop_masks.append(self.create_oval_mask(crop_vision_frame.shape, blur=blur_val))
            
        # Apply box mask if requested OR if any mask padding is specified
        if 'box' in mask_types or any(p > 0 for p in mask_padding):
            crop_masks.append(self.create_box_mask(crop_vision_frame, padding=mask_padding, blur=blur_val))
            
        # Target Hair Protection (BiSeNet Hair=0, Hat=0, 101px blur)
        if do_protect and target_face is not None and affine_matrix is not None:
            crop_masks.append(self.create_target_bisenet_mask(temp_vision_frame, target_face, affine_matrix, crop_vision_frame.shape))
            
        if 'occlusion' in mask_types:
            crop_masks.append(self.create_occlusion_mask(crop_vision_frame, occlusion_model))
            
        if 'region' in mask_types:
            crop_masks.append(self.create_region_mask(temp_vision_frame, target_face, affine_matrix, crop_vision_frame.shape, regions=mask_regions))
            
        if not crop_masks:
            combined_mask = np.ones(crop_vision_frame.shape[:2], dtype=np.float32)
        else:
            combined_mask = np.minimum.reduce(crop_masks).clip(0, 1)
            
        # Priority additive masks (e.g., eyes)
        if 'eyes' in mask_types:
            eyes_mask = self.create_eyes_mask(crop_vision_frame, target_face, affine_matrix)
            combined_mask = np.maximum(combined_mask, eyes_mask)
            
        return combined_mask

# Export a default instance
parser_app = None
_lock = threading.Lock()

def get_parser() -> MaskParser:
    global parser_app
    if parser_app is None:
        with _lock:
            if parser_app is None:
                parser_app = MaskParser()
    return parser_app

def get_combined_mask(
    temp_vision_frame: np.ndarray,
    crop_vision_frame: np.ndarray,
    mask_types: List[str] = None,
    target_face = None,
    affine_matrix = None,
    occlusion_model: str = None,
    mask_padding: List[int] = None,
    mask_blur: float = None,
    clean_source_face: bool = None,
    mask_regions: List[str] = None,
    target_hair_protect: bool = None
) -> np.ndarray:
    return get_parser().get_combined_mask(
        temp_vision_frame=temp_vision_frame,
        crop_vision_frame=crop_vision_frame,
        mask_types=mask_types,
        target_face=target_face,
        affine_matrix=affine_matrix,
        occlusion_model=occlusion_model,
        mask_padding=mask_padding,
        mask_blur=mask_blur,
        clean_source_face=clean_source_face,
        mask_regions=mask_regions,
        target_hair_protect=target_hair_protect
    )
