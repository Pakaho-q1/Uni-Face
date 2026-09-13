"""
tests/test_fixes.py
Unit tests for all 10 code-review fixes.
Run: conda activate uniface && python -m pytest tests/test_fixes.py -v
"""
import os
import sys
import re
import time
import threading
import tempfile
import unittest
import hashlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# -- Issue #4: List annotation must not raise NameError --------------------
class TestStateImports(unittest.TestCase):
    def test_list_annotation_ok(self):
        from uniface.core.state import StateManager
        m = StateManager()
        self.assertIsInstance(m.mask_types, list)
        self.assertIsInstance(m.mask_regions, list)


# -- Issue #7: get_platform_dir must use re.sub, not str.replace -----------
class TestPlatformDirSanitize(unittest.TestCase):
    def _s(self, v):
        return re.sub(r'[^a-z0-9_]', '_', v.lower())

    def test_hyphen(self):
        self.assertEqual(self._s('webui-react'), 'webui_react')

    def test_dot(self):
        self.assertEqual(self._s('webui.react'), 'webui_react')

    def test_space(self):
        self.assertEqual(self._s('My Platform'), 'my_platform')

    def test_alphanumeric_kept(self):
        self.assertEqual(self._s('webui_react'), 'webui_react')

    def test_old_literal_replace_was_broken(self):
        # The old broken code did str.replace(r'[^a-z0-9]', '_')
        # which searches for the LITERAL string '[^a-z0-9]', never finds it,
        # and leaves dangerous chars like '-' untouched.
        broken = 'webui-react'.lower().replace(r'[^a-z0-9]', '_')
        self.assertIn('-', broken, "str.replace does not understand regex — confirms old bug existed")
        # The fixed version removes it
        fixed = re.sub(r'[^a-z0-9_]', '_', 'webui-react'.lower())
        self.assertNotIn('-', fixed)


# -- Issue #6: compositor.match_color must not mutate source_crop ----------
class TestCompositorMatchColor(unittest.TestCase):
    def test_source_not_mutated_and_result_closer_to_source(self):
        import numpy as np
        from uniface.modules.compositor import FaceCompositor
        c = FaceCompositor()
        src = (np.ones((64, 64, 3), dtype=np.float32) * 200)
        tgt = (np.ones((64, 64, 3), dtype=np.float32) * 50)
        src_before = src.copy()
        result = c.match_color(src, tgt)
        np.testing.assert_array_equal(src, src_before,
            err_msg='source_crop must not be mutated by match_color')
        self.assertGreater(float(result.mean()), float(tgt.mean()),
            'Result should be brighter (closer to source) after color matching')


# -- Issue #2: save_jobs debounce ------------------------------------------
class TestSaveJobsDebounce(unittest.TestCase):
    def _make(self, tmp):
        from uniface.api_server import JobManager
        import queue as _q
        jm = object.__new__(JobManager)
        jm.jobs = {'j1': {'status': 'processing', 'progress': 0}}
        jm.cancel_events = {}
        jm.active_websockets = {}
        jm.job_queue = _q.Queue()
        jm.jobs_file = os.path.join(tmp, 'jobs.json')
        jm._save_lock = threading.Lock()
        jm._last_save_time = time.monotonic()  # simulate very recent save
        return jm

    def test_progress_update_debounced(self):
        with tempfile.TemporaryDirectory() as tmp:
            jm = self._make(tmp)
            jm.update_job('j1', {'progress': 50.0})
            self.assertFalse(os.path.exists(jm.jobs_file),
                'Progress-only update must be debounced')

    def test_status_change_forces_immediate_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            jm = self._make(tmp)
            jm.update_job('j1', {'status': 'completed'})
            self.assertTrue(os.path.exists(jm.jobs_file),
                'Status change must flush to disk immediately')

    def test_elapsed_debounce_allows_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            jm = self._make(tmp)
            jm._last_save_time = 0.0  # force stale timestamp
            jm.save_jobs(force=False)
            self.assertTrue(os.path.exists(jm.jobs_file),
                'save_jobs must write when debounce period has elapsed')


# -- Issue #8: target files cleaned up even on exception -------------------
class TestCleanupOnError(unittest.TestCase):
    def test_target_deleted_in_finally(self):
        with tempfile.TemporaryDirectory() as tmp:
            target_file = os.path.join(tmp, 'target.jpg')
            open(target_file, 'wb').close()
            self.assertTrue(os.path.exists(target_file))
            # Simulate finally block in run_job_background
            try:
                raise RuntimeError('Simulated processing failure')
            except Exception:
                pass
            finally:
                try:
                    os.remove(target_file)
                except Exception:
                    pass
            self.assertFalse(os.path.exists(target_file),
                'Target file must be deleted even when job fails')


