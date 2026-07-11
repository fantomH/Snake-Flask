# [+] -------------------------------------------------------------------| INFO
# [snake_permissions/decorators.py]
# description : Flask route decorators for permissions.

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar, cast

from flask import abort

from .permissions import can


F = TypeVar("F", bound=Callable[..., Any])


def permission_required(permission_name: str) -> Callable[[F], F]:
    """
    Require a permission before allowing access to a route.
    """

    def decorator(function: F) -> F:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not can(permission_name):
                abort(403)

            return function(*args, **kwargs)

        return cast(F, wrapper)

    return decorator
