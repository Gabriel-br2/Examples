from typing import Any, Dict, Type


class StrictDriverMeta(type):
    """
    Validates the structure of a class BEFORE it is created in memory.
    It enforces that any subclass must implement specific methods.
    If a developer forgets a method, the script crashes at IMPORT time.
    """
    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> 'StrictDriverMeta':
        if name != "BaseDeviceDriver":
            required_methods = ['connect', 'read_data']
            
            for method in required_methods:
                if method not in namespace or not callable(namespace[method]):
                    raise TypeError(f"[ARCHITECTURE ERROR] Class '{name}' is missing required method '{method}()'")
        
        
        return super().__new__(mcs, name, bases, namespace)


class BaseDeviceDriver(metaclass=StrictDriverMeta):
    """
    Base class that automatically applies the strict metaclass to 
    all hardware drivers inheriting from it.
    """
    pass


class ValidTemperatureDriver(BaseDeviceDriver):
    """This class will be created successfully because it follows the rules."""
    def connect(self) -> None:
        print("[I2C] Connected to temperature sensor.")
        
    def read_data(self) -> float:
        return 25.5


# This class will fail to be created because it does not implement the required methods.
#class InvalidJuniorDriver(BaseDeviceDriver):
#    def connect(self) -> None:
#        pass


if __name__ == "__main__":
    sensor = ValidTemperatureDriver()
    sensor.connect()
    print(f"Data received: {sensor.read_data()}")