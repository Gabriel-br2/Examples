from typing import Any, Dict, Type

class SingletonMeta(type):
    """
    A metaclass that restricts the instantiation of a class to one single object.
    Crucial for hardware interfaces (e.g., a serial port or a microcontroller) 
    where multiple concurrent instances would cause access collisions.
    """
    _instances: Dict[Type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            print(f"[METACLASS] Creating the very first instance of {cls.__name__}")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            print(f"[METACLASS] Returning existing instance of {cls.__name__}")
            
        return cls._instances[cls]


class SerialPortController(metaclass=SingletonMeta):
    """Only one can exist."""
    def __init__(self):
        print(" -> Initializing physical serial port connection at 115200 baud...")


if __name__ == "__main__":
    port1 = SerialPortController()
    port2 = SerialPortController()
    port3 = SerialPortController()
    
    print(f"\nAre port1 and port2 the exact same object? {port1 is port2}")
    