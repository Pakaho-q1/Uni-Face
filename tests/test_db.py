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
        db.close_thread_connection()
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

    def test_job_crud_operations(self):
        # 1. Create job
        job = db.create_job_record(
            job_id="test-job-1",
            platform="web",
            status="pending",
            source_type="image",
            source_file_id="source/123.jpg",
            source_name="face.jpg",
            target_type="upload",
            target_count=2,
            target_summary="video.mp4",
            config_json='{"swap_model": "inswapper_128"}'
        )
        self.assertEqual(job["id"], "test-job-1")
        self.assertEqual(job["status"], "pending")
        self.assertEqual(job["source_name"], "face.jpg")

        # 2. Get single job
        fetched = db.get_job_record("test-job-1")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["id"], "test-job-1")
        self.assertEqual(fetched["config_json"], '{"swap_model": "inswapper_128"}')

        # 3. Update job
        db.update_job_record("test-job-1", {
            "status": "processing",
            "progress": 45.5,
            "frames_done": 45,
            "total_frames": 100
        })
        updated = db.get_job_record("test-job-1")
        self.assertEqual(updated["status"], "processing")
        self.assertEqual(updated["progress"], 45.5)

        # 4. List jobs & active count
        active_count = db.get_active_jobs_count("web")
        self.assertEqual(active_count, 1)

        jobs = db.list_job_records(platform="web")
        self.assertEqual(len(jobs), 1)

        # 5. Create another completed job
        db.create_job_record(job_id="test-job-2", platform="web", status="completed")
        self.assertEqual(db.get_jobs_count(status="completed"), 1)
        self.assertEqual(db.get_active_jobs_count("web"), 1)

        # 6. Clear completed jobs
        cleared = db.clear_completed_job_records(platform="web")
        self.assertEqual(cleared, 1)
        self.assertIsNone(db.get_job_record("test-job-2"))
        self.assertIsNotNone(db.get_job_record("test-job-1"))

        # 7. Delete specific job
        deleted = db.delete_job_record("test-job-1")
        self.assertTrue(deleted)
        self.assertIsNone(db.get_job_record("test-job-1"))

if __name__ == '__main__':
    unittest.main()

