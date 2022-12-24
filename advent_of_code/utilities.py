"""General utilities for solving the puzzles."""

import functools
import time
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def timer(func: Callable[..., T]) -> Callable[..., T]:
    """Print the runtime of the decorated function."""

    @functools.wraps(func)
    def wrapper_timer(*args: Any, **kwargs: Any) -> T:
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"run {func.__name__!r}: {run_time:.4f} s")
        return value

    return wrapper_timer
