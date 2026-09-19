"""
日志工具
"""
import logging
from datetime import datetime
from config.config import LOGS_DIR, LOG_LEVEL

_log_file = LOGS_DIR / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def get_logger(name: str = "weather-center") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    if logger.handlers:
        return logger
    ch = logging.StreamHandler()
    ch.setFormatter(_formatter)
    logger.addHandler(ch)
    fh = logging.FileHandler(_log_file, encoding="utf-8")
    fh.setFormatter(_formatter)
    logger.addHandler(fh)
    return logger
