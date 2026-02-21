import time
from typing import Any

class BoundedInteger:
    """
    A Data Descriptor that ensures an attribute is strictly an integer
    and falls within a specific minimum and maximum range.
    """
    def __init__(self, min_val: int, max_val: int):
        self.min_val = min_val
        self.max_val = max_val
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        # Called automatically in Python 3.6+ when the class is created.
        # It binds the descriptor to the name of the variable it was assigned to.
        self.name = name

    def __get__(self, instance: object, owner: type) -> Any:
        # If accessed from the class itself (not an instance), return the descriptor object
        if instance is None:
            return self
        
        # Retrieve the value directly from the instance's dictionary
        return instance.__dict__.get(self.name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Attribute '{self.name}' must be strictly an integer.")
        
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(
                f"Attribute '{self.name}' out of bounds. "
                f"Got {value}, expected between {self.min_val} and {self.max_val}."
            )
        
        # Store the validated value in the instance's dictionary
        instance.__dict__[self.name] = value



class MotorController:
    pwm_signal = BoundedInteger(min_val=0, max_val=255)
    steering_angle = BoundedInteger(min_val=-45, max_val=45)

    def __init__(self, initial_pwm: int, initial_angle: int):
        self.pwm_signal = initial_pwm
        self.steering_angle = initial_angle

    def complex_kinematics_matrix(self) -> list:
        """Simulates a heavy mathematical computation for robot kinematics."""
        time.sleep(1.5)
        return [[1.0, 0.5], [0.5, 1.0]]


if __name__ == "__main__":    
    motor = MotorController(initial_pwm=100, initial_angle=0)
    print(f"Current PWM: {motor.pwm_signal}")
    print(f"Current Angle: {motor.steering_angle}")
    
    print("\nAttempting to set invalid PWM value (300)...")
    try:
        motor.pwm_signal = 300
    except ValueError as e:
        print(f"Caught Exception: {e}")

    print("\nAttempting to set float instead of int for angle...")
    try:
        motor.steering_angle = 15.5
    except TypeError as e:
        print(f"Caught Exception: {e}")