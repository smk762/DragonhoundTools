#!/usr/bin/env python3
import time
import functools
from logger import logger

def slow_down(func):
    """Sleep 1 second before calling the function"""
    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)
    return wrapper_slow_down

def print_runtime(func):
    """Prints how long function took to run"""
    @functools.wraps(func)
    def wrapper_print_runtime(*args, **kwargs):
        start = time.perf_counter()
        x = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f">>> {end-start:.3f} sec to complete {func.__name__!r}")
        return x
    return wrapper_print_runtime