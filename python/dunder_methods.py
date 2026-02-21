import math
from typing import Union, List

class RobotVector3D:
    """
    Represents a 3D coordinate or spatial vector in robotics.
    Demonstrates overloading arithmetic and comparison operators.
    """
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Vector3D(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"

    def __add__(self, other: 'RobotVector3D') -> 'RobotVector3D':
        """Overloads the '+' operator."""
        if isinstance(other, RobotVector3D):
            return RobotVector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        
        # Returning NotImplemented tells Python to try the reverse operation (__radd__) 
        # on the other object before throwing a TypeError.
        return NotImplemented

    def __mul__(self, scalar: Union[int, float]) -> 'RobotVector3D':
        """Overloads the '*' operator for scalar multiplication."""
        if isinstance(scalar, (int, float)):
            return RobotVector3D(self.x * scalar, self.y * scalar, self.z * scalar)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        """
        Overloads the '==' operator.
        Crucial: Never use '==' directly for floats due to precision issues.
        Use math.isclose instead.
        """
        if not isinstance(other, RobotVector3D):
            return False
            
        tolerance = 1e-5
        return (math.isclose(self.x, other.x, abs_tol=tolerance) and
                math.isclose(self.y, other.y, abs_tol=tolerance) and
                math.isclose(self.z, other.z, abs_tol=tolerance))


class PIDController:
    """
    Demonstrates the __call__ method.
    It allows an instance of a class to be executed exactly like a function,
    but it retains internal state (like the accumulated integral error) 
    between calls without relying on global variables.
    """
    def __init__(self, kp: float, ki: float, kd: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self._integral = 0.0
        self._previous_error = 0.0

    def __call__(self, current_error: float, dt: float) -> float:
        """
        This method is triggered when you use the object instance with parentheses ().
        Calculates the control output based on the error.
        """
        p_term = self.kp * current_error
        
        self._integral += current_error * dt
        i_term = self.ki * self._integral
        
        derivative = (current_error - self._previous_error) / dt
        d_term = self.kd * derivative
        
        self._previous_error = current_error
        
        return p_term + i_term + d_term


class CircularSensorBuffer:
    """
    Acts just like a Python list, but keeps its memory footprint 
    capped by overwriting the oldest data when full (FIFO behavior).
    """
    def __init__(self, max_size: int):
        self.max_size = max_size
        self._buffer: List[float] = []

    def push_data(self, value: float) -> None:
        if len(self._buffer) >= self.max_size:
            self._buffer.pop(0) # Remove the oldest element
        self._buffer.append(value)

    def __len__(self) -> int:
        """Overloads the len() built-in function."""
        return len(self._buffer)

    def __getitem__(self, index: int) -> float:
        """
        Overloads the bracket operator '[]'.
        Allows accessing data like: my_buffer[2]
        """
        return self._buffer[index]


if __name__ == "__main__":
    
    print("--- 1. Testing Math Overloading ---")
    pos_initial = RobotVector3D(10.0, 5.0, 0.0)
    movement = RobotVector3D(2.0, -1.0, 5.0)
    
    # Notice how clean this is compared to pos_initial.add(movement)
    pos_final = pos_initial + movement
    print(f"Final Position after addition: {pos_final}")
    
    pos_scaled = pos_final * 2.5
    print(f"Position scaled by 2.5: {pos_scaled}")
    
    # Testing float-safe equality
    pos_copy = RobotVector3D(30.0, 10.0000001, 12.5)
    print(f"Are pos_scaled and pos_copy equal? {pos_scaled == pos_copy}")


    print("\n--- 2. Testing Callable Instances (PID Controller) ---")
    # Instantiating the object
    heater_control = PIDController(kp=1.2, ki=0.5, kd=0.1)
    
    # We are calling the object itself, triggering __call__
    output_1 = heater_control(current_error=5.0, dt=1.0)
    print(f"Control Output (Cycle 1): {output_1:.2f}")
    
    # The internal integral state is preserved between calls
    output_2 = heater_control(current_error=3.0, dt=1.0)
    print(f"Control Output (Cycle 2): {output_2:.2f}")


    print("\n--- 3. Testing Container Emulation ---")
    data_buffer = CircularSensorBuffer(max_size=3)
    
    # Pushing 4 elements into a buffer of size 3
    data_buffer.push_data(10.0)
    data_buffer.push_data(15.5)
    data_buffer.push_data(20.1)
    data_buffer.push_data(25.9) # This should push 10.0 out
    
    # Testing len()
    print(f"Buffer size: {len(data_buffer)} / {data_buffer.max_size}")
    
    # Testing [] operator
    print("Iterating over buffer using standard Python indexing:")
    for i in range(len(data_buffer)):
        print(f" -> Index {i}: {data_buffer[i]}")