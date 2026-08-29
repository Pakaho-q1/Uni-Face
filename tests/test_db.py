import os
import unittest
import tempfile
from unittest.mock import patch

from uniface.core import db

class TestDeduplicationDB(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp_dir.name, "test_uniface.db")
        # Patch the database path for isolation
        self.patcher = patch.object(db, "_db_path", self.db_path)
        self.patcher.start()
        db.init_db()

    def tearDown(self):
        self.patcher.stop()
        self.tmp_dir.cleanup()

    def test_register_and_get_hash(self):
        file_hash = "abc123md5hash"
        pool_path = "/workspace/target_sets/.pool/abc123md5hash.jpg"
        size = 1048576
        
        # Initially not found
        self.assertIsNone(db.get_hash_path(file_hash))
        
        # Register hash
        db.register_hash(file_hash, pool_path, size)
        
        # Now found
        retrieved_path = db.get_hash_path(file_hash)
        self.assertEqual(retrieved_path, pool_path)

    def test_remove_hash(self):
        file_hash = "delete_test_hash"
        pool_path = "/workspace/target_sets/.pool/delete_test.jpg"
        
        db.register_hash(file_hash, pool_path, 2048)
        self.assertEqual(db.get_hash_path(file_hash), pool_path)
        
        # Remove hash
        db.remove_hash(file_hash)
        self.assertIsNone(db.get_hash_path(file_hash))

    def test_duplicate_registration_ignored(self):
        file_hash = "dup_test_hash"
        db.register_hash(file_hash, "/path1.jpg", 100)
        db.register_hash(file_hash, "/path2.jpg", 200) # Should be ignored by INSERT OR IGNORE
        
        self.assertEqual(db.get_hash_path(file_hash), "/path1.jpg")

if __name__ == '__main__':
    unittest.main()
