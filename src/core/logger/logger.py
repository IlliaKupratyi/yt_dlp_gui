"""
Application logger
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from src.core.config.config import LOG_DIR

def setup_logger(
        name: str = "yt_dlp_gui",
        level: int = logging.INFO,
        log_to_console: bool = True,
        max_file_size: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 3
) -> logging.Logger:
    """Configure a logger with file rotation and optional console output."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if logger already configured
    if logger.hasHandlers():
        return logger

    # Ensure log directory exists
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    # Standard log format
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)s:%(funcName)s:%(lineno)d — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Rotating file handler (10 MB max, keep 3 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_file_size,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Optional console output
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


    return logger
