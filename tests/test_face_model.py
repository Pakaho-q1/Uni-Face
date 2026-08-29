import os
import unittest
import tempfile
import numpy as np

from uniface.core.types import Face
from uniface.core.face_model import save_face_model, load_face_model

class TestFaceModel(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_save_and_load_face_model(self):
        # Create 3 dummy faces with 512-dim embeddings
        emb1 = np.random.randn(512).astype(np.float32)
        emb2 = np.random.randn(512).astype(np.float32)
        emb3 = np.random.randn(512).astype(np.float32)
        
        faces = [
            Face(bbox=np.array([0, 0, 100, 100]), embedding=emb1),
            Face(bbox=np.array([10, 10, 110, 110]), embedding=emb2),
            Face(bbox=np.array([20, 20, 120, 120]), embedding=emb3)
        ]
        
        saved_path = save_face_model("test_person", faces, self.tmp_dir.name)
        self.assertTrue(os.path.exists(saved_path))
        self.assertTrue(saved_path.endswith("test_person.safetensors"))
        
        # Load face model
        loaded = load_face_model("test_person", self.tmp_dir.name)
        self.assertIn("embeddings", loaded)
        self.assertEqual(loaded["embeddings"].shape, (3, 512))
        np.testing.assert_array_almost_equal(loaded["embeddings"][0], emb1)
        np.testing.assert_array_almost_equal(loaded["embeddings"][1], emb2)
        np.testing.assert_array_almost_equal(loaded["embeddings"][2], emb3)

    def test_save_face_model_empty_raises(self):
        faces_no_emb = [Face(bbox=np.array([0, 0, 100, 100]))]
        with self.assertRaises(ValueError):
            save_face_model("empty_person", faces_no_emb, self.tmp_dir.name)

    def test_load_non_existent_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_face_model("non_existent_person", self.tmp_dir.name)

if __name__ == '__main__':
    unittest.main()
