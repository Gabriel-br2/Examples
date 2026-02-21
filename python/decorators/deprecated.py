import functools
from typing import Callable, Any, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])

def deprecated(reason: str = "This feature will be removed in future versions") -> Callable[[F], F]:
    """It issues a warning when the function is called."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"\n[DEPRECATED] The function '{func.__name__}' is deprecated. Reason: {reason}\n",)
    
            return func(*args, **kwargs)
        return cast(F, wrapper)
    return decorator


if __name__ == "__main__":
    @deprecated(reason="old version, Use 'new_function' instead.")
    def old_function(x: int) -> int:
        """Example of a deprecated function."""
        return x * 2

    print(old_function(5))