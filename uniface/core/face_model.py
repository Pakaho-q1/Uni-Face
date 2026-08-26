import os
import numpy as np
from safetensors.numpy import save_file, load_file
from uniface.core.types import Face

def save_face_model(name: str, faces: list[Face], workspace_dir: str):
    """
    Save multiple faces (embeddings) into a .safetensors file.
    Args:
        name: the model name (e.g., 'john_doe')
        faces: a list of Face objects (must contain embeddings)
        workspace_dir: the base workspace directory
    """
    models_dir = os.path.join(workspace_dir, "face_models")
    os.makedirs(models_dir, exist_ok=True)
    
    embeddings = []
    for f in faces:
        if f.embedding is not None:
            embeddings.append(f.embedding)
            
    if not embeddings:
        raise ValueError("No embeddings found in the provided faces.")
        
    # Stack into shape (N, 512)
    tensor = np.vstack(embeddings).astype(np.float32)
    
    filepath = os.path.join(models_dir, f"{name}.safetensors")
    
    # safetensors requires a dict of numpy arrays
    tensors = {"embeddings": tensor}
    save_file(tensors, filepath)
    return filepath

def load_face_model(name: str, workspace_dir: str) -> dict:
    """
    Load a .safetensors face model.
    Returns:
        dict containing the 'embeddings' tensor
    """
    filepath = os.path.join(workspace_dir, "face_models", f"{name}.safetensors")
    if not os.path.exists(filepath):
        # Allow checking if user passed .safetensors in name
        if name.endswith(".safetensors"):
            filepath = os.path.join(workspace_dir, "face_models", name)
        else:
            filepath = os.path.join(workspace_dir, "face_models", f"{name}.safetensors")
            
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Face model {name} not found at {filepath}")
            
    tensors = load_file(filepath)
    return tensors
