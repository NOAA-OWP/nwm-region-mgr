"""Logging configuration."""

import logging
from pathlib import Path
from typing import Optional, Union


class CustomLoggingFormatter(logging.Formatter):
    """Custom logging formatter to rename levels."""

    LEVEL_MAP = {
        logging.ERROR: "SEVERE",
        logging.CRITICAL: "FATAL",
    }

    def format(self, record):
        record.levelname = self.LEVEL_MAP.get(record.levelno, record.levelname)
        return super().format(record)


def _normalize_level(level, default=logging.INFO):
    """Convert string/int log level to logging level."""
    if isinstance(level, int):
        return level

    if isinstance(level, str):
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
        return user_log_levels.get(level.strip().lower(), default)

    return default


def _create_handler(handler, level, formatter):
    """Apply common handler configuration."""
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def setup_logging(
    level: Union[int, str] = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    file_level: Optional[Union[int, str]] = None,
):
    """Configure logging with console and optional file output."""
    level = _normalize_level(level)
    file_level = _normalize_level(file_level, level) if file_level else level

    root_logger = logging.getLogger()
    root_logger.setLevel(min(level, file_level))

    # Clear existing handlers
    root_logger.handlers.clear()

    formatter = CustomLoggingFormatter(
        "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
    )

    # Console handler
    console_handler = _create_handler(logging.StreamHandler(), level, formatter)
    root_logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = _create_handler(
            logging.FileHandler(log_file, mode="w"),
            file_level,
            formatter,
        )
        root_logger.addHandler(file_handler)
