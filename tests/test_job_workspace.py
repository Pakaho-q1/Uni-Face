import os
import shutil
import tempfile
import unittest
import numpy as np
import cv2
from unittest.mock import patch

from uniface.core import db
from uniface.core.workspace import ensure_workspace, get_job_workspace, cleanup_job_workspace
from uniface.core.job_manager import (
    JobManager, JobStartRequest, generate_job_id, is_image_path,
    setup_job_hardlinks, run_job_background
)
from uniface.core.types import Face

class TestJobWorkspacePattern(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp_dir.name, "test_uniface.db")
        self.patcher = patch.object(db, "_db_path", self.db_path)
        self.patcher.start()
        db.init_db()

        self.platform = "test_ws"
        self.p_dir = os.path.join(self.tmp_dir.name, "workspace", self.platform)
        self.uploads_dir = os.path.join(self.p_dir, "uploads")
        self.outputs_dir = os.path.join(self.p_dir, "outputs")
        os.makedirs(os.path.join(self.uploads_dir, "source"), exist_ok=True)
        os.makedirs(os.path.join(self.uploads_dir, "target"), exist_ok=True)
        os.makedirs(self.outputs_dir, exist_ok=True)

        self.ws_patcher = patch("uniface.core.job_manager.ensure_workspace", return_value=(self.uploads_dir, self.outputs_dir))
        self.ws_patcher.start()
        self.pd_patcher = patch("uniface.core.job_manager.get_platform_dir", return_value=self.p_dir)
        self.pd_patcher.start()
        self.ws_mod_patcher = patch("uniface.core.workspace.get_platform_dir", return_value=self.p_dir)
        self.ws_mod_patcher.start()

        from uniface.core.job_manager import job_manager
        self.jm = job_manager
        self.jm.jobs.clear()
        self.jm.cancel_events.clear()
        self.jm.jobs_file = os.path.join(self.tmp_dir.name, "jobs.json")

    def tearDown(self):
        db.close_thread_connection()
        self.ws_mod_patcher.stop()
        self.pd_patcher.stop()
        self.ws_patcher.stop()
        self.patcher.stop()
        try:
            self.tmp_dir.cleanup()
        except Exception:
            pass

    def test_job_id_format(self):
        job_id = generate_job_id()
        self.assertNotIn("/", job_id)
        self.assertNotIn("\\", job_id)
        parts = job_id.split("_")
        self.assertEqual(len(parts), 3) # YYMMDD, HHMMSS, short_hex
        self.assertEqual(len(parts[0]), 6) # YYMMDD
        self.assertEqual(len(parts[1]), 6) # HHMMSS
        self.assertEqual(len(parts[2]), 4) # 4 hex chars

    def test_image_path_detection(self):
        self.assertTrue(is_image_path("photo.jpg"))
        self.assertTrue(is_image_path("image.PNG"))
        self.assertTrue(is_image_path("graphic.webp"))
        self.assertTrue(is_image_path("raw.jfif"))
        self.assertTrue(is_image_path("picture.avif"))
        self.assertFalse(is_image_path("clip.mp4"))
        self.assertFalse(is_image_path("movie.mkv"))

    def test_hardlink_creation_on_job_create(self):
        # Create physical dummy files in uploads
        src_path = os.path.join(self.uploads_dir, "source", "source.jpg")
        tgt_path = os.path.join(self.uploads_dir, "target", "target.webp")
        with open(src_path, "wb") as f: f.write(b"source_bytes")
        with open(tgt_path, "wb") as f: f.write(b"target_bytes")

        req = JobStartRequest(
            source_file_id="source/source.jpg",
            target_file_ids=["target/target.webp"]
        )
        job_id = self.jm.create_job(self.platform, req)
        ws = setup_job_hardlinks(self.platform, job_id, req)

        linked_src = os.path.join(ws["source_dir"], "source.jpg")
        linked_tgt = os.path.join(ws["target_dir"], "target.webp")

        self.assertTrue(os.path.exists(linked_src))
        self.assertTrue(os.path.exists(linked_tgt))
        self.assertEqual(os.path.getsize(linked_src), len(b"source_bytes"))
        self.assertEqual(os.path.getsize(linked_tgt), len(b"target_bytes"))

    def test_image_job_execution_outputs_and_cleanup(self):
        # Setup source and 2 targets (image)
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        src_path = os.path.join(self.uploads_dir, "source", "face.jpg")
        tgt1_path = os.path.join(self.uploads_dir, "target", "tgt1.jpg")
        tgt2_path = os.path.join(self.uploads_dir, "target", "tgt2.webp")
        cv2.imwrite(src_path, img)
        cv2.imwrite(tgt1_path, img)
        cv2.imwrite(tgt2_path, img)

        req = JobStartRequest(
            source_file_id="source/face.jpg",
            target_file_ids=["target/tgt1.jpg", "target/tgt2.webp"],
            skip_existing=True
        )
        job_id = self.jm.create_job(self.platform, req)
        ws = get_job_workspace(self.platform, job_id)
        job_output_dir = ws["output_dir"]

        fake_face = Face(bbox=np.array([0,0,50,50]), score=0.99)
        with patch("uniface.modules.detector.detect", return_value=[fake_face]), \
             patch("uniface.core.image_service.process_images_swarm") as mock_swarm:
            
            # Simulate swarm processing
            def fake_swarm(source, in_paths, out_paths, progress_callback, cancel_event, job_config):
                for outp in out_paths:
                    cv2.imwrite(outp, img)
            mock_swarm.side_effect = fake_swarm

            run_job_background(job_id, req, self.platform)

        # 1. Check outputs are in outputs/<job_id>/
        self.assertTrue(os.path.exists(job_output_dir))
        out_files = os.listdir(job_output_dir)
        self.assertEqual(len(out_files), 2)
        
        # 2. Check jobs/<job_id>/ was cleaned up upon completion
        self.assertFalse(os.path.exists(ws["job_dir"]))

        # 3. Check job status is completed
        job_rec = self.jm.get_job(job_id)
        self.assertEqual(job_rec["status"], "completed")
        self.assertEqual(job_rec["progress"], 100.0)

    def test_image_retry_resumes_from_checkpoint(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        src_path = os.path.join(self.uploads_dir, "source", "face.jpg")
        tgt1_path = os.path.join(self.uploads_dir, "target", "tgt1.jpg")
        tgt2_path = os.path.join(self.uploads_dir, "target", "tgt2.jpg")
        cv2.imwrite(src_path, img)
        cv2.imwrite(tgt1_path, img)
        cv2.imwrite(tgt2_path, img)

        req = JobStartRequest(
            source_file_id="source/face.jpg",
            target_file_ids=["target/tgt1.jpg", "target/tgt2.jpg"],
            skip_existing=True
        )
        job_id = self.jm.create_job(self.platform, req)
        ws = get_job_workspace(self.platform, job_id)
        job_output_dir = ws["output_dir"]

        fake_face = Face(bbox=np.array([0,0,50,50]), score=0.99)
        with patch("uniface.modules.detector.detect", return_value=[fake_face]), \
             patch("uniface.core.image_service.process_images_swarm") as mock_swarm:
            
            # 1. First run: process only target 1 then user cancels
            def fake_swarm_cancelled(source, in_paths, out_paths, progress_callback, cancel_event, job_config):
                cv2.imwrite(out_paths[0], img) # First output saved
                cancel_event.set() # User cancelled
            mock_swarm.side_effect = fake_swarm_cancelled

            run_job_background(job_id, req, self.platform)

        self.assertEqual(len(os.listdir(job_output_dir)), 1)
        self.assertTrue(os.path.exists(ws["job_dir"])) # Kept because cancelled

        # 2. User calls Retry
        with patch.object(self.jm.job_queue, "put"):
            self.jm.retry_job(job_id)
        self.assertEqual(self.jm.get_job(job_id)["status"], "pending")

        # 3. Retry run: should skip target 1 and only process target 2
        with patch("uniface.modules.detector.detect", return_value=[fake_face]), \
             patch("uniface.core.image_service.process_images_swarm") as mock_swarm_retry:
            
            def fake_swarm_retry(source, in_paths, out_paths, progress_callback, cancel_event, job_config):
                # Only 1 pending target should be passed!
                self.assertEqual(len(in_paths), 1)
                self.assertEqual(len(out_paths), 1)
                for outp in out_paths:
                    cv2.imwrite(outp, img)
            mock_swarm_retry.side_effect = fake_swarm_retry

            run_job_background(job_id, req, self.platform)

        # Now all 2 outputs exist
        self.assertEqual(len(os.listdir(job_output_dir)), 2)
        # Sandbox is cleaned up
        self.assertFalse(os.path.exists(ws["job_dir"]))
        self.assertEqual(self.jm.get_job(job_id)["status"], "completed")

    def test_delete_job_cleans_both_sandbox_and_output(self):
        req = JobStartRequest(
            source_file_id="source/f.jpg",
            target_file_ids=["target/t.jpg"]
        )
        job_id = self.jm.create_job(self.platform, req)
        ws = get_job_workspace(self.platform, job_id)
        
        # Create dummy file in outputs/<job_id>/
        out_file = os.path.join(ws["output_dir"], "dummy.jpg")
        with open(out_file, "w") as f: f.write("output")
        
        self.assertTrue(os.path.exists(ws["job_dir"]))
        self.assertTrue(os.path.exists(ws["output_dir"]))

        # Delete job
        self.jm.delete_job(job_id)

        # Both should be gone
        self.assertFalse(os.path.exists(ws["job_dir"]))
        self.assertFalse(os.path.exists(ws["output_dir"]))
        self.assertIsNone(db.get_job_record(job_id))
