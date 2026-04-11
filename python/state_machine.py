from dataclasses import dataclass, field
from typing import Callable, Iterable
from enum import Enum, auto

type Action[C] = Callable[[C], None]

class InvalidTransition(Exception):
    pass

@dataclass
class StateMachine[S: Enum, E: Enum, C]:
    trassitions: dict[tuple[S, E], tuple[S, Action[C]]] = field(
        default_factory=dict[tuple[S, E], tuple[S, Action[C]]]
    )

    def add_transition(self, from_state: S, event: E, to_state: S, func: Action[C]) -> None:
        self.trassitions[(from_state, event)] = (to_state, func)

    def next_transition(self, state: S, event: E) -> tuple[S, Action[C]]:
        try:
            return self.trassitions[(state, event)]
        except KeyError as e:
            raise InvalidTransition(f"Cannot {event.name} from {state.name}") from e
            
    def handle(self, ctx: C, state: S, event: E) -> S:
        next_state, action = self.next_transition(state, event)
        action(ctx)
        return next_state

    def transiction(self, from_state: S | Iterable[S], event: E, to_state: S) -> Callable[[Action[C]], Action[C]]:
        if not isinstance(from_state, Iterable):
            from_state = (from_state,)
        
        def decorator(func: Action[C]) -> Action[C]:
            for s in from_state:
                self.add_transition(s, event, to_state, func)
            return func
        return decorator

#############################################################################

class PayState(Enum):
    NEW        = auto()
    AUTHORIZED = auto()
    CAPTURED   = auto()
    FAILED     = auto()
    REFUNDED   = auto()

class PayEvent(Enum):
    AUTHORIZE = auto()
    CAPTURE   = auto()
    FAIL      = auto()
    REFUND    = auto()

@dataclass
class PaymentCtx:
    payment_id: str
    audit: list[str] = field(default_factory=list[str])


pay_sm: StateMachine[PayState, PayEvent, PaymentCtx] = StateMachine()

@pay_sm.transiction(PayState.NEW, PayEvent.AUTHORIZE, PayState.AUTHORIZED)
def authorize(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id} authorized")


@pay_sm.transiction(PayState.AUTHORIZED, PayEvent.CAPTURE, PayState.CAPTURED)
def capture(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id} captured")


@pay_sm.transiction((PayState.NEW, PayState.AUTHORIZED, PayState.CAPTURED, PayState.FAILED), PayEvent.FAIL, PayState.FAILED)
def fail(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id} failed")


@pay_sm.transiction(PayState.CAPTURED, PayEvent.REFUND, PayState.REFUNDED)
def refund(ctx: PaymentCtx) -> None:
    ctx.audit.append(f"{ctx.payment_id} refunded") 


@dataclass
class Payment:
    ctx: PaymentCtx
    state: PayState = PayState.NEW

    def handle(self, event: PayEvent) -> None:
        self.state =pay_sm.handle(self.ctx, self.state, event)

def main() -> None:
    p = Payment(ctx=PaymentCtx(payment_id="p1"))
    p.handle(PayEvent.AUTHORIZE)
    p.handle(PayEvent.CAPTURE)
    p.handle(PayEvent.REFUND)

    print("final state:", p.state)
    print("audit:", p.ctx.audit)

if __name__ == "__main__":
    main()