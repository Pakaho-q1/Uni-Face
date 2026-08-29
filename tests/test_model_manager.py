import os
import unittest
import tempfile
import hashlib
from uniface.core.model_manager import calculate_hash

class TestModelManager(unittest.TestCase):
    def test_calculate_hash(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"UniFace Model Verification Content")
            f_path = f.name
            
        try:
            expected_hash = hashlib.sha256(b"UniFace Model Verification Content").hexdigest()
            computed_hash = calculate_hash(f_path)
            self.assertEqual(computed_hash, expected_hash)
        finally:
            if os.path.exists(f_path):
                os.remove(f_path)

if __name__ == '__main__':
    unittest.main()
