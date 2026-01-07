# common/logging_config.py
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from common.paths import LOG_DIR
import functools

def _create_log_handler() -> logging.Handler:
    """
    出力先に応じた Handler を生成
    """
    log_dest = os.getenv("LOG_DEST", "stdout")
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(target_func)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if log_dest == "file":
        app_name = os.getenv("APP_NAME", "app")

        log_path = LOG_DIR / "apps" / app_name
        log_path.mkdir(parents=True, exist_ok=True)

        handler = TimedRotatingFileHandler(
            filename=log_path / f"{app_name}.log",
            when="midnight",
            backupCount=14,
            encoding="utf-8",
        )
    else:
        handler = logging.StreamHandler()

    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    return handler


def get_logger(name: str) -> logging.Logger:
    """
    共通 logger 取得関数
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # 二重登録防止

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(log_level)

    handler = _create_log_handler()
    logger.addHandler(handler)

    logger.propagate = False
    return logger

def setup_logging() -> None:
    log_dest = os.getenv("LOG_DEST", "stdout").strip().lower()
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    app_name = os.getenv("APP_NAME", "app")

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(log_level)

    # ★既存ハンドラをクリア（これが重要）
    root.handlers.clear()

    if log_dest == "file":
        log_path = LOG_DIR / "apps" / app_name
        log_path.mkdir(parents=True, exist_ok=True)

        handler = TimedRotatingFileHandler(
            filename=log_path / f"{app_name}.log",
            when="midnight",
            backupCount=14,
            encoding="utf-8",
        )
    else:
        handler = logging.StreamHandler()

    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    root.addHandler(handler)


def log_start_end(func):
    logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"{func.__name__} を開始します")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} を終了します")
            return result
        except Exception:
            logger.exception("エラーが発生しました")
            raise

    return wrapper