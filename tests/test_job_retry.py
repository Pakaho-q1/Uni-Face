import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from uniface.core import db
from uniface.core.job_manager import JobManager, JobStartRequest

class TestJobRetryAndCleanup(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp_dir.name, "test_uniface.db")
        self.patcher = patch.object(db, "_db_path", self.db_path)
        self.patcher.start()
        db.init_db()

        self.jm = JobManager()
        self.jm.jobs_file = os.path.join(self.tmp_dir.name, "jobs.json")

    def tearDown(self):
        self.patcher.stop()
        self.tmp_dir.cleanup()

    def test_in_place_retry_job(self):
        req = JobStartRequest(
            source_file_id="source1.jpg",
            target_file_ids=["target1.mp4", "target2.mp4"]
        )
        job_id = self.jm.create_job("test_platform", req)
        
        # Simulate job failed / cancelled
        self.jm.update_job(job_id, {"status": "failed", "error": "Cancelled by user", "progress": 45.0})
        
        job_before = db.get_job_record(job_id)
        self.assertEqual(job_before["status"], "failed")
        self.assertEqual(job_before["error"], "Cancelled by user")
        
        # Retry job
        success = self.jm.retry_job(job_id)
        self.assertTrue(success)
        
        # Verify status is pending, error is None, and ID is identical (no duplicate)
        job_after = self.jm.get_job(job_id)
        self.assertEqual(job_after["id"], job_id)
        self.assertEqual(job_after["status"], "pending")
        self.assertIsNone(job_after["error"])
        
        # Verify item was added to job_queue
        queued_item = self.jm.job_queue.get_nowait()
        self.assertEqual(queued_item[0], job_id)
        self.assertEqual(queued_item[2], "test_platform")

    def test_delete_job_cleans_temp_directory(self):
        platform = "test_platform"
        req = JobStartRequest(
            source_file_id="my_source.jpg",
            target_file_ids=["video1.mp4"]
        )
        job_id = self.jm.create_job(platform, req)
        
        # Create mock output & temp directories
        with patch("uniface.core.job_manager.ensure_workspace") as mock_ws:
            outputs_dir = os.path.join(self.tmp_dir.name, "outputs")
            mock_ws.return_value = (self.tmp_dir.name, outputs_dir)
            
            # Expected temp dir name prefix: out_my_sourc_video1
            temp_dir = os.path.join(outputs_dir, "temp", "out_my_sourc_video1")
            os.makedirs(temp_dir, exist_ok=True)
            with open(os.path.join(temp_dir, "meta.json"), "w") as f:
                f.write("{}")
                
            # Create a partial video in outputs_dir
            os.makedirs(outputs_dir, exist_ok=True)
            partial_video = os.path.join(outputs_dir, "out_my_sourc_video1_30%.mp4")
            with open(partial_video, "w") as f:
                f.write("partial content")
                
            self.assertTrue(os.path.exists(temp_dir))
            self.assertTrue(os.path.exists(partial_video))
            
            # Delete job
            self.jm.delete_job(job_id)
            
            # Temp directory and partial video should be deleted
            self.assertFalse(os.path.exists(temp_dir))
            self.assertFalse(os.path.exists(partial_video))
            # Record should be gone from DB
            self.assertIsNone(db.get_job_record(job_id))


class TestJobEndpoints(unittest.TestCase):
    def setUp(self):
        from uniface.api_server import app
        from uniface.core.state import state
        import httpx
        import asyncio

        state.auth = None

        class SyncTestClient:
            def __init__(self, app):
                self.transport = httpx.ASGITransport(app=app)
            def post(self, url, **kwargs):
                async def _req():
                    async with httpx.AsyncClient(transport=self.transport, base_url="http://test") as c:
                        return await c.post(url, **kwargs)
                return asyncio.run(_req())
            def delete(self, url, **kwargs):
                async def _req():
                    async with httpx.AsyncClient(transport=self.transport, base_url="http://test") as c:
                        return await c.delete(url, **kwargs)
                return asyncio.run(_req())

        self.client = SyncTestClient(app)

    def test_retry_endpoint(self):
        from uniface.core.job_manager import job_manager
        
        req = JobStartRequest(
            source_file_id="api_src.jpg",
            target_file_ids=["api_tgt.mp4"]
        )
        job_id = job_manager.create_job("api_test", req)
        job_manager.update_job(job_id, {"status": "failed", "error": "Cancelled by user"})
        
        # Call POST /api/v1/jobs/{job_id}/retry
        res = self.client.post(f"/api/v1/jobs/{job_id}/retry", headers={"x-client-platform": "api_test"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "pending")
        self.assertEqual(data["job_id"], job_id)
        
        # Verify in DB/job_manager
        j = job_manager.get_job(job_id)
        self.assertEqual(j["status"], "pending")
        self.assertIsNone(j["error"])

        # Clean up
        job_manager.delete_job(job_id)

    def test_debug_endpoint(self):
        res = self.client.get("/api/v1/jobs/debug") if hasattr(self.client, "get") else None
        # Verify debug endpoint responds
        import httpx
        from uniface.api_server import app
        import asyncio
        async def _get():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as c:
                return await c.get("/api/v1/jobs/debug")
        res = asyncio.run(_get())
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("worker_thread_alive", data)
        self.assertIn("job_queue_size", data)
        self.assertIn("recent_jobs", data)

