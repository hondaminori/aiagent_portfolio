import time
import functools
from contextlib import contextmanager
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

@contextmanager
def measure_time(label: str):
    """
    処理時間を計測する context manager

    使用例:
        with measure_time("vector_search"):
            do_search()
    """
    start = time.perf_counter()

    try:
        yield
        elapsed = (time.perf_counter() - start) * 1000
        logger.info(f"{label} completed | elapsed_ms={elapsed:.2f}")
    except Exception:
        elapsed = (time.perf_counter() - start) * 1000
        logger.exception(f"{label} failed | elapsed_ms={elapsed:.2f}")
        raise

def measure_time_decorator(label: str) -> Callable:
    """
    処理時間を計測する decorator

    使用例:
        @measure_time_decorator("ask_service")
        def ask(...):
            ...
    """
    def decorator(func: Callable) -> Callable:

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                elapsed = (time.perf_counter() - start) * 1000
                logger.info(
                    f"{label} completed | elapsed_ms={elapsed:.2f} | function={func.__name__}"
                )
                return result
            except Exception:
                elapsed = (time.perf_counter() - start) * 1000
                logger.exception(
                    f"{label} failed | elapsed_ms={elapsed:.2f} | function={func.__name__}"
                )
                raise

        return wrapper

    return decorator
