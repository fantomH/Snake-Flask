# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/access/blueprints/authentication.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-07 10:54:31 UTC
# Updated     : 2026-07-16 20:12:17 UTC
# Description : Authentication routes.
# +---------------------------------------------------------------------------+

from time import time

from flask import Blueprint
from flask import flash
from flask import g
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask import session
from flask import current_app
from werkzeug.security import check_password_hash

from snake_flask.access.authentication_manager import login_required
from snake_flask.linguae import get_language_dictionary
from snake_flask.utils import display_session
from snake_flask.utils import display_config
from snake_flask.utils import display_debug
from snake_vault.utils.data_validator import is_valid_password

from .. user import User

bp = Blueprint(
    "authentication",
    __name__,
    template_folder="../templates",
)

@bp.route("/auth/")
def auth_routine():

    user_id = session.get("user_id", None)

    # +-----------------------------------------------------------------------+
    # [+] Login routine
    # +-----------------------------------------------------------------------+
    if user_id is None:
        return redirect(url_for("authentication.login"))

    user = User.fetch_by_id(session["user_id"])
    
    # +-----------------------------------------------------------------------+
    # [+] MFA
    #  
    # This part takes care of setting up and login verification of MFA.
    # +-----------------------------------------------------------------------+
    if (
        current_app.config["SNAKE_ACCESS_MFA_ENABLED"]
        or current_app.config["SNAKE_ACCESS_MFA_REQUIRED"]
    ):
        if user.mfa_enabled:
            if user.mfa_secret:
                mfa_confirmed_at = session.get("mfa_confirmed_at")
                mfa_timeout = current_app.config["SNAKE_ACCESS_MFA_CONFIRM_TIMEOUT"]
                if not mfa_confirmed_at or time() - mfa_confirmed_at > mfa_timeout:
                    return redirect(url_for("mfa.mfa_verify"))
            else:
                return redirect(url_for("mfa.mfa_setup"))

    # +-----------------------------------------------------------------------+
    # [+] PIN
    # 
    # This part takes care of setting up PIN only.
    # +-----------------------------------------------------------------------+
    if (
        current_app.config["SNAKE_ACCESS_PIN_ENABLED"]
        or current_app.config["SNAKE_ACCESS_PIN_REQUIRED"]
    ):
        if user.pin_enabled:
            if not user.pin_secret:
                return redirect(url_for("pin.pin_setup"))

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

@bp.route("/password-confirmation/", methods=["GET", "POST"])
@login_required
def password_confirm():

    display_language = get_language_dictionary()

    if g.current_user is None:
        return redirect(url_for("authentication.login"))

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
        "snake_access/password_confirm.html",
        title=display_language.get("SNAKE_ACCESS-confirm_password", "Confirm password"),
        display_language=display_language,
    )


@bp.route('/login/', methods=['GET', 'POST'])
def login():

    display_language = get_language_dictionary()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.fetch_by_username(username)

        if user:
            if user.is_active:
                if check_password_hash(user.password_hash, password):

                    session.clear()
                    session["user_id"] = user.id

                    return redirect(url_for("authentication.auth_routine"))

                else:
                    flash(
                        display_language.get(
                            "LOGIN-wrong_password",
                            "Username or password is incorrect."
                        ),
                        "danger"
                    )
            else:
                flash(
                    display_language.get(
                        "LOGIN-account_not_active", 
                        "Your account must be activated. Contact your administrator"
                    ),
                    "danger"
                )
        else:
            flash(
                display_language.get(
                    "LOGIN-please_sign_up",
                    "This account does not exist"
                ),
                "danger"
            )

    return render_template(
        'snake_access/login.html',
        title=display_language.get("LOGIN-title", "Log in"),
        display_language=display_language
    )

@bp.route("/sign-up/", methods=["GET", "POST"])
def sign_up():

    display_language = get_language_dictionary()

    form_data = {
        "firstname": "",
        "lastname": "",
        "username": "",
        "email": "",
    }

    if request.method == "POST":
        form_data["firstname"] = request.form.get("firstname", "").strip()
        form_data["lastname"] = request.form.get("lastname", "").strip()
        form_data["username"] = request.form.get("username", "").strip()
        form_data["email"] = request.form.get("email", "").strip()

        password1 = request.form.get("password1").strip()
        password2 = request.form.get("password2").strip()

        validated = True

        if len(form_data["firstname"]) < 1:
            flash(
                display_language.get(
                    "SIGNUP-firstname",
                     "First name"
                )
                + " " + 
                display_language.get(
                    "SIGNUP-cannot_be_empty", 
                    "cannot be empty."
                ),
                "danger"
            )
            validated = False

        if len(form_data["lastname"]) < 1:
            flash(
                display_language.get(
                    "SIGNUP-lastname",
                    "Last name"
                )
                + " " + 
                display_language.get(
                    "SIGNUP-cannot_be_empty", 
                    "cannot be empty."
                ),
                "danger"
            )
            validated = False

        if len(form_data["username"]) < 1:
            flash(
                display_language.get(
                    "SIGNUP-user",
                    "Username"
                )
                + " " +
                display_language.get(
                    "SIGNUP-cannot_be_empty",
                    "cannot be empty"
                ),
                "danger"
            )
            validated = False

        if User.fetch_by_username(form_data["username"]):
            flash(
                display_language.get(
                    "SIGNUP-user_already_exists",
                    "User already exists."
                ), 
                "danger"
            )
            validated = False

        if User.fetch_by_email(form_data["email"]):
            flash(
                display_language.get(
                    "SIGNUP-email_already_exists", 
                    "Email already exists"
                ), 
                "danger"
            )
            validated = False

        if not is_valid_password(password1):
            flash(
                display_language.get(
                    "SIGNUP-invalid_password", 
                    "Invalid password"
                ), 
                "danger"
            )
            validated = False
            
        if password1 != password2:
            flash(
                display_language.get(
                    "SIGNUP-passwords_dont_match", 
                    "Password do not match"
                ), 
                "danger"
            )
            validated = False

        if not validated:
            return render_template(
                "snake_access/sign-up.html",
                display_language=display_language,
                form_data=form_data,
            )

        User.create_user(
            username=form_data["username"],
            firstname=form_data["firstname"],
            lastname=form_data["lastname"],
            email=form_data["email"],
            password=password1,
        )

        flash(
            display_language.get(
                "SIGNUP-Account-created.", 
                "Account created."
            ),
            "success"
        )

        return redirect(url_for("authentication.login"))

    return render_template(
        "snake_access/sign-up.html",
        display_language=display_language,
        form_data=form_data,
    )

@bp.route("/my-account/", methods=["GET"])
@login_required
def my_account():

    display_language = get_language_dictionary()

    return render_template(
        'snake_access/my-account.html',
        display_language=display_language,
    )

@bp.route("/logout/", methods=['GET'])
@login_required
def logout():
    session.clear()
    return redirect(url_for("authentication.login"))
