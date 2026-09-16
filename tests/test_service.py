import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from uniface.core.types import Face
from uniface.core.service import FaceService

class TestFaceService(unittest.TestCase):
    
    @patch('uniface.core.service.composite')
    @patch('uniface.core.service.restore')
    @patch('uniface.core.service.swap')
    @patch('uniface.core.service.detect')
    def test_process_image_success(self, mock_detect, mock_swap, mock_restore, mock_composite):
        # Setup mock faces
        mock_source_face = Face(
            bbox=np.array([0, 0, 100, 100]),
            landmark_5=np.zeros((5, 2)),
            landmark_106=np.zeros((68, 2)),
            embedding=np.zeros((512,))
        )
        
        mock_target_face = Face(
            bbox=np.array([50, 50, 150, 150]),
            landmark_5=np.zeros((5, 2)),
            landmark_106=np.zeros((68, 2)),
            embedding=np.zeros((512,))
        )
        
        # mock_detect will return a list with one face for source, and one for target
        # Since it's called twice, we use side_effect
        mock_detect.side_effect = [[mock_source_face], [mock_target_face]]
        
        # mock_swap and mock_restore return dummy images
        dummy_swapped = np.zeros((200, 200, 3), dtype=np.uint8)
        dummy_restored = np.ones((200, 200, 3), dtype=np.uint8) * 128
        dummy_composite = np.ones((200, 200, 3), dtype=np.uint8) * 255
        
        mock_swap.return_value = dummy_swapped
        mock_restore.return_value = dummy_restored
        mock_composite.return_value = dummy_composite
        
        service = FaceService()
        from uniface.core.state import state
        state.processors = ['swap', 'restore', 'color']
        
        source_img = np.zeros((200, 200, 3), dtype=np.uint8)
        target_img = np.zeros((200, 200, 3), dtype=np.uint8)
        
        # Execute
        result_img = service.process_image(source_img, target_img)
        
        # Assertions
        self.assertEqual(mock_detect.call_count, 2)
        self.assertEqual(mock_swap.call_count, 1)
        self.assertEqual(mock_restore.call_count, 1)
        self.assertEqual(mock_composite.call_count, 1)
        
        # Result should be the composite image
        np.testing.assert_array_equal(result_img, dummy_composite)

    @patch('uniface.core.service.detect')
    def test_process_image_no_source_face(self, mock_detect):
        # If source has no face
        mock_detect.return_value = []
        
        service = FaceService()
        source_img = np.zeros((200, 200, 3), dtype=np.uint8)
        target_img = np.ones((200, 200, 3), dtype=np.uint8) * 128
        
        result_img = service.process_image(source_img, target_img)
        
        # Should return target img unchanged
        np.testing.assert_array_equal(result_img, target_img)
        self.assertEqual(mock_detect.call_count, 1)

    @patch('uniface.core.service.composite')
    @patch('uniface.core.service.restore')
    @patch('uniface.core.service.swap')
    @patch('uniface.core.service.detect')
    def test_process_image_with_job_config(self, mock_detect, mock_swap, mock_restore, mock_composite):
        from uniface.core.types import JobConfig
        from uniface.core.state import state
        
        # Set global state to everything
        state.processors = ['swap', 'restore', 'color']
        
        mock_source_face = Face(bbox=np.array([0, 0, 100, 100]), embedding=np.zeros((512,)))
        mock_target_face = Face(bbox=np.array([50, 50, 150, 150]), embedding=np.zeros((512,)))
        mock_detect.side_effect = [[mock_source_face], [mock_target_face]]
        
        dummy_swapped = np.zeros((200, 200, 3), dtype=np.uint8)
        mock_swap.return_value = dummy_swapped
        
        service = FaceService()
        source_img = np.zeros((200, 200, 3), dtype=np.uint8)
        target_img = np.zeros((200, 200, 3), dtype=np.uint8)
        
        # Create an isolated JobConfig with ONLY 'swap' processor
        custom_config = JobConfig(
            processors=['swap'],
            swap_model="hyperswap_1a_256",
            swap_weight=0.8
        )
        
        result_img = service.process_image(source_img, target_img, job_config=custom_config)
        
        # Only swap should have been called, NOT restore or composite
        self.assertEqual(mock_swap.call_count, 1)
        self.assertEqual(mock_restore.call_count, 0)
        self.assertEqual(mock_composite.call_count, 0)
        
        # Global state was NOT mutated
        self.assertEqual(state.processors, ['swap', 'restore', 'color'])

    def test_filter_and_sort_target_faces(self):
        from uniface.core.service import filter_and_sort_target_faces
        
        # Create test faces:
        # face1: Female (gender=0), bbox [10, 10, 50, 50] (area=1600), score=0.9
        # face2: Male (gender=1), bbox [100, 100, 200, 200] (area=10000), score=0.7
        # face3: Female (gender=0), bbox [300, 50, 350, 100] (area=2500), score=0.95
        f1 = Face(bbox=np.array([10, 10, 50, 50]), score=0.9, gender=0)
        f2 = Face(bbox=np.array([100, 100, 200, 200]), score=0.7, gender=1)
        f3 = Face(bbox=np.array([300, 50, 350, 100]), score=0.95, gender=0)
        
        faces = [f1, f2, f3]
        
        # Test 1: Gender Filter Female + Largest
        res = filter_and_sort_target_faces(faces, gender_filter="female", face_order="largest")
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], f3) # Area 2500 vs 1600
        
        # Test 2: Gender Filter Male
        res = filter_and_sort_target_faces(faces, gender_filter="male", face_order="largest")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], f2)
        
        # Test 3: Face Order Smallest
        res = filter_and_sort_target_faces(faces, gender_filter="all", face_order="smallest")
        self.assertEqual(res[0], f1) # Area 1600
        
        # Test 4: Face Order Highest Score
        res = filter_and_sort_target_faces(faces, gender_filter="all", face_order="highest_score")
        self.assertEqual(res[0], f3) # Score 0.95
        
        # Test 5: Face Order Left to Right
        res = filter_and_sort_target_faces(faces, gender_filter="all", face_order="left_to_right")
        self.assertEqual(res[0], f1) # X=10
        
        # Test 6: Face Order Right to Left
        res = filter_and_sort_target_faces(faces, gender_filter="all", face_order="right_to_left")
        self.assertEqual(res[0], f3) # X=300

    @patch('uniface.core.service.restore')
    @patch('uniface.core.service.swap')
    @patch('uniface.core.service.detect')
    def test_process_image_dual_stage_swap(self, mock_detect, mock_swap, mock_restore):
        from uniface.core.types import JobConfig
        
        mock_source_face = Face(bbox=np.array([0, 0, 100, 100]), embedding=np.zeros((512,)))
        mock_target_face = Face(bbox=np.array([50, 50, 150, 150]), embedding=np.zeros((512,)))
        mock_detect.side_effect = [[mock_source_face], [mock_target_face]]
        
        mock_swap.return_value = np.zeros((200, 200, 3), dtype=np.uint8)
        mock_restore.return_value = np.ones((200, 200, 3), dtype=np.uint8) * 128
        
        service = FaceService()
        source_img = np.zeros((200, 200, 3), dtype=np.uint8)
        target_img = np.zeros((200, 200, 3), dtype=np.uint8)
        
        cfg = JobConfig(
            processors=['swap'],
            swap_model="inswapper_128",
            swap_weight=0.6,
            dual_swap=True,
            swap_model_2="hyperswap_high_512",
            swap_weight_2=0.85,
            stage1_restore=False,
            stage2_restore=False
        )
        
        _ = service.process_image(source_img, target_img, job_config=cfg)
        
        # mock_swap should be called twice!
        self.assertEqual(mock_swap.call_count, 2)
        # Stage 1 call arguments:
        call_1_kwargs = mock_swap.call_args_list[0][1]
        self.assertEqual(call_1_kwargs["swap_model"], "inswapper_128")
        self.assertEqual(call_1_kwargs["swap_weight"], 0.6)
        
        # Stage 2 call arguments:
        call_2_kwargs = mock_swap.call_args_list[1][1]
        self.assertEqual(call_2_kwargs["swap_model"], "hyperswap_high_512")
        self.assertEqual(call_2_kwargs["swap_weight"], 0.85)

    @patch('uniface.core.service.restore')
    @patch('uniface.core.service.swap')
    @patch('uniface.core.service.detect')
    def test_process_image_staged_restore(self, mock_detect, mock_swap, mock_restore):
        from uniface.core.types import JobConfig
        
        mock_source_face = Face(bbox=np.array([0, 0, 100, 100]), embedding=np.zeros((512,)))
        mock_target_face = Face(bbox=np.array([50, 50, 150, 150]), embedding=np.zeros((512,)))
        mock_detect.side_effect = [[mock_source_face], [mock_target_face]]
        
        mock_swap.return_value = np.zeros((200, 200, 3), dtype=np.uint8)
        mock_restore.return_value = np.ones((200, 200, 3), dtype=np.uint8) * 128
        
        service = FaceService()
        source_img = np.zeros((200, 200, 3), dtype=np.uint8)
        target_img = np.zeros((200, 200, 3), dtype=np.uint8)
        
        cfg = JobConfig(
            processors=['swap', 'restore'],
            swap_model="inswapper_128",
            swap_weight=0.6,
            stage1_restore=True,
            restore_model="gfpgan_1.4",
            restore_weight=0.5,
            dual_swap=True,
            swap_model_2="hyperswap_high_512",
            swap_weight_2=0.8,
            stage2_restore=True,
            restore_model_2="gpen_bfr_256",
            restore_weight_2=0.9
        )
        
        _ = service.process_image(source_img, target_img, job_config=cfg)
        
        # 2 swaps and 2 restores!
        self.assertEqual(mock_swap.call_count, 2)
        self.assertEqual(mock_restore.call_count, 2)
        
        # Stage 1 restore call:
        res_call_1_kwargs = mock_restore.call_args_list[0][1]
        self.assertEqual(res_call_1_kwargs["restore_model"], "gfpgan_1.4")
        self.assertEqual(res_call_1_kwargs["weight"], 0.5)
        
        # Stage 2 restore call:
        res_call_2_kwargs = mock_restore.call_args_list[1][1]
        self.assertEqual(res_call_2_kwargs["restore_model"], "gpen_bfr_256")
        self.assertEqual(res_call_2_kwargs["weight"], 0.9)

    @patch('uniface.core.service.restore')
    @patch('uniface.core.service.swap')
    @patch('uniface.core.service.detect')
    def test_process_image_dual_swap_with_face_boost_and_source_restore(self, mock_detect, mock_swap, mock_restore):
        from uniface.core.types import JobConfig
        
        mock_source_face = Face(bbox=np.array([0, 0, 100, 100]), landmark_5=np.array([[10, 10], [20, 10], [15, 15], [12, 20], [18, 20]]), embedding=np.ones((512,)))
        mock_target_face = Face(bbox=np.array([50, 50, 150, 150]), landmark_5=np.array([[60, 60], [80, 60], [70, 75], [65, 90], [75, 90]]), embedding=np.zeros((512,)))
        mock_detect.side_effect = [[mock_source_face], [mock_target_face]]
        
        mock_swap.return_value = np.ones((200, 200, 3), dtype=np.uint8) * 100
        
        service = FaceService()
        source_img = np.zeros((200, 200, 3), dtype=np.uint8)
        target_img = np.zeros((200, 200, 3), dtype=np.uint8)
        
        cfg = JobConfig(
            processors=['swap'],
            swap_model="inswapper_128",
            swap_weight=0.6,
            dual_swap=True,
            swap_model_2="hyperswap_high_512",
            swap_weight_2=0.8,
            face_boost="512",
            restore_source_face=False,
            target_hair_protect=True
        )
        
        result = service.process_image(source_img, target_img, job_config=cfg)
        
        # Dual swap executed twice cleanly with face_boost forwarded
        self.assertEqual(mock_swap.call_count, 2)
        stage1_kwargs = mock_swap.call_args_list[0][1]
        self.assertEqual(stage1_kwargs["swap_model"], "inswapper_128")
        self.assertEqual(stage1_kwargs["face_boost"], "512")
        self.assertTrue(stage1_kwargs["target_hair_protect"])
        
        stage2_kwargs = mock_swap.call_args_list[1][1]
        self.assertEqual(stage2_kwargs["swap_model"], "hyperswap_high_512")
        self.assertEqual(stage2_kwargs["face_boost"], "512")
        self.assertTrue(stage2_kwargs["target_hair_protect"])
        
        # target_face landmarks remain pure
        np.testing.assert_array_equal(mock_target_face.landmark_5, np.array([[60, 60], [80, 60], [70, 75], [65, 90], [75, 90]]))

if __name__ == '__main__':
    unittest.main()
