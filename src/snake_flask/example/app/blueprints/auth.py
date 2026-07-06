# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/example/app/routes/auth.py]                  |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-05-19 16:01:48 UTC                                     |
# | Updated     : 2026-07-01 19:00:45 UTC                                     |
# | Description : Authentication routes.                                      |
# +---------------------------------------------------------------------------+

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash

from snake_flask.linguae import get_language_dictionary
from snake_vault.utils.data_validator import is_valid_password

from ..login_manager import login_required
from ..models.user import User

bp = Blueprint("auth", __name__)

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

                    if user.mfa_enabled:

                        session.clear()
                        session["pending_user_id"] = user.id

                        if user.mfa_secret:
                            return redirect(url_for("mfa.verify_mfa"))

                        return redirect(url_for("mfa.mfa_setup"))

                    session.clear()
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
        'auth/login.html',
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
                "auth/sign-up.html",
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

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/sign-up.html",
        display_language=display_language,
        form_data=form_data,
    )

@bp.route("/my-account/", methods=["GET"])
def my_account():

    display_language = get_language_dictionary()

    return render_template(
        'auth/my-account.html',
        display_language=display_language,
    )

@bp.route("/logout/", methods=['GET'])
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
