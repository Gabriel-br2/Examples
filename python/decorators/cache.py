
import time
import functools
from typing import Callable, Any, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])

def cache_with_ttl(ttl_seconds: int = 60) -> Callable[[F], F]:
    """Stores the result of the function for a specified time (TTL)."""

    def decorator(func: F) -> F:
        cache: dict[str, tuple[Any, float]] = {} 

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_key = str(args) + str(kwargs)
            
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if time.time() - timestamp < ttl_seconds:
                    print(f"[CACHE] Returning cached value to '{func.__name__}' (Validity: {ttl_seconds}s)")
                    return result
                else:
                    print(f"[CACHE] Cache expired for '{func.__name__}'. Recalculating...")

            result = func(*args, **kwargs)
            cache[cache_key] = (result, time.time())
            return result
        return cast(F, wrapper)
    return decorator

if __name__ == "__main__":
    @cache_with_ttl(ttl_seconds=5)
    def database_query(query: str) -> str:
        print("Consulting...")
        time.sleep(1)
        return True

    database_query("SELECT * FROM users") 
    database_query("SELECT * FROM users") 
    time.sleep(6)
    database_query("SELECT * FROM users") 