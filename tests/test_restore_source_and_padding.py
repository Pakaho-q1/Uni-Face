import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from uniface.core.types import Face, JobConfig
from uniface.modules.utils import face_math
from uniface.modules.restorer import FaceRestorer
from uniface.core.service import resolve_source_face, clear_source_face_cache


class TestAdaptiveFacePadding(unittest.TestCase):

    def test_check_face_needs_padding_normal_face(self):
        # Medium face comfortably in center of 1000x1000 frame
        face = Face(
            bbox=np.array([300, 300, 500, 500]),
            landmark_5=np.array([[350, 350], [450, 350], [400, 400], [360, 460], [440, 460]], dtype=np.float32)
        )
        self.assertFalse(face_math.check_face_needs_padding(face, (1000, 1000, 3)))

    def test_check_face_needs_padding_large_face(self):
        # Large face occupying 60% of frame width/height
        face = Face(
            bbox=np.array([200, 200, 800, 800]),
            landmark_5=np.array([[350, 350], [650, 350], [500, 500], [400, 700], [600, 700]], dtype=np.float32)
        )
        self.assertTrue(face_math.check_face_needs_padding(face, (1000, 1000, 3)))

    def test_check_face_needs_padding_boundary_touching(self):
        # Face touching left border (x1=10 in 1000px image)
        face = Face(
            bbox=np.array([10, 300, 250, 550]),
            landmark_5=np.array([[50, 350], [150, 350], [100, 400], [60, 480], [140, 480]], dtype=np.float32)
        )
        self.assertTrue(face_math.check_face_needs_padding(face, (1000, 1000, 3)))

    def test_pad_and_resize_and_unpad(self):
        crop = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        resized, pad_info = face_math.pad_and_resize_crop(crop, padding_ratio=0.15)
        self.assertEqual(resized.shape, (512, 512, 3))
        self.assertEqual(pad_info, (76, 76, 76, 76))
        
        # Simulate model output (e.g. enhanced crop of same shape)
        unpadded = face_math.unpad_crop(resized, pad_info, (512, 512))
        self.assertEqual(unpadded.shape, (512, 512, 3))


class TestRestoreSourceFaceConfig(unittest.TestCase):

    def setUp(self):
        clear_source_face_cache()

    @patch('uniface.core.service.detect')
    @patch('uniface.modules.restorer.restore_crop')
    @patch('uniface.modules.detector.get_detector')
    def test_resolve_source_face_with_custom_model_and_weight(self, mock_get_det, mock_restore_crop, mock_detect):
        dummy_face = Face(
            bbox=np.array([100, 100, 400, 400]),
            landmark_5=np.array([[180, 200], [320, 200], [250, 270], [200, 340], [300, 340]], dtype=np.float32),
            embedding=np.ones(512, dtype=np.float32)
        )
        mock_detect.return_value = [dummy_face]
        
        mock_enhanced_crop = np.zeros((512, 512, 3), dtype=np.uint8)
        mock_restore_crop.return_value = mock_enhanced_crop
        
        mock_detector_instance = MagicMock()
        mock_detector_instance._calculate_embedding.return_value = np.full(512, 2.0, dtype=np.float32)
        mock_get_det.return_value = mock_detector_instance
        
        img = np.zeros((512, 512, 3), dtype=np.uint8)
        
        cfg = JobConfig(
            restore_source_face=True,
            restore_source_face_model="codeformer",
            restore_source_face_weight=0.65
        )
        
        result_face = resolve_source_face(img, job_config=cfg)
        self.assertIsNotNone(result_face)
        mock_restore_crop.assert_called_once()
        _, kwargs = mock_restore_crop.call_args
        self.assertEqual(kwargs.get("restore_model"), "codeformer")
        self.assertAlmostEqual(kwargs.get("weight"), 0.65)
        self.assertTrue(np.allclose(result_face.embedding, np.full(512, 2.0, dtype=np.float32)))

    @patch('onnxruntime.InferenceSession')
    def test_restorer_restore_crop_with_padding(self, mock_ort_session):
        mock_session = MagicMock()
        mock_input = MagicMock()
        mock_input.name = 'input'
        mock_session.get_inputs.return_value = [mock_input]
        mock_ort_session.return_value = mock_session
        
        dummy_out = np.zeros((3, 512, 512), dtype=np.float32)
        mock_session.run.return_value = [[dummy_out]]
        
        restorer = FaceRestorer(model_key="gfpgan_1.4")
        crop = np.zeros((512, 512, 3), dtype=np.uint8)
        enhanced = restorer.restore_crop(crop, padding_ratio=0.15)
        self.assertEqual(enhanced.shape, (512, 512, 3))


if __name__ == '__main__':
    unittest.main()
