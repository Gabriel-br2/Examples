import time
from enum import Enum, auto
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Type, Optional, Any

class Trigger(Enum):
    """Events that force the machine to change its state."""
    START_PROCESS = auto()
    OVERHEAT_DETECTED = auto()
    COOLING_FINISHED = auto()
    FINISH_PROCESS = auto()


@dataclass
class HardwareContext:
    """The central memory that all states can read and modify."""
    device_name: str
    temperature: float = 25.0
    is_active: bool = False


class BaseState(ABC):
    """Contract that forces every state to have these specific methods."""
    
    def on_enter(self, context: HardwareContext) -> None:
        """Called exactly once when the state begins."""
        pass

    def on_exit(self, context: HardwareContext) -> None:
        """Called exactly once when the state ends."""
        pass

    @abstractmethod
    def execute(self, context: HardwareContext) -> Optional[Trigger]:
        """Core logic loop. Returns a Trigger to change state, or None to stay."""
        pass


# =========================================================
# STATES (The Business Logic)
# =========================================================
class IdleState(BaseState):
    def on_enter(self, context: HardwareContext) -> None:
        print(f"\n[{context.device_name}] Entering IDLE Mode.")
        context.is_active = False

    def execute(self, context: HardwareContext) -> Optional[Trigger]:
        print(" -> Waiting for work...")
        time.sleep(0.5)
        return Trigger.START_PROCESS


class WorkingState(BaseState):
    def on_enter(self, context: HardwareContext) -> None:
        print(f"\n[{context.device_name}] Entering WORKING Mode.")
        context.is_active = True

    def execute(self, context: HardwareContext) -> Optional[Trigger]:
        context.temperature += 20.0
        print(f" -> Processing... Temperature rising to {context.temperature}C")
        time.sleep(0.5)
        
        if context.temperature >= 65.0:
            return Trigger.OVERHEAT_DETECTED
            
        return None # Continue working until an overheat or external finish trigger


class FaultState(BaseState):
    def on_enter(self, context: HardwareContext) -> None:
        print(f"\n[{context.device_name}] ALARM! OVERHEAT DETECTED. Shutting down actuators.")
        context.is_active = False # Safe state enforced

    def execute(self, context: HardwareContext) -> Optional[Trigger]:
        context.temperature -= 20.0
        print(f" -> Cooling down... Current temp: {context.temperature}C")
        time.sleep(0.5)
        
        if context.temperature <= 25.0:
            return Trigger.COOLING_FINISHED
            
        return None


# =========================================================
# 5. THE ORCHESTRATOR (Context Manager + Callable)
# =========================================================
class SynchronousStateMachine:
    """
    Manages the transitions and the execution loop.
    Contains NO business logic itself, only routing rules.
    """
    def __init__(self, context: HardwareContext):
        self.context = context
        self.current_state: BaseState = IdleState()
        
        # The routing table: CurrentState -> {Trigger -> NextState}
        self.transitions: Dict[Type[BaseState], Dict[Trigger, Type[BaseState]]] = {
            IdleState: {
                Trigger.START_PROCESS: WorkingState
            },
            WorkingState: {
                Trigger.OVERHEAT_DETECTED: FaultState,
                Trigger.FINISH_PROCESS: IdleState
            },
            FaultState: {
                Trigger.COOLING_FINISHED: IdleState
            }
        }

    def __enter__(self) -> 'SynchronousStateMachine':
        """Safely boots the hardware when entering the 'with' block."""
        print("=== SYSTEM BOOT ===")
        self.current_state.on_enter(self.context)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Guarantees safe shutdown even if the script crashes."""
        print("\n=== SYSTEM SHUTDOWN ===")
        self.current_state.on_exit(self.context)
        self.context.is_active = False
        print("[SAFETY] Hardware locked securely.")

    def trigger_transition(self, trigger: Trigger) -> None:
        """Looks up the routing table and swaps the active state class."""
        state_class = type(self.current_state)
        allowed_transitions = self.transitions.get(state_class, {})
        
        if trigger in allowed_transitions:
            next_state_class = allowed_transitions[trigger]
            
            self.current_state.on_exit(self.context)
            self.current_state = next_state_class()
            self.current_state.on_enter(self.context)
        else:
            print(f"[ERROR] Invalid trigger {trigger.name} for {state_class.__name__}")

    def __call__(self, max_ticks: int) -> None:
        """Executes the machine using the instance as a function."""
        for _ in range(max_ticks):
            trigger = self.current_state.execute(self.context)
            if trigger:
                self.trigger_transition(trigger)


if __name__ == "__main__":
    shared_memory = HardwareContext(device_name="ROBOT_ARM_ALPHA")
    
    with SynchronousStateMachine(shared_memory) as fsm:        
        fsm(max_ticks=8)