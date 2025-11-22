def profile_function_execution_time(func):
    import time

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
        return result

    return wrapper


def profile_memory_usage(func):
    import tracemalloc

    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Function '{func.__name__}' memory usage: Current = {current / 10**6:.4f} MB; Peak = {peak / 10**6:.4f} MB")
        return result

    return wrapper


def log_profiling_info(func):
    import logging

    logging.basicConfig(level=logging.INFO)

    def wrapper(*args, **kwargs):
        logging.info(f"Profiling function: {func.__name__}")
        result = func(*args, **kwargs)
        return result

    return wrapper