# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/example/app/login_manager.py]                |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-05-20 19:48:23 UTC                                     |
# | Updated     : 2026-07-01 18:27:27 UTC                                     |
# | Description : Login Manager.                                              |
# +---------------------------------------------------------------------------+

from functools import wraps

from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from .models.user import User

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
            return redirect(url_for("auth.login", next=request.path))

        return view(**kwargs)

    return wrapped_view
