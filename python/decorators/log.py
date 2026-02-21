import logging
import functools
from typing import Callable, Any, TypeVar, cast

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

F = TypeVar('F', bound=Callable[..., Any])

def logger(func: F) -> F:
    """It records the input arguments and the output result."""
    
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logging.info(f"Running '{func.__name__}' with args={args}, kwargs={kwargs}")
    
        try:
            result = func(*args, **kwargs)
            logging.info(f"'{func.__name__}' returned: {result}")
            return result
        except Exception as e:
            logging.error(f"Error in '{func.__name__}': {e}")
            raise
    
    return cast(F, wrapper)


if __name__ == "__main__":
    @logger
    def add(a: int, b: int) -> int:
        return a + b

    @logger
    def divide(a: int, b: int) -> float:
        return a / b

    add(5, 3)
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass