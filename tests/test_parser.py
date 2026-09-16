import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from uniface.modules.parser import MaskParser, get_combined_mask

class TestMaskParser(unittest.TestCase):

    @patch('onnxruntime.InferenceSession')
    def test_create_occlusion_mask(self, mock_ort_session):
        mock_xseg_session = MagicMock()
        mock_bisenet_session = MagicMock()
        mock_ort_session.side_effect = [mock_xseg_session, mock_bisenet_session]
        
        # Mock xseg output (H, W, 1) or (1, H, W, 1) depending on model, parser takes [0][0]
        # Let's mock [0][0] as returning a 256x256x1 array
        dummy_xseg_out = np.ones((256, 256, 1), dtype=np.float32)
        
        mock_run_result = MagicMock()
        mock_run_result.__getitem__.return_value = MagicMock()
        mock_run_result.__getitem__().__getitem__.return_value = dummy_xseg_out
        # Or simpler:
        mock_xseg_session.run.return_value = [[dummy_xseg_out]]
        
        parser = MaskParser()
        crop_vision_frame = np.zeros((128, 128, 3), dtype=np.uint8)
        
        mask = parser.create_occlusion_mask(crop_vision_frame)
        
        self.assertEqual(mask.shape, (128, 128)) # Should be resized back to crop size
        mock_xseg_session.run.assert_called_once()
        
    @patch('onnxruntime.InferenceSession')
    def test_create_region_mask(self, mock_ort_session):
        mock_bisenet_session = MagicMock()
        mock_input = MagicMock()
        mock_input.name = "input"
        mock_bisenet_session.get_inputs.return_value = [mock_input]
        mock_ort_session.return_value = mock_bisenet_session
        
        # Mock bisenet output (1, 19, 512, 512)
        dummy_bisenet_out = np.zeros((19, 512, 512), dtype=np.float32)
        dummy_bisenet_out[1, 100:200, 100:200] = 10.0 # High logit for skin
        
        mock_bisenet_session.run.return_value = [dummy_bisenet_out]
        
        parser = MaskParser()
        full_frame = np.zeros((512, 512, 3), dtype=np.uint8)
        crop_shape = (128, 128, 3)
        affine_matrix = np.eye(2, 3, dtype=np.float32)
        
        from uniface.core.types import Face
        target_face = Face(
            bbox=np.array([100, 100, 400, 400]),
            landmark_5=np.array([[192, 240], [319, 240], [257, 314], [201, 371], [313, 371]], dtype=np.float32),
            landmark_106=np.zeros((68, 2), dtype=np.float32),
            embedding=np.zeros((512,), dtype=np.float32)
        )
        
        mask = parser.create_region_mask(full_frame, target_face, affine_matrix, crop_shape, regions=['skin'])
        
        self.assertEqual(mask.shape, (128, 128))
        mock_bisenet_session.run.assert_called_once()

    def test_create_box_mask(self):
        # We don't need ONNX for box mask
        with patch('onnxruntime.InferenceSession'):
            parser = MaskParser()
            crop_vision_frame = np.zeros((100, 100, 3), dtype=np.uint8)
            
            # padding: [top, right, bottom, left]
            mask = parser.create_box_mask(crop_vision_frame, padding=[10, 10, 10, 10], blur=0.0)
            
            self.assertEqual(mask.shape, (100, 100))
            self.assertEqual(mask[5, 50], 0.0)   # Top padding area
            self.assertEqual(mask[95, 50], 0.0)  # Bottom padding area
            self.assertEqual(mask[50, 50], 1.0)  # Center area

    def test_get_combined_mask_with_padding(self):
        with patch('onnxruntime.InferenceSession'):
            parser = MaskParser()
            crop_frame = np.zeros((100, 100, 3), dtype=np.uint8)
            full_frame = np.zeros((200, 200, 3), dtype=np.uint8)
            
            # mask_padding: [top=20, right=0, bottom=0, left=0]
            mask = parser.get_combined_mask(
                full_frame, crop_frame, mask_types=['box'], mask_padding=[20, 0, 0, 0]
            )
            self.assertEqual(mask.shape, (100, 100))
            self.assertLess(mask[5, 50], 0.1) # Top should be padded out (faded/0)
            self.assertGreater(mask[50, 50], 0.8) # Center should remain active

    @patch('onnxruntime.InferenceSession')
    def test_create_hair_mask_and_join_alpha(self, mock_ort_session):
        mock_bisenet = MagicMock()
        mock_input = MagicMock()
        mock_input.name = "input"
        mock_bisenet.get_inputs.return_value = [mock_input]
        mock_ort_session.return_value = mock_bisenet
        
        # BiSeNet dummy: Class 17 (hair) at top
        dummy_pred = np.zeros((19, 512, 512), dtype=np.float32)
        dummy_pred[17, 50:150, 150:350] = 10.0 # Hair
        mock_bisenet.run.return_value = [dummy_pred]
        
        from uniface.core.types import Face
        target_face = Face(
            bbox=np.array([100, 100, 400, 400]),
            landmark_5=np.array([[192, 240], [319, 240], [257, 314], [201, 371], [313, 371]], dtype=np.float32),
            landmark_106=np.zeros((68, 2), dtype=np.float32),
            embedding=np.zeros((512,), dtype=np.float32)
        )
        
        parser = MaskParser()
        full_frame = np.zeros((512, 512, 3), dtype=np.uint8)
        crop_frame = np.zeros((128, 128, 3), dtype=np.uint8)
        affine_matrix = np.eye(2, 3, dtype=np.float32)
        
        # 1. create_hair_mask returns inverted alpha (1.0 = keep, 0.0 = hair)
        hair_alpha = parser.create_hair_mask(full_frame, target_face, affine_matrix, crop_frame.shape, blur=0.3)
        self.assertEqual(hair_alpha.shape, (128, 128))
        self.assertGreaterEqual(float(np.min(hair_alpha)), 0.0)
        self.assertLessEqual(float(np.max(hair_alpha)), 1.0)
        
        # 2. get_combined_mask with target_hair_protect=True joins ReActor-style hair protection
        combined = parser.get_combined_mask(
            full_frame, crop_frame, mask_types=['box'],
            target_face=target_face, affine_matrix=affine_matrix,
            target_hair_protect=True, mask_blur=0.3
        )
        self.assertEqual(combined.shape, (128, 128))

    def test_create_oval_mask(self):
        with patch('onnxruntime.InferenceSession'):
            parser = MaskParser()
            mask = parser.create_oval_mask((256, 256, 3), blur=0.3)
            self.assertEqual(mask.shape, (256, 256))
            # Center of ellipse is 1.0
            self.assertEqual(mask[128, 128], 1.0)
            # Corners are 0.0
            self.assertEqual(mask[5, 5], 0.0)
            self.assertEqual(mask[250, 250], 0.0)

if __name__ == '__main__':
    unittest.main()

