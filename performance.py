import time
from functools import wraps


def measure_time(func):
    """Measure and print execution time of a function.
    Elapsed execution time is expressed in seconds.

    Args:
        A function whose execution time should be measured.
    
    Returns:
        A wrapped function that prints its execution time.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        print(
            f"{func.__name__}: "
            f"{end - start:.3f} seconds"
        )

        return result

    return wrapper