import time
import tracemalloc
from functools import wraps, lru_cache

# Decorator para medir tempo e memória
def measure_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Tempo: {end - start:.6f}s, Memória pico: {peak / 1024:.2f} KiB")
        return result
    return wrapper