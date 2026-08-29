import logging
import unittest
from uniface.core.logging import get_logger, setup_logging

class TestLogging(unittest.TestCase):
    def test_get_logger(self):
        logger = get_logger("test_module")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "test_module")

    def test_setup_logging(self):
        setup_logging(level=logging.DEBUG)
        root_logger = logging.getLogger()
        self.assertEqual(root_logger.level, logging.DEBUG)

if __name__ == '__main__':
    unittest.main()
