import logging
import sys
from typing import Optional

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_logging_configured = False

def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None):
    """
    Configure root logging for Uni-Face with consistent formatting.
    """
    global _logging_configured
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        handlers=handlers,
        force=True
    )
    _logging_configured = True

def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger instance for the given module.
    """
    if not _logging_configured:
        setup_logging()
    return logging.getLogger(name)
