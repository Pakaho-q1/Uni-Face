import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from uniface.core.types import Face
from uniface.modules.swapper.inswapper import Inswapper
from uniface.modules.swapper.hyperswap import Hyperswap
from uniface.modules.swapper.swap import get_swapper, swap

class TestSwapper(unittest.TestCase):

    @patch('uniface.modules.swapper.inswapper.onnx')
    @patch('onnxruntime.InferenceSession')
    def test_inswapper_initialization(self, mock_ort_session, mock_onnx):
        mock_model = MagicMock()
        mock_initializer = MagicMock()
        mock_model.graph.initializer = [mock_initializer]
        mock_onnx.load.return_value = mock_model
        
        swapper = Inswapper()
        
        mock_ort_session.assert_called_once()
        mock_onnx.load.assert_called_once()

    @patch('uniface.modules.parser.get_combined_mask')
    @patch('uniface.modules.swapper.inswapper.onnx')
    @patch('onnxruntime.InferenceSession')
    def test_inswapper_swap_execution(self, mock_ort_session, mock_onnx, mock_get_combined_mask):
        mock_model = MagicMock()
        mock_onnx.load.return_value = mock_model
        
        mock_onnx.numpy_helper.to_array.return_value = np.ones((512, 512), dtype=np.float32)
        
        mock_session = MagicMock()
        mock_ort_session.return_value = mock_session
        
        dummy_swapped_crop = np.zeros((3, 128, 128), dtype=np.float32)
        mock_session.run.return_value = [[dummy_swapped_crop]]
        
        mock_get_combined_mask.return_value = np.ones((128, 128), dtype=np.float32)
        
        swapper = Inswapper()
        
        source_face = Face(
            bbox=np.array([0, 0, 100, 100]),
            landmark_5=np.zeros((5, 2), dtype=np.float32),
            landmark_106=np.zeros((68, 2), dtype=np.float32),
            embedding=np.ones((512,), dtype=np.float32)
        )
        
        target_face = Face(
            bbox=np.array([50, 50, 150, 150]),
            landmark_5=np.array([[30,30], [70,30], [50,50], [40,70], [60,70]], dtype=np.float32),
            landmark_106=np.zeros((68, 2), dtype=np.float32),
            embedding=np.ones((512,), dtype=np.float32)
        )
        
        temp_vision_frame = np.zeros((200, 200, 3), dtype=np.uint8)
        
        result_frame = swapper.swap(source_face, target_face, temp_vision_frame)
        
        self.assertEqual(result_frame.shape, (200, 200, 3))
        mock_session.run.assert_called_once()
        mock_get_combined_mask.assert_called_once()

    @patch('uniface.modules.parser.get_combined_mask')
    @patch('onnxruntime.InferenceSession')
    def test_hyperswap_swap_execution(self, mock_ort_session, mock_get_combined_mask):
        mock_session = MagicMock()
        mock_ort_session.return_value = mock_session
        
        dummy_swapped_crop = np.zeros((3, 256, 256), dtype=np.float32)
        mock_session.run.return_value = [[dummy_swapped_crop]]
        mock_get_combined_mask.return_value = np.ones((256, 256), dtype=np.float32)
        
        swapper = Hyperswap()
        
        source_face = Face(
            bbox=np.array([0, 0, 100, 100]),
            landmark_5=np.zeros((5, 2), dtype=np.float32),
            landmark_106=np.zeros((68, 2), dtype=np.float32),
            embedding=np.ones((512,), dtype=np.float32)
        )
        
        target_face = Face(
            bbox=np.array([50, 50, 150, 150]),
            landmark_5=np.array([[30,30], [70,30], [50,50], [40,70], [60,70]], dtype=np.float32),
            landmark_106=np.zeros((68, 2), dtype=np.float32),
            embedding=np.ones((512,), dtype=np.float32)
        )
        
        temp_vision_frame = np.zeros((200, 200, 3), dtype=np.uint8)
        result_frame = swapper.swap(source_face, target_face, temp_vision_frame)
        
    @patch('uniface.modules.swapper.inswapper.onnx')
    @patch('onnxruntime.InferenceSession')
    def test_inswapper_handles_none_landmarks_gracefully(self, mock_ort_session, mock_onnx):
        mock_model = MagicMock()
        mock_onnx.load.return_value = mock_model
        mock_onnx.numpy_helper.to_array.return_value = np.ones((512, 512), dtype=np.float32)
        
        swapper = Inswapper()
        
        source_face = Face(bbox=np.array([0, 0, 100, 100]), embedding=np.ones((512,)))
        # Target face with None landmark_5
        target_face = Face(bbox=np.array([50, 50, 150, 150]), landmark_5=None, embedding=np.ones((512,)))
        
        temp_vision_frame = np.ones((200, 200, 3), dtype=np.uint8) * 100
        # Should gracefully return original frame without raising 'NoneType' object is not subscriptable
        result_frame = swapper.swap(source_face, target_face, temp_vision_frame)
        np.testing.assert_array_equal(result_frame, temp_vision_frame)

    @patch('uniface.modules.parser.get_combined_mask')
    @patch('uniface.modules.swapper.inswapper.onnx')
    @patch('onnxruntime.InferenceSession')
    def test_target_face_none_embedding_swaps_successfully(self, mock_ort_session, mock_onnx, mock_get_combined_mask):
        # When target_face.embedding is None, swapper should NOT abort or warn, but use 100% source embedding
        mock_model = MagicMock()
        mock_onnx.load.return_value = mock_model
        mock_onnx.numpy_helper.to_array.return_value = np.ones((512, 512), dtype=np.float32)
        mock_session = MagicMock()
        mock_ort_session.return_value = mock_session
        mock_session.run.return_value = [[np.zeros((3, 128, 128), dtype=np.float32)]]
        mock_get_combined_mask.return_value = np.ones((128, 128), dtype=np.float32)

        swapper = Inswapper()
        source_face = Face(bbox=np.array([0, 0, 100, 100]), embedding=np.ones((512,), dtype=np.float32))
        target_face = Face(
            bbox=np.array([50, 50, 150, 150]),
            landmark_5=np.array([[30,30], [70,30], [50,50], [40,70], [60,70]], dtype=np.float32),
            embedding=None  # Target embedding is None!
        )
        frame = np.zeros((200, 200, 3), dtype=np.uint8)
        result = swapper.swap(source_face, target_face, frame)
        self.assertEqual(result.shape, (200, 200, 3))
        mock_session.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
