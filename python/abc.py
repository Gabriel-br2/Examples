from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseActuator(ABC):
    """
    An Abstract Base Class defines a strict contract.
    It cannot be instantiated directly. Any subclass MUST implement
    all methods decorated with @abstractmethod to be instantiated.
    """
    def __init__(self, hardware_id: str):
        self.hardware_id = hardware_id
        self._is_enabled = False

    @abstractmethod
    def set_target_position(self, position: float) -> bool:
        """Commands the actuator to move to a specific position."""
        pass

    @property
    @abstractmethod
    def current_state(self) -> Dict[str, Any]:
        """Returns the current state of the actuator (position, temperature, etc)."""
        pass

    def enable_power(self) -> None:
        """Provides default logic that subclasses can use out-of-the-box."""
        print(f"[HW_BASE] Power enabled for actuator {self.hardware_id}")
        self._is_enabled = True

    def disable_power(self) -> None:
        print(f"[HW_BASE] Power disabled for actuator {self.hardware_id}")
        self._is_enabled = False


# =========================================================
# VALID SUBCLASS
# =========================================================
class ServoMotor(BaseActuator):
    """
    A concrete implementation. It successfully overrides all abstract methods.
    """
    def __init__(self, hardware_id: str, max_angle: float):
        super().__init__(hardware_id)
        self.max_angle = max_angle
        self._current_angle = 0.0

    def set_target_position(self, position: float) -> bool:
        if not self._is_enabled:
            print(f"[SERVO] Error: Cannot move {self.hardware_id}. Power is off.")
            return False
            
        if position > self.max_angle:
            print(f"[SERVO] Error: Position {position} exceeds max angle.")
            return False
            
        print(f"[SERVO] Moving {self.hardware_id} to {position} degrees.")
        self._current_angle = position
        return True

    @property
    def current_state(self) -> Dict[str, Any]:
        return {
            "id": self.hardware_id,
            "angle": self._current_angle,
            "powered": self._is_enabled
        }


# =========================================================
# INVALID SUBCLASS
# =========================================================
class DefectiveStepperMotor(BaseActuator):
    """
    This class forgets to implement the 'current_state' property.
    Python will raise a TypeError the moment you try to create an object of this class.
    """
    def __init__(self, hardware_id: str):
        super().__init__(hardware_id)

    def set_target_position(self, position: float) -> bool:
        print(f"[STEPPER] Stepping to {position}")
        return True


# =========================================================
# EXECUTION
# =========================================================
if __name__ == "__main__":
    
    try:
        base_device = BaseActuator("GENERIC_01")
    except TypeError as e:
        print(f"Caught Expected Error: {e}")

    try:
        bad_motor = DefectiveStepperMotor("STEPPER_X")
    except TypeError as e:
        print(f"Caught Expected Error: {e}")

    robot_joint = ServoMotor(hardware_id="JOINT_1", max_angle=180.0)
    
    print("\nAttempting to move before powering on:")
    robot_joint.set_target_position(90.0)
    
    print("\nPowering on and moving:")
    robot_joint.enable_power()
    robot_joint.set_target_position(90.0)
    
    print(f"\nCurrent State: {robot_joint.current_state}")