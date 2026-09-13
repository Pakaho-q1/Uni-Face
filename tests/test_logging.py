import logging
import unittest
from uniface.core.logging import get_logger, setup_logging, resolve_log_level
from uniface.core.state import state

class TestLogging(unittest.TestCase):
    def test_get_logger(self):
        logger = get_logger("test_module")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "test_module")

    def test_setup_logging(self):
        setup_logging(level=logging.DEBUG)
        root_logger = logging.getLogger()
        self.assertEqual(root_logger.level, logging.DEBUG)

    def test_resolve_log_level(self):
        self.assertEqual(resolve_log_level("debug"), logging.DEBUG)
        self.assertEqual(resolve_log_level("info"), logging.INFO)
        self.assertEqual(resolve_log_level("warning"), logging.WARNING)
        self.assertEqual(resolve_log_level("error"), logging.ERROR)
        self.assertEqual(resolve_log_level("unknown"), logging.WARNING)
        self.assertEqual(resolve_log_level(logging.INFO), logging.INFO)

    def test_uvicorn_loggers_aligned(self):
        setup_logging(level="warning")
        for uvi in ("uvicorn", "uvicorn.error", "uvicorn.access"):
            self.assertEqual(logging.getLogger(uvi).level, logging.WARNING)

    def test_state_set_log_level(self):
        state.set_log_level("info")
        self.assertEqual(state.log_level, "info")
        self.assertEqual(logging.getLogger().level, logging.INFO)
        state.set_log_level("warning")
        self.assertEqual(state.log_level, "warning")
        self.assertEqual(logging.getLogger().level, logging.WARNING)

if __name__ == '__main__':
    unittest.main()

