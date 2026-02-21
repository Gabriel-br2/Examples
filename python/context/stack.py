from contextlib import ExitStack
from typing import List, Any

class HardwareRelay:
    """Represents a physical GPIO relay that must be turned off after use."""

    def __init__(self, pin_number: int):
        self.pin_number = pin_number

    def __enter__(self) -> 'HardwareRelay':
        print(f"[GPIO] Energizing relay on pin {self.pin_number}")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        print(f"[GPIO] De-energizing relay on pin {self.pin_number}")


def activate_multiple_relays(pins: List[int]) -> None:
    """
    Uses ExitStack to dynamically open a variable number of context managers.
    Replaces the need for deeply nested 'with' statements.
    """

    with ExitStack() as stack:
        for pin in pins:
            stack.enter_context(HardwareRelay(pin))
            
        print(f"\n[SYSTEM] Successfully initialized {len(pins)} relays simultaneously.")
        print("[SYSTEM] Performing coordinated operations...")


if __name__ == "__main__":    
    relay_pins = [12, 14, 27]
    activate_multiple_relays(relay_pins)