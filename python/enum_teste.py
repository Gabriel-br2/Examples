from enum import Enum, IntEnum, IntFlag, auto
from typing import Tuple

class MotorCommand(IntEnum):
    """
    Unlike a standard Enum, an IntEnum can be directly compared to integers.
    This is extremely useful when writing to hardware registers that expect
    raw integer values (e.g., over I2C, SPI, or Serial).
    """
    STOP = 0
    MOVE_FORWARD = 1
    MOVE_BACKWARD = 2
    EMERGENCY_BRAKE = 255

class SystemFaultFlag(IntFlag):
    """
    IntFlag allows combining multiple enum members using bitwise operators.
    Each value must be a power of 2 (1, 2, 4, 8, 16...) so their binary 
    representations do not overlap.
    """
    NO_FAULT = 0          # Binary: 0000 0000
    TEMP_HIGH = 1         # Binary: 0000 0001
    PRESSURE_LOW = 2      # Binary: 0000 0010
    VIBRATION_HIGH = 4    # Binary: 0000 0100
    NETWORK_LOSS = 8      # Binary: 0000 1000
    
    CRITICAL_HARDWARE_FAILURE = TEMP_HIGH | PRESSURE_LOW | VIBRATION_HIGH


class HardwareComponent(Enum):
    """
    Enums can have custom initialization, properties, and methods.
    This maps a single concept to multiple related data points.
    """
   
    MAIN_CPU = (0x10, "Central Processing Unit", 3.3)
    MOTOR_DRIVER = (0x20, "L298N Motor Controller", 12.0)
    TEMP_SENSOR = (0x30, "DS18B20 Temperature Node", 5.0)

    def __init__(self, hex_address: int, component_name: str, voltage: float):
        self.hex_address = hex_address
        self.component_name = component_name
        self.voltage = voltage

    @property
    def is_low_voltage(self) -> bool:
        return self.voltage <= 5.0

    def get_formatted_address(self) -> str:
        return f"0x{self.hex_address:02X}"


if __name__ == "__main__":
    
    print("--- 1. Testing IntEnum ---")
    current_command = MotorCommand.MOVE_FORWARD
    print(f"Command Name: {current_command.name}")

    print(f"Is command equal to integer 1? {current_command == 1}")
    
    raw_byte_to_send = int(current_command)
    print(f"Raw byte to transmit: {raw_byte_to_send}\n")


    print("--- 2. Testing IntFlag (Bitwise Operations) ---")
    current_status = SystemFaultFlag.TEMP_HIGH | SystemFaultFlag.NETWORK_LOSS
    print(f"Combined Status Value: {int(current_status)}") # Output will be 9 (1 + 8)
    print(f"Status Representation: {repr(current_status)}")

    if SystemFaultFlag.TEMP_HIGH in current_status:
        print(" -> ALARM: High temperature detected in the combined status!")

    if SystemFaultFlag.VIBRATION_HIGH not in current_status:
        print(" -> OK: Vibration levels are normal.\n")


    print("--- 3. Testing Rich Enums ---")
    target_device = HardwareComponent.TEMP_SENSOR
    
    print(f"Device: {target_device.component_name}")
    print(f"Address: {target_device.get_formatted_address()}")
    print(f"Voltage: {target_device.voltage}V")
    print(f"Is Low Voltage Logic? {target_device.is_low_voltage}")