# [ INFO ] ------------------------------------------------------------------ +
# | [Snake-Flask/src/snake_flask/access/authentication_manager.py]            |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-07 14:37:38 UTC                                     |
# | Updated     : 2026-07-07 14:37:38 UTC                                     |
# | Description : Authentication manager.                                     |
# + ------------------------------------------------------------------------- +

from functools import wraps
from time import time

from flask import g
from flask import current_app
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from app.models.user import User

def password_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.current_user is None:
            return redirect(url_for("authentication.auth_routine", next=request.path))

        password_confirmed_at = session.get("password_confirmed_at")

        if not password_confirmed_at or time() - password_confirmed_at > current_app.config["SNAKE_ACCESS_PASSWORD_CONFIRM_TIMEOUT"]:
            return redirect(url_for("authentication.confirm_password", next=request.path))

        return view(**kwargs)

    return wrapped_view
