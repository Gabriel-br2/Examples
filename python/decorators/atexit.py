import atexit
import functools
from typing import Callable, Any, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])

def run_at_exit(func: F) -> F:
    """Registers the function in the atexit module for execution upon shutdown."""
    atexit.register(func)
    
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return cast(F, wrapper)


if __name__ == "__main__":
    @run_at_exit
    def goodbye() -> None:
        print("Goodbye! This runs when the script finishes.")

    print("Hello! The script is running...")