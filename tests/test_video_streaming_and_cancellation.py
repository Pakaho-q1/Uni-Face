"""
tests/test_video_streaming_and_cancellation.py
Test video pipe streaming, simultaneous audio, temp/retry file naming, and cancellation.
"""
import os
import shutil
import tempfile
import unittest
import subprocess
import numpy as np

from unittest.mock import patch
from uniface.core.types import JobConfig, Face
from uniface.core.video_service import (
    FFMPEG_BIN, 
    FFPROBE_BIN, 
    create_ffmpeg_encoder, 
    stream_existing_frames_to_encoder,
    process_video
)


class TestVideoStreamingAndNaming(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.tmp_dir, "outputs")
        self.job_temp_dir = os.path.join(self.tmp_dir, "jobs", "temp")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.job_temp_dir, exist_ok=True)

        # Generate a 1-second dummy audio.aac
        self.audio_file = os.path.join(self.job_temp_dir, "audio.aac")
        subprocess.run([
            FFMPEG_BIN, "-y",
            "-f", "lavfi", "-i", "sine=frequency=1000:duration=1",
            "-c:a", "aac",
            self.audio_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_simultaneous_video_audio_muxing(self):
        temp_video = os.path.join(self.output_dir, "temp_out_test.mp4")
        w, h, fps = 160, 120, 30.0
        
        proc = create_ffmpeg_encoder(
            temp_video, w, h, fps, 
            encoder="libx264", 
            audio_path=self.audio_file
        )
        
        frame = b'\x00' * (w * h * 3)
        for _ in range(15):  # 0.5 second of video
            proc.stdin.write(frame)
            
        proc.stdin.close()
        proc.wait(timeout=5)
        
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(os.path.exists(temp_video))
        self.assertGreater(os.path.getsize(temp_video), 0)

        # Verify using ffprobe that BOTH video and audio streams exist
        probe_res = subprocess.run([
            FFPROBE_BIN, "-v", "error", "-show_streams", temp_video
        ], capture_output=True, text=True, timeout=5)
        
        self.assertIn("codec_type=video", probe_res.stdout)
        self.assertIn("codec_type=audio", probe_res.stdout)

    def test_retry_fast_streaming_pass_through(self):
        # 1. Create a source partial video with 10 frames
        w, h, fps = 100, 100, 30.0
        temp_video = os.path.join(self.output_dir, "temp_sample.mp4")
        retry_video = os.path.join(self.output_dir, "retry_sample.mp4")
        
        proc1 = create_ffmpeg_encoder(temp_video, w, h, fps, encoder="libx264")
        frame = b'\x55' * (w * h * 3)
        for _ in range(10):
            proc1.stdin.write(frame)
        proc1.stdin.close()
        proc1.wait(timeout=5)
        self.assertTrue(os.path.exists(temp_video))

        # 2. Start retry_sample.mp4 and stream the 10 frames into it
        proc2 = create_ffmpeg_encoder(retry_video, w, h, fps, encoder="libx264")
        transferred = stream_existing_frames_to_encoder(temp_video, 10, proc2, w, h)
        self.assertEqual(transferred, 10)

        # 3. Add 5 more frames
        for _ in range(5):
            proc2.stdin.write(frame)
        proc2.stdin.close()
        proc2.wait(timeout=5)
        
        self.assertEqual(proc2.returncode, 0)
        self.assertTrue(os.path.exists(retry_video))
        self.assertGreater(os.path.getsize(retry_video), os.path.getsize(temp_video))

    def test_process_video_cancellation_and_retry_flow(self):
        import threading
        from unittest.mock import patch
        from uniface.core.video_service import process_video
        from uniface.core.types import JobConfig, Face

        # 1. Create a 20-frame input video
        in_v = os.path.join(self.tmp_dir, "input_source.mp4")
        out_v = os.path.join(self.output_dir, "final_output.mp4")
        
        subprocess.run([
            FFMPEG_BIN, "-y",
            "-f", "lavfi", "-i", "testsrc=size=160x120:rate=30",
            "-vframes", "20",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            in_v
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)

        cfg = JobConfig(processors=[], video_encoder="libx264")
        dummy_face = Face(bbox=np.array([0, 0, 10, 10]), score=0.99)
        cancel_event = threading.Event()

        def on_progress(cur, total, mat):
            if cur >= 8:
                cancel_event.set()

        # Step 1: Run and cancel after frame 8
        with patch("uniface.core.service.resolve_source_face", return_value=dummy_face), \
             patch("uniface.modules.detector.detect", return_value=[]):
            res = process_video(
                dummy_face, in_v, out_v,
                progress_callback=on_progress,
                cancel_event=cancel_event,
                job_config=cfg,
                job_temp_dir=self.job_temp_dir
            )

        temp_out = os.path.join(self.output_dir, "temp_final_output.mp4")
        self.assertTrue(os.path.exists(temp_out), "temp_final_output.mp4 should exist after cancellation")
        self.assertFalse(os.path.exists(out_v), "final_output.mp4 should not exist yet")
        self.assertFalse(os.path.exists(os.path.join(self.output_dir, "temp")), "outputs folder must not have temp directory")

        # Step 2: Retry with skip_existing=True to resume
        with patch("uniface.core.service.resolve_source_face", return_value=dummy_face), \
             patch("uniface.modules.detector.detect", return_value=[]):
            res_retry = process_video(
                dummy_face, in_v, out_v,
                skip_existing=True,
                job_config=cfg,
                job_temp_dir=self.job_temp_dir
            )

        self.assertTrue(os.path.exists(out_v), "final_output.mp4 should exist upon 100% completion")
        self.assertFalse(os.path.exists(temp_out), "temp_final_output.mp4 must be removed after successful retry")
        self.assertFalse(os.path.exists(os.path.join(self.output_dir, "retry_final_output.mp4")), "retry_ file must not be left behind")

    def test_process_video_with_face_model_dict(self):
        in_v = os.path.join(self.tmp_dir, "test_fm_in.mp4")
        out_v = os.path.join(self.output_dir, "test_fm_out.mp4")
        subprocess.run([
            FFMPEG_BIN, "-y",
            "-f", "lavfi", "-i", "testsrc=size=160x120:rate=30",
            "-vframes", "5",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            in_v
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)

        cfg = JobConfig(processors=[], video_encoder="libx264")
        model_dict = {"embeddings": np.ones((2, 512), dtype=np.float32)}

        with patch("uniface.modules.detector.detect", return_value=[]):
            res = process_video(
                model_dict, in_v, out_v,
                skip_existing=False,
                job_config=cfg,
                job_temp_dir=self.job_temp_dir
            )

        self.assertTrue(os.path.exists(out_v), "Output video should be created when using a face model dict")

    def test_process_video_no_face_detected_raises(self):
        in_v = os.path.join(self.tmp_dir, "test_noface_in.mp4")
        out_v = os.path.join(self.output_dir, "test_noface_out.mp4")
        subprocess.run([
            FFMPEG_BIN, "-y",
            "-f", "lavfi", "-i", "testsrc=size=160x120:rate=30",
            "-vframes", "2",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            in_v
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)

        cfg = JobConfig(processors=[], video_encoder="libx264")
        mock_source_img = np.zeros((100, 100, 3), dtype=np.uint8)

        with patch("uniface.core.service.resolve_source_face", return_value=None):
            with self.assertRaises(ValueError) as ctx:
                process_video(
                    mock_source_img, in_v, out_v,
                    job_config=cfg,
                    job_temp_dir=self.job_temp_dir
                )
            self.assertIn("No source face detected", str(ctx.exception))


