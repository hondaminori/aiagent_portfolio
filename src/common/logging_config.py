from __future__ import annotations

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from common.paths import LOG_DIR
from common.config import LOG_LEVEL, LOG_DEST

import functools

class DefaultFieldsFilter(logging.Filter):
    """
    Formatterで参照する独自フィールドが無い場合にデフォルト値を注入する。
    """
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "target_func"):
            record.target_func = "-"
        return True

def setup_logging() -> None:
    """
    プロセス全体（root logger）の logging 設定を初期化する。
    - 出力先は stdout か file のどちらか
    - handler は1つだけ
    - 起動点（bootstrap）で必ず最初に呼ぶこと
    """
    # log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = LOG_LEVEL.upper()
    # log_dest = os.getenv("LOG_DEST", "stdout").strip().lower()
    log_dest = LOG_DEST.strip().lower()
    app_name = os.getenv("APP_NAME", "unknown").strip()

    root = logging.getLogger()
    root.setLevel(log_level)

    # ★既存ハンドラをクリア（これが重要）
    root.handlers.clear()

    formatter = logging.Formatter(
        # fmt="%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(target_func)s | %(message)s",
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if log_dest == "file":
        log_path = LOG_DIR / app_name
        log_path.mkdir(parents=True, exist_ok=True)

        handler = TimedRotatingFileHandler(
            filename=log_path / f"{app_name}.log",
            when="midnight",
            backupCount=14,
            encoding="utf-8",
        )

    # 今のところはfileかstdoutしか考えない。
    # file+stdoutの場合はhandlerを [] にする。
    else:
        handler = logging.StreamHandler()

    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    root.addHandler(handler)

def log_start_end(func):
    logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        extra = {"target_func": func.__name__}

        logger.info("start", extra=extra)
        try:
            result = func(*args, **kwargs)
            logger.info("end", extra=extra)
            return result
        except Exception:
            logger.exception("error", extra=extra)
            raise

    return wrapper