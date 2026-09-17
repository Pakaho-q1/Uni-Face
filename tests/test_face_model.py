import os
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
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

    @patch('uniface.api.routers.face_models.get_platform_dir')
    @patch('uniface.core.face_model.save_face_model')
    @patch('uniface.modules.detector.detect')
    @patch('uniface.modules.restorer.restore_crop')
    @patch('uniface.modules.detector.get_detector')
    def test_build_face_model_with_restore_source_face(self, mock_get_det, mock_restore_crop, mock_detect, mock_save, mock_get_plat):
        import asyncio
        from unittest.mock import AsyncMock, MagicMock
        from uniface.api.routers.face_models import build_face_model
        import cv2

        mock_get_plat.return_value = self.tmp_dir.name
        mock_save.return_value = os.path.join(self.tmp_dir.name, "face_models", "person.safetensors")

        dummy_face = Face(
            bbox=np.array([50, 50, 200, 200]),
            landmark_5=np.array([[80, 80], [140, 80], [110, 110], [90, 150], [130, 150]], dtype=np.float32),
            embedding=np.zeros(512, dtype=np.float32)
        )
        mock_detect.return_value = [dummy_face]
        mock_restore_crop.return_value = np.zeros((512, 512, 3), dtype=np.uint8)

        mock_det = MagicMock()
        mock_det._calculate_embedding.return_value = np.ones(512, dtype=np.float32) * 5.0
        mock_get_det.return_value = mock_det

        # Create dummy image bytes
        dummy_img = np.zeros((300, 300, 3), dtype=np.uint8)
        _, img_buf = cv2.imencode('.jpg', dummy_img)

        mock_file = MagicMock()
        mock_file.read = AsyncMock(return_value=img_buf.tobytes())

        res = asyncio.run(build_face_model(
            name="person",
            files=[mock_file],
            restore_source_face=True,
            restore_model="codeformer",
            restore_weight=0.75,
            x_client_platform="test_plat"
        ))

        self.assertEqual(res["status"], "success")
        self.assertEqual(res["faces_extracted"], 1)
        mock_restore_crop.assert_called_once()
        _, kwargs = mock_restore_crop.call_args
        self.assertEqual(kwargs.get("restore_model"), "codeformer")
        self.assertAlmostEqual(kwargs.get("weight"), 0.75)
        mock_save.assert_called_once()
        saved_faces = mock_save.call_args[0][1]
        self.assertTrue(np.allclose(saved_faces[0].embedding, np.ones(512, dtype=np.float32) * 5.0))

if __name__ == '__main__':
    unittest.main()
