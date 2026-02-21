import time
import functools
from typing import Callable, Any, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])

def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)) -> Callable[[F], F]:
    """ It attempts to execute the function again if a specific exception is raised. """
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    
                    if attempts == max_attempts:
                        print(f"[RETRY] Final failure in '{func.__name__}' after {max_attempts} attempts.")
                        raise
                    print(f"[RETRY] Error in '{func.__name__}' ({e}). Attempt {attempts}/{max_attempts}. Waiting {delay}s...")
                    time.sleep(delay)

        return cast(F, wrapper)
    return decorator


if __name__ == "__main__":
    import random


    @retry(max_attempts=2, delay=2, exceptions=(ValueError,))
    def unstable_function() -> str:
                
        if random.random() < 0.9:  # 70% chance to fail
            raise ValueError("Random failure occurred!")
        return "Success!"

    print(unstable_function())
    