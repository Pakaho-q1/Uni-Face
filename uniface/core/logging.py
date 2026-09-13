import logging
import sys
from typing import Optional, Union

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOG_LEVEL_MAP = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "warn": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

_logging_configured = False

def resolve_log_level(level: Union[int, str]) -> int:
    if isinstance(level, str):
        return LOG_LEVEL_MAP.get(level.lower().strip(), logging.WARNING)
    return level

def setup_logging(level: Union[int, str] = logging.WARNING, log_file: Optional[str] = None):
    """
    Configure root logging for Uni-Face with consistent formatting.
    Defaults to WARNING for clean console output unless --log-info or --log-debug is requested.
    """
    global _logging_configured
    numeric_level = resolve_log_level(level)
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=numeric_level,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        handlers=handlers,
        force=True
    )
    # Align uvicorn loggers so HTTP requests don't clutter terminal in clean mode
    for uvi_logger in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(uvi_logger).setLevel(numeric_level)
    _logging_configured = True

def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger instance for the given module.
    """
    if not _logging_configured:
        setup_logging()
    return logging.getLogger(name)
