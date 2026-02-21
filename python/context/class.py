from typing import Type, Optional
from types import TracebackType


class RobotConnection:
    """
    Manages a TCP/IP connection to an industrial robot arm.
    Ensures the device is safely locked during use and released afterward.
    """
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.is_connected = False

    def __enter__(self) -> 'RobotConnection':
        """Executed at the start of the 'with' block."""

        print(f"[TCP/IP] Initiating handshake with robot at {self.ip_address}...")
        self.is_connected = True
        print("[TCP/IP] Hardware connection established and locked.")
        
        return self

    def execute_command(self, command: str) -> None:
        if not self.is_connected:
            raise ConnectionError("Cannot send command. Robot is offline.")
        
        print(f" -> Executing: {command}")
        
        # Simulating a hardware fault during execution
        if command == "FORCE_OVERLOAD":
            raise RuntimeError("Hardware overload detected in joint 3!")

    def __exit__(
        self, 
        exc_type: Optional[Type[BaseException]], 
        exc_val: Optional[BaseException], 
        exc_tb: Optional[TracebackType]
    ) -> bool:
        
        """Executed at the end of the 'with' block, regardless of exceptions."""
        print(f"[TCP/IP] Releasing hardware lock for {self.ip_address}...")
        self.is_connected = False
        
        if exc_type is not None:
            print(f"[ALARM] Emergency Stop Triggered due to: {exc_val}")
            
            if exc_type is RuntimeError:
                print("[SYSTEM] Overload handled safely by safe-state protocol. Suppressing crash.")
                return True 
        
        return False


if __name__ == "__main__":
    
    with RobotConnection("192.168.1.116") as robot:
        robot.execute_command("MOVE_TO_HOME")
        robot.execute_command("FORCE_OVERLOAD")
        robot.execute_command("GRIPPER_CLOSE")  
