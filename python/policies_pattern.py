from dataclasses import dataclass
from dataclasses import field
from dataclasses import replace
from functools import reduce
from functools import wraps
from typing import Callable
from typing import Dict

type Policy = Callable[[User, Request], Request]

POLICY_REGISTRY: Dict[str, Policy] = {}


def register_policy() -> Callable:
    def decorator(func: Callable) -> Callable:
        POLICY_REGISTRY[func.__name__] = func
        return func

    return decorator


class PolicyViolationError(Exception):
    pass


@dataclass(slots=True)
class User:
    name: str
    roles: set
    has_mfa: bool
    is_active: bool
    subscription_tier: str


@dataclass(slots=True)
class Request:
    path: str
    action: str
    requires_audit: bool = False
    required_role: str | None = None
    audit_log: list[str] = field(default_factory=list)
    access_granted: bool = False


@register_policy()
def active_user(user: User, request: Request) -> Request:
    if not user.is_active:
        raise PolicyViolationError("User is not active")
    return request


@register_policy()
def mfa_required(user: User, request: Request) -> Request:
    if request.action == "delete" and not user.has_mfa:
        raise PolicyViolationError("MFA is required for delete action")
    return request


@register_policy()
def role_required(user: User, request: Request) -> Request:
    if request.required_role and request.required_role not in user.roles:
        raise PolicyViolationError(
            f"User must have {request.required_role} role to perform this action"
        )
    return request


@register_policy()
def audit(user: User, request: Request) -> Request:
    if not request.requires_audit:
        return request

    return replace(
        request,
        audit_log=request.audit_log
        + [f"User {user.name} performed {request.action} action"],
    )


@register_policy()
def grant_access(user: User, request: Request) -> Request:
    return replace(request, access_granted=True)


def policy_set(policy_names: list[str]) -> Callable:
    def decorator(func: Callable) -> Callable:
        policies_to_apply = [POLICY_REGISTRY[name] for name in policy_names]

        @wraps(func)
        def wrapper(user: User, request: Request, *args, **kwargs) -> Request:
            processed_request = reduce(
                lambda current_req, policy: policy(user, current_req),
                policies_to_apply,
                request,
            )
            return func(user, processed_request, *args, **kwargs)

        return wrapper

    return decorator


@policy_set(["active_user", "mfa_required", "role_required", "audit", "grant_access"])
def process_endpoint(user: User, request: Request) -> Request:
    # In a real application, this is where the main logic of the endpoint would be executed.
    return request


def main() -> None:
    user = User(
        name="John Doe",
        roles={"admin"},
        has_mfa=True,
        is_active=True,
        subscription_tier="free",
    )

    request = Request(
        path="/delete", action="delete", required_role="admin", requires_audit=True
    )

    request = process_endpoint(user, request)
    print(request)


if __name__ == "__main__":
    main()
