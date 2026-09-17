"""
tests/test_performance_and_optimizations.py
Tests for Uni-Face 6-phase performance and architectural optimizations.
"""
import unittest
import numpy as np
import cv2
from unittest.mock import MagicMock, patch

from uniface.modules.utils.face_math import map_mask_between_crops
from uniface.modules.utils.image_io import get_letterbox_thumbnail
from uniface.modules.swapper.base import BaseOnnxSwapper
from uniface.modules.swapper.inswapper import Inswapper
from uniface.modules.swapper.hyperswap import Hyperswap
from uniface.modules.detector import NativeDetector
from uniface.modules.restorer import FaceRestorer
from uniface.core.types import Face, JobConfig
from uniface.core.service import resolve_source_face, clear_source_face_cache


class TestPerformanceOptimizations(unittest.TestCase):
    def setUp(self):
        clear_source_face_cache()

    def test_map_mask_between_crops(self):
        # Create a mock 512x512 mask and random affine matrices
        mask_src = np.ones((512, 512), dtype=np.float32)
        # Identity matrix for src
        m_src = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=np.float32)
        # Translation matrix for dst
        m_dst = np.array([[1.0, 0.0, 10.0], [0.0, 1.0, 10.0]], dtype=np.float32)
        
        mapped = map_mask_between_crops(mask_src, m_src, m_dst, (256, 256))
        self.assertEqual(mapped.shape, (256, 256))
        self.assertEqual(mapped.dtype, np.float32)

    def test_swapper_hierarchy(self):
        # Verify Inswapper and Hyperswap inherit from BaseOnnxSwapper
        self.assertTrue(issubclass(Inswapper, BaseOnnxSwapper))
        self.assertTrue(issubclass(Hyperswap, BaseOnnxSwapper))

    def test_source_face_cache(self):
        mock_source_img = np.zeros((100, 100, 3), dtype=np.uint8)
        dummy_face = Face(
            bbox=np.array([10, 10, 50, 50]),
            score=0.99,
            embedding=np.zeros(512),
            gender=1,
            age=25
        )
        
        cfg = JobConfig()
        with patch("uniface.core.service.detect", return_value=[dummy_face]) as mock_detect:
            # First call: detects and caches
            face1 = resolve_source_face(mock_source_img, cfg)
            self.assertIsNotNone(face1)
            self.assertEqual(mock_detect.call_count, 1)

            # Second call: should hit cache and NOT invoke detect again
            face2 = resolve_source_face(mock_source_img, cfg)
            self.assertIs(face1, face2)
            self.assertEqual(mock_detect.call_count, 1)

    def test_detector_lazy_loading(self):
        detector = NativeDetector()
        # arcface_session and genderage_session should start as None
        self.assertIsNone(detector._arcface_session)
        self.assertIsNone(detector._genderage_session)

    def test_letterbox_thumbnail(self):
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            tmp_name = f.name
        try:
            img = np.zeros((300, 600, 3), dtype=np.uint8)
            cv2.imwrite(tmp_name, img)
            thumb = get_letterbox_thumbnail(tmp_name, target_size=100)
            self.assertIsNotNone(thumb)
            self.assertIsInstance(thumb, bytes)
            decoded = cv2.imdecode(np.frombuffer(thumb, dtype=np.uint8), cv2.IMREAD_COLOR)
            self.assertEqual(decoded.shape, (100, 100, 3))
        finally:
            if os.path.exists(tmp_name):
                os.remove(tmp_name)

    def test_restorer_unified_crop(self):
        restorer = FaceRestorer()
        mock_crop = np.zeros((256, 256, 3), dtype=np.uint8)
        # Mock restore_crop returning a 512x512 enhanced crop
        with patch.object(restorer, "restore_crop", return_value=np.zeros((512, 512, 3), dtype=np.uint8)) as mock_crop_fn:
            result = restorer.restore_crop(mock_crop, blend=80)
            self.assertEqual(result.shape, (512, 512, 3))
            mock_crop_fn.assert_called_once()
