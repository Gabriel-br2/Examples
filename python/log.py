"""
Advanced Debug and Logging System.
DEV      : Gabriel Rocha de Souza
PROJECT  : Digital Twin / DensoPy
"""

import os
import time
import logging
import inspect
import functools
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Any, Callable, Dict, Type, Optional
from types import TracebackType

from rich.logging import RichHandler

class HandleDebug:
    """
    Implements the Borg (Monostate) pattern.
    Ensures that no matter how many times or in how many different files 
    you instantiate HandleDebug(), they all share the exact same logging pipeline.
    Prevents duplicate logs and file permission crashes.
    """
    _shared_state: Dict[str, Any] = {}

    def __init__(self, name: str = "example", file_name: str = "LOG/example_debug.log"):
        self.__dict__ = self._shared_state
        
        if not hasattr(self, 'is_initialized'):
            self.MEASURE_PERFORMANCE: bool = True
            
            log_path = Path(file_name)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            self.log = logging.getLogger(f"{name}_core")
            self.log.setLevel(logging.DEBUG)

            self.log.propagate = False

            if self.log.hasHandlers():
                self.log.handlers.clear()

            fmt = logging.Formatter("%(asctime)s | %(levelname)-8s - %(name)s - %(message)s")

            console_handler = RichHandler(
                level=logging.INFO,
                show_path=True,
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                markup=True,
            )

            file_handler = RotatingFileHandler(
                filename=file_name, 
                maxBytes=5 * 1024 * 1024, # 5 MB
                backupCount=3,            # Keep 3 old files
                encoding="utf-8"
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(fmt)

            self.log.addHandler(console_handler)
            self.log.addHandler(file_handler)

            self.log.debug(f"{'='*15} System Logger Initialized {'='*15}")
            self.is_initialized = True


class LogHardwareOperation:
    """
    A context manager designed to track the lifecycle of critical code blocks.
    It automatically logs entries, successful exits, and safely captures exceptions.
    """
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.logger = HandleDebug().log
        self.start_time = 0.0

    def __enter__(self) -> None:
        self.start_time = time.perf_counter()
        self.logger.info(f"▶️ [START] Hardware Operation: '{self.operation_name}' initiated.")

    def __exit__(
        self, 
        exc_type: Optional[Type[BaseException]], 
        exc_val: Optional[BaseException], 
        exc_tb: Optional[TracebackType]
    ) -> bool:
        
        elapsed = time.perf_counter() - self.start_time
        
        if exc_type is not None:
            self.logger.error(f"❌ [FAILED] Operation '{self.operation_name}' crashed after {elapsed:.2f}s!")
            self.logger.exception(f"Exception details for '{self.operation_name}':")
            return False 
            
        self.logger.info(f"⏹️ [SUCCESS] Operation '{self.operation_name}' completed safely in {elapsed:.2f}s.")
        return True


if __name__ == "__main__":
    
    sys_logger_1 = HandleDebug()
    sys_logger_2 = HandleDebug(name="this_name_will_be_ignored", file_name="ignored.log")
    
    sys_logger_2.log.info("This log entry was written by sys_logger_2, but uses sys_logger_1's setup.")

    
    with LogHardwareOperation("MOVE_ARM_TO_HOME_POSITION"):
        sys_logger_1.log.debug("Sending joint coordinates over TCP...")
        time.sleep(0.4)
        sys_logger_1.log.debug("Coordinates received. Actuators engaging.")


    print("\nForcing a hardware fault to test exception logging...")
    try:
        with LogHardwareOperation("ENGAGE_END_EFFECTOR"):
            sys_logger_1.log.debug("Attempting to close gripper...")
            time.sleep(0.2)
            
            raise RuntimeError("Collision detected on axis 6!")
    except RuntimeError:
        pass 