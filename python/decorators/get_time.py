import time
import functools
from typing import Callable, Any, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])

def timer(func: F) -> F:
    """Simple decorator for measuring the execution time of a function."""
    
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        print(f"[TIMER] '{func.__name__}' executed in {end_time - start_time:.6f} seconds.")
        
        return result
    return cast(F, wrapper)

if __name__ == "__main__":
    @timer
    def example_function(n: int) -> int:
        """Example function that sums numbers from 1 to n."""
        return sum(range(1, n + 1))

    print(example_function(1000000))