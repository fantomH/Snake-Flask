# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/access/authentication_manager.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-07 14:37:38 UTC
# Updated     : 2026-07-15 16:23:28 UTC
# Description : Authentication manager.
# +---------------------------------------------------------------------------+

from functools import wraps
from time import time

from flask import g
from flask import current_app
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from .user import User

def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.current_user = None
        return

    g.current_user = User.fetch_by_id(user_id)

def init_app(app):
    app.before_request(load_logged_in_user)

    @app.context_processor
    def inject_current_user():
        return {
            "current_user": getattr(g, "current_user", None)
        }

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.current_user is None:
            return redirect(url_for("authentication.auth_routine", next=request.path))

        return view(**kwargs)

    return wrapped_view

def password_required(view):
    """Decorator to require the user to confirm password to access a view."""

    @wraps(view)
    def wrapped_view(**kwargs):
        if g.current_user is None:
            return redirect(url_for("authentication.auth_routine", next=request.path))

        password_confirmed_at = session.get("password_confirmed_at")

        if not password_confirmed_at or time() - password_confirmed_at > current_app.config["SNAKE_ACCESS_PASSWORD_CONFIRM_TIMEOUT"]:
            return redirect(url_for("authentication.password_confirm", next=request.path))

        return view(**kwargs)

    return wrapped_view

def pin_required(view):
    """Decorator to require the user to confirm pin to access a view."""

    @wraps(view)
    def wrapped_view(**kwargs):
        if g.current_user is None:
            return redirect(url_for("authentication.auth_routine"), next=request.path)

        pin_confirmed_at = session.get("pin_confirmed_at")

        if not pin_confirmed_at or time() - pin_confirmed_at > current_app.config["SNAKE_ACCESS_PIN_CONFIRM_TIMEOUT"]:
            return redirect(url_for("pin.pin_confirm", next=request.path))

        return view(**kwargs)

    return wrapped_view
