from typing import Callable, Dict


ACTIVE_DRIVERS: Dict[str, Callable] = {}

def register_sensor(sensor_name: str) -> Callable:
    """
    Decorator that registers the driver function in the global dictionary.
    It runs at the exact moment the module is loaded into memory.
    """
    def decorator(func: Callable) -> Callable:
        ACTIVE_DRIVERS[sensor_name] = func
        return func
    return decorator