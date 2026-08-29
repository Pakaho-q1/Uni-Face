import unittest
import numpy as np
from uniface.core.types import Face

class TestTypes(unittest.TestCase):
    def test_face_creation(self):
        bbox = np.array([10, 20, 110, 120])
        face = Face(bbox=bbox)
        
        np.testing.assert_array_equal(face.bbox, bbox)
        self.assertEqual(face.score, 0.0)
        self.assertIsNone(face.landmark_5)
        self.assertIsNone(face.landmark_106)
        self.assertIsNone(face.embedding)
        self.assertIsNone(face.gender)
        self.assertIsNone(face.age)
        self.assertEqual(face.attributes, {})

    def test_face_with_attributes(self):
        bbox = np.array([0, 0, 50, 50])
        emb = np.random.randn(512).astype(np.float32)
        lm5 = np.zeros((5, 2), dtype=np.float32)
        
        face = Face(
            bbox=bbox,
            score=0.95,
            landmark_5=lm5,
            embedding=emb,
            gender=1,
            age=25,
            attributes={"emotion": "happy"}
        )
        
        self.assertEqual(face.score, 0.95)
        self.assertEqual(face.gender, 1)
        self.assertEqual(face.age, 25)
        self.assertEqual(face.attributes["emotion"], "happy")
        np.testing.assert_array_equal(face.embedding, emb)

if __name__ == '__main__':
    unittest.main()
