from dataclasses import dataclass, field
from typing import List, Dict
import time

@dataclass(frozen=True)
class TelemetryPacket:
    """
    A strictly immutable data structure.
    Once instantiated, its attributes cannot be modified.
    This is critical for thread safety and generating hashable objects 
    (meaning this object can be used as a dictionary key).
    """
    sensor_id: str
    temperature: float
    # Using a factory to automatically generate the timestamp at creation time,
    # rather than at class definition time.
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        """
        Runs immediately after the auto-generated __init__.
        Perfect for strict data validation.
        """
        if self.temperature < -273.15:
            # Note: Because the class is frozen, we cannot do `self.temperature = ...`
            # to fix the value. We can only raise an error or use object.__setattr__ 
            # (which breaks the frozen contract and should be avoided).
            raise ValueError(f"Invalid temperature: {self.temperature}. Cannot be below absolute zero.")


@dataclass
class IndustrialRobotState:
    """
    Manages the state of a multi-axis robot.
    Demonstrates advanced field configurations for dynamic defaults and internal caching.
    """
    axis_count: int
    
    # DANGER: Never do `joint_angles: List[float] = []`. 
    # All instances would share the exact same list in memory!
    # SOLUTION: Use default_factory to create a fresh list for each new object.
    joint_angles: List[float] = field(default_factory=list)
    
    # Internal variables that we don't want to pass in the constructor (init=False)
    # and we don't want to clutter the print output (repr=False)
    _kinematics_hash: str = field(default="", init=False, repr=False)
    
    def __post_init__(self) -> None:
        """
        Auto-populating and validating complex fields.
        """
        print(f"[SYSTEM] Initializing robot state for {self.axis_count} axes...")
        
        # If no angles were provided, initialize them to zero based on axis_count
        if not self.joint_angles:
            self.joint_angles = [0.0] * self.axis_count
            
        # Strict architecture validation
        if len(self.joint_angles) != self.axis_count:
            raise ValueError(
                f"Mismatch: Expected {self.axis_count} joint angles, "
                f"but got {len(self.joint_angles)}."
            )
            
        # Simulating the calculation of an internal state hash
        self._kinematics_hash = f"HASH_{sum(self.joint_angles)}"


if __name__ == "__main__":
    
    packet = TelemetryPacket(sensor_id="NODE_A1", temperature=25.5)
    print(f"Created Packet: {packet}")
    
    print("\nAttempting to modify the frozen packet (should fail):")
    try:
        packet.temperature = 30.0
    except Exception as e:
        print(f"Caught Exception: {type(e).__name__} - {e}")

    print("\nAttempting to create packet with invalid physics:")
    try:
        bad_packet = TelemetryPacket(sensor_id="NODE_ERR", temperature=-300.0)
    except ValueError as e:
        print(f"Caught Validation Error: {e}")


    robot_arm = IndustrialRobotState(axis_count=6)
    
    print(f"Robot State Representation:\n{robot_arm}")
    print(f"Notice the '_kinematics_hash' is hidden from the print output above.")
    print(f"But we can still access it directly: {robot_arm._kinematics_hash}")

    print("\nAttempting to initialize with a mismatched array:")
    try:
        invalid_robot = IndustrialRobotState(axis_count=6, joint_angles=[90.0, 45.0, 0.0])
    except ValueError as e:
        print(f"Caught Validation Error: {e}")