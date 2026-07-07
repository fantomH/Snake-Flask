# [ INFO ] ------------------------------------------------------------------ +
# | [Snake-Flask/src/snake_flask/access/blueprints/authentication.py]
# |
# | Author      : Pascal Malouin (https://github.com/fantomH)
# | Created     : 2026-07-07 10:54:31 UTC
# | Updated     : 2026-07-07 10:54:31 UTC
# | Description : Authentication blueprints.
# + ------------------------------------------------------------------------- +

from time import time

from flask import Blueprint
from flask import g
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask import session
from flask import current_app
from werkzeug.security import check_password_hash

from snake_flask.linguae import get_language_dictionary
from snake_flask.utils import display_session
from snake_flask.utils import display_config
from snake_flask.utils import display_debug

from app.models.user import User

bp = Blueprint(
    "authentication",
    __name__,
    template_folder="../templates",
    url_prefix="/auth",
)

@bp.route("/authentication/")
def auth_routine():

    user_id = session.get("user_id", None)

    # [+] ------------------------------------------------------------------- +
    # | Login routine
    # + --------------------------------------------------------------------- +
    if user_id is None:
        return redirect(url_for("auth.login"))

    user = User.fetch_by_id(session["user_id"])
    
    if (
        current_app.config["SNAKE_ACCESS_MFA_ENABLED"]
        or current_app.config["SNAKE_ACCESS_MFA_REQUIRED"]
    ):
        if user.mfa_enabled:
            if user.mfa_secret:
                mfa_confirmed_at = session.get("mfa_confirmed_at")
                mfa_timeout = current_app.config["SNAKE_ACCESS_MFA_CONFIRM_TIMEOUT"]
                if not mfa_confirmed_at or time() - mfa_confirmed_at > mfa_timeout:
                    return redirect(url_for("mfa.verify_mfa"))
            else:
                return redirect(url_for("mfa.mfa_setup"))

    session["user_id"] = user.id
    session.permanent = True

    next_page = request.args.get("next")

    if (
        not next_page
        or not next_page.startswith("/")
        or next_page.startswith("/logout")
    ):
        next_page = url_for("index")

    return redirect(next_page)

@bp.route("/confirm-password/", methods=["GET", "POST"])
def confirm_password():

    display_language = get_language_dictionary()

    if g.current_user is None:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        password = request.form.get("password")

        if check_password_hash(g.current_user.password_hash, password):
            session["password_confirmed_at"] = time()

            next_page = request.args.get("next")

            if (
                not next_page
                or not next_page.startswith("/")
                or next_page.startswith("/logout")
            ):
                next_page = url_for("index")

            return redirect(next_page)

        flash(display_language.get("SNAKE_ACCESS_wrong_password", "Wrong password."), "danger")

    return render_template(
        "snake_access/confirm_password.html",
        title=display_language.get("SNAKE_ACCESS-confirm_password", "Confirm password"),
        display_language=display_language,
    )
