import time
from functools import wraps



def measure_time(func):
    '''
    Measure and print execution time of target function
    '''
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