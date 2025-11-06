"""Logging configuration."""

import logging
from pathlib import Path
from typing import Optional, Union


class CustomLoggingFormatter(logging.Formatter):
    """Custom logging formatter to change 'ERROR' to 'SEVERE', and 'CRITICAL' to 'FATAL'.

    This is to be consistent with logging levels in ngen and ngen-cal.

    """

    def format(self, record):
        """Format the log record."""
        if record.levelno == logging.ERROR:
            record.levelname = "SEVERE"
        elif record.levelno == logging.CRITICAL:
            record.levelname = "FATAL"
        return super().format(record)


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    file_level: Optional[int] = None,
):
    """Configure logging for specific packages with optional file output.

    Args:
        level: Logging level for console output (default: INFO).
        log_file: Optional path to a file where logs will be written.
        file_level: Logging level for file output (default: same as console level).

    """
    user_log_levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "warn": logging.WARNING,
        "error": logging.ERROR,
        "severe": logging.ERROR,
        "fatal": logging.CRITICAL,
        "critical": logging.CRITICAL,
    }

    level = user_log_levels.get(level.strip().lower(), logging.INFO)
    file_level = (
        user_log_levels.get(file_level.strip().lower(), level) if file_level else level
    )

    # Set root logger to WARNING to suppress noisy external logs
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)

    # Remove existing handlers to avoid duplication
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Formatter shared by all handlers
    formatter = CustomLoggingFormatter(
        "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    # Optional file handler
    file_handler = None
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(file_level or level)

    # Apply handlers to  package
    logger = logging.getLogger("nwm_region_mgr")
    logger.setLevel(min(level, file_level or level))  # Allow lower thresholds
    # Apply handlers to package
    logger = logging.getLogger("nwm_region_mgr")
    logger.setLevel(min(level, file_level or level))  # Allow lower thresholds

    # Remove existing handlers for the logger to avoid duplication
    # (e.g., when both formulation and parameter regionalizations are run)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    # Remove existing handlers for the logger to avoid duplication
    # (e.g., when both formulation and parameter regionalizations are run)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.addHandler(console_handler)
    if file_handler:
        logger.addHandler(file_handler)
    logger.propagate = False  # Prevent duplication through root logger
    logger.addHandler(console_handler)
    if file_handler:
        logger.addHandler(file_handler)
    logger.propagate = False  # Prevent duplication through root logger