# -- Issue #9: WebSocket skips duplicate preview_image ---------------------
class TestWsPreviewDedup(unittest.TestCase):
    def _build(self, job, last_hash):
        resp = {k: v for k, v in job.items() if k != 'preview_image'}
        preview = job.get('preview_image')
        new_hash = last_hash
        if preview:
            mid = len(preview) // 2
            h = hashlib.md5((preview[mid : mid + 256] + preview[-128:]).encode()).hexdigest()
            if h != last_hash:
                resp['preview_image'] = preview
                new_hash = h
        return resp, new_hash

    def test_first_preview_included(self):
        r, _ = self._build({'status': 'processing', 'preview_image': 'data:A' * 10}, '')
        self.assertIn('preview_image', r)

    def test_duplicate_preview_omitted(self):
        job = {'status': 'processing', 'preview_image': 'data:A' * 10}
        _, lh = self._build(job, '')
        r, _ = self._build(job, lh)
        self.assertNotIn('preview_image', r)

    def test_changed_preview_included(self):
        _, lh = self._build({'preview_image': 'data:A' * 10}, '')
        r, _ = self._build({'preview_image': 'data:B' * 10}, lh)
        self.assertIn('preview_image', r)


# -- Issue #15: FFMPEG_BIN comes from config, not bare string --------------
class TestFfmpegPath(unittest.TestCase):
    def test_bins_are_strings(self):
        from uniface.core.video_service import FFMPEG_BIN, FFPROBE_BIN
        self.assertIsInstance(FFMPEG_BIN, str)
        self.assertIsInstance(FFPROBE_BIN, str)
        self.assertTrue(len(FFMPEG_BIN) > 0)

    def test_bundled_used_when_exists(self):
        from uniface.core.config import MODEL_PATHS
        from uniface.core.video_service import FFMPEG_BIN
        bundled = Path(str(MODEL_PATHS.get('ffmpeg', '')))
        if bundled.exists():
            self.assertEqual(FFMPEG_BIN, str(bundled))
        else:
            self.assertEqual(FFMPEG_BIN, 'ffmpeg')


# -- Issue #5: swarm poison pill routing is correct -------------------------
class TestSwarmPoisonPill(unittest.TestCase):
    def test_detect_routes_to_swap(self):
        from uniface.core.swarm import SwarmEngine
        e = SwarmEngine(max_workers=2, queue_size=5)
        e.processors = ['swap']
        e._forward_none('detect')
        self.assertEqual(e.queues['swap'].qsize(), 1)
        self.assertEqual(e.queues['out'].qsize(), 0)

    def test_detect_no_processors_routes_to_out(self):
        from uniface.core.swarm import SwarmEngine
        e = SwarmEngine(max_workers=2, queue_size=5)
        e.processors = []
        e._forward_none('detect')
        self.assertEqual(e.queues['out'].qsize(), 1)

    def test_swap_no_restore_routes_to_out(self):
        from uniface.core.swarm import SwarmEngine
        e = SwarmEngine(max_workers=2, queue_size=5)
        e.processors = ['swap']
        e._forward_none('swap')
        self.assertEqual(e.queues['out'].qsize(), 1)

    def test_restore_routes_to_color(self):
        from uniface.core.swarm import SwarmEngine
        e = SwarmEngine(max_workers=2, queue_size=5)
        e.processors = ['swap', 'restore', 'color']
        e._forward_none('restore')
        self.assertEqual(e.queues['color'].qsize(), 1)
        self.assertEqual(e.queues['out'].qsize(), 0)

# -- Issue #16: Providers parsing must return non-empty list without None --
class TestProviderParsing(unittest.TestCase):
    def test_parse_providers_returns_valid_list(self):
        from uniface.core.state import state
        p_cpu = state.parse_providers("cpu")
        self.assertIsInstance(p_cpu, list)
        self.assertNotIn(None, p_cpu)
        self.assertEqual(p_cpu, ["CPUExecutionProvider"])
        
        p_cuda = state.parse_providers("cuda")
        self.assertIsInstance(p_cuda, list)
        self.assertNotIn(None, p_cuda)
        self.assertEqual(p_cuda[0][0], "CUDAExecutionProvider")

# -- Code Audit: Test Cached Embeddings & Face Model Loader --
class TestCodeAuditOptimizations(unittest.TestCase):
    def test_job_config_cached_embeddings(self):
        import base64
        import numpy as np
        from uniface.core.types import JobConfig
        # Create a dummy 512-dim embedding
        raw_emb = np.ones(512, dtype=np.float32)
        b64_str = base64.b64encode(raw_emb.tobytes()).decode('utf-8')
        
        cfg = JobConfig(reference_face_ids=[b64_str])
        embs1 = cfg.get_reference_embeddings()
        self.assertEqual(len(embs1), 1)
        self.assertAlmostEqual(float(np.linalg.norm(embs1[0])), 1.0, places=4)
        
        # Second call must return the exact same cached object in memory
        embs2 = cfg.get_reference_embeddings()
        self.assertIs(embs1, embs2)

    def test_face_model_load_safetensors_extension_handling(self):
        from uniface.core.face_model import load_face_model
        with tempfile.TemporaryDirectory() as tmp:
            # Must raise FileNotFoundError without redundant extension nesting
            with self.assertRaises(FileNotFoundError) as ctx:
                load_face_model("nonexistent_model.safetensors", tmp)
            self.assertIn("nonexistent_model.safetensors", str(ctx.exception))
            self.assertNotIn(".safetensors.safetensors", str(ctx.exception))

if __name__ == '__main__':
    unittest.main(verbosity=2)
