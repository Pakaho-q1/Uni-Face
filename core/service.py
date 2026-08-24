import numpy as np
import cv2
from typing import Union, Dict
from core.types import Face

from core.state import state
from modules.detector import detect
from modules.swaper.swap import swap
from modules.restorer import restore
from modules.compositor import composite

class FaceService:
    def __init__(self):
        pass

    def run_detect(self, source: Union[np.ndarray, Face, Dict], target_img: np.ndarray, verbose: bool = True):
        """
        Detect faces in target and source. Handles dynamic source selection.
        Returns: (source_face, target_face) or (None, None) if detection fails.
        """
        # 1. Detect Target Faces
        target_faces = detect(target_img)
        if not target_faces:
            if verbose:
                print("No face detected in target image.")
            return None, None
            
        target_faces.sort(key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
        target_face = target_faces[0]
        
        # 2. Get/Detect Source Face
        if isinstance(source, np.ndarray):
            source_faces = detect(source)
            if not source_faces:
                if verbose:
                    print("No face detected in source image.")
                return None, None
            source_faces.sort(key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
            source_face = source_faces[0]
        elif isinstance(source, dict) and "embeddings" in source:
            # Dynamic Selection Logic
            target_emb = target_face.embedding
            if target_emb is None:
                if verbose:
                    print("Target face has no embedding.")
                return None, None
            
            source_embs = source["embeddings"]
            
            # Compute Cosine Similarity
            target_norm = target_emb / (np.linalg.norm(target_emb) + 1e-8)
            
            if "norms" not in source:
                source["norms"] = source_embs / (np.linalg.norm(source_embs, axis=1, keepdims=True) + 1e-8)
            source_norms = source["norms"]
            
            sims = np.dot(source_norms, target_norm)
            best_idx = np.argmax(sims)
            best_emb = source_embs[best_idx]
            
            # Create a dummy Face object with the best embedding
            source_face = Face(bbox=np.array([0,0,0,0]), embedding=best_emb)
        else:
            source_face = source
            
        return source_face, target_face

    def run_swap(self, source_face: Face, target_face: Face, target_img: np.ndarray) -> np.ndarray:
        return swap(source_face, target_face, target_img)

    def run_restore(self, target_face: Face, current_img: np.ndarray, verbose: bool = True) -> np.ndarray:
        if verbose:
            print(f"Starting Restorer (model: {state.restore_model}, blend: {state.restore_blend})...")
        return restore(target_face, current_img, blend=(state.restore_blend / 100.0))

    def run_color(self, target_face: Face, current_img: np.ndarray, original_img: np.ndarray, verbose: bool = True) -> np.ndarray:
        if verbose:
            print("Starting Compositor (Color Match & Blend)...")
        return composite(target_face, current_img, original_img)

    def process_image(self, source: Union[np.ndarray, Face, Dict], target_img: np.ndarray, verbose: bool = True) -> np.ndarray:
        source_face, target_face = self.run_detect(source, target_img, verbose)
        if source_face is None or target_face is None:
            return target_img
        
        result_img = target_img.copy()
        
        if 'swap' in state.processors:
            result_img = self.run_swap(source_face, target_face, result_img)
            
        if 'restore' in state.processors:
            result_img = self.run_restore(target_face, result_img, verbose)
            
        if 'color' in state.processors:
            result_img = self.run_color(target_face, result_img, target_img, verbose)
            
        return result_img

service_app = FaceService()

def run_detect(source: Union[np.ndarray, Face, Dict], target_img: np.ndarray, verbose: bool = True):
    return service_app.run_detect(source, target_img, verbose)

def run_swap(source_face: Face, target_face: Face, target_img: np.ndarray) -> np.ndarray:
    return service_app.run_swap(source_face, target_face, target_img)

def run_restore(target_face: Face, current_img: np.ndarray, verbose: bool = True) -> np.ndarray:
    return service_app.run_restore(target_face, current_img, verbose)

def run_color(target_face: Face, current_img: np.ndarray, original_img: np.ndarray, verbose: bool = True) -> np.ndarray:
    return service_app.run_color(target_face, current_img, original_img, verbose)

def process_image(source: Union[np.ndarray, Face, Dict], target_img: np.ndarray, verbose: bool = True) -> np.ndarray:
    return service_app.process_image(source, target_img, verbose)
