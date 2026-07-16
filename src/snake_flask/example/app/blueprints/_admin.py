# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/example/app/routes/admin.py]                 |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-05-19 16:01:48 UTC                                     |
# | Updated     : 2026-06-19 19:34:47 UTC                                     |
# | Description : Admin routes.                                               |
# +---------------------------------------------------------------------------+

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import jsonify
from flask import render_template
from flask import request

from snake_flask.linguae import get_language_dictionary
from snake_vault.utils.data_validator import is_valid_password

from ..login_manager import ( login_required )
from ..models.user import User
from ..tables.admin import get_users_table

bp = Blueprint("admin", __name__)

@bp.route("/admin/users/")
@login_required
def users():

    display_language = get_language_dictionary()
    users_table = get_users_table()

    return render_template(
        "admin/users.html",
        users_table=users_table,
        display_language=display_language,
    )

@bp.route("/admin/users/data/")
@login_required
def users_data():

    users_table = get_users_table()

    return jsonify(
        users_table.get_data()
    )

@bp.route("/admin/users/update/", methods=["POST"])
@login_required
def users_update():

    data = request.get_json()

    User.update_user(
        data.get("id"),
        **{
            data.get("column"): data.get("value")
        }
    )

    return jsonify({
        "ok": True,
    })

@bp.route("/admin/users/account/<username>/", methods=["GET", "POST"])
def user_account(username):

    user_account = User.fetch_by_username(username)
    display_language = get_language_dictionary()

    if request.method == "POST":

        form_data = {}

        form_data["is_active"] = 1 if request.form.get("is_active", "").strip() else 0
        form_data["mfa_enabled"] = 1 if request.form.get("mfa_enabled", "").strip() else 0
        form_data["pin_enabled"] = 1 if request.form.get("pin_enabled", "").strip() else 0
        form_data["username"] = request.form.get("username", "").strip()
        form_data["firstname"] = request.form.get("firstname", "").strip()
        form_data["lastname"] = request.form.get("lastname", "").strip()
        form_data["email"] = request.form.get("email", "").strip()

        password1 = request.form.get("password1", "").strip()
        password2 = request.form.get("password2", "").strip()

        validated = True
        user_account_values_to_update = {}

        # +- [+] is_active ---------------------------------------------------+
        if form_data["is_active"] != user_account.is_active:
            user_account_values_to_update["is_active"] = form_data["is_active"]

        if form_data["mfa_enabled"] != user_account.mfa_enabled:
            user_account_values_to_update["mfa_enabled"] = form_data["mfa_enabled"]

        if form_data["pin_enabled"] != user_account.pin_enabled:
            user_account_values_to_update["pin_enabled"] = form_data["pin_enabled"]

        # +- [+] firstname ---------------------------------------------------+
        if form_data["firstname"] != user_account.firstname:
            if len(form_data["firstname"]) < 1:
                flash(
                    display_language.get(
                        "USER-ACCOUNT-firstname",
                        "First name"
                    )
                    + " " +
                    display_language.get(
                        "USER-ACCOUNT-cannot_be_empty",
                        "cannot be empty"
                    ), 
                    "danger"
                )
                validated = False
            else:
                user_account_values_to_update['firstname'] = form_data["firstname"]

        # +- [+] lastname ----------------------------------------------------+
        if form_data["lastname"] != user_account.lastname:
            if len(form_data["lastname"]) < 1:
                flash(
                    display_language.get(
                        "USER-ACCOUNT-lastname",
                        "Last name"
                    )
                    + " " +
                    display_language.get(
                        "USER-ACCOUNT-cannot_be_empty",
                        "cannot be empty"
                    ), 
                    "danger"
                )
                validated = False
            else:
                user_account_values_to_update['lastname'] = form_data["lastname"]

        # +- [+] username ----------------------------------------------------+
        if form_data["username"] != user_account.username:
            pass
            if User.fetch_by_username(form_data["username"]):
                flash(
                    display_language.get(
                        "USER-ACCOUNT-username-already-exists",
                        "Username already exists."
                    ),
                    "danger"
                )
                validated = False
            elif len(form_data["username"]) < 1:
                flash(
                    display_language.get(
                        "USER-ACCOUNT-username",
                        "Username"
                    )
                    + " " +
                    display_language.get(
                        "USER-ACCOUNT-cannot_be_empty",
                        "cannot be empty."
                    ),
                    "danger"
                )
                validated = False
            else:
                user_account_values_to_update["username"] = form_data["username"]

        # +- [+] email -------------------------------------------------------+
        if form_data["email"] != user_account.email:
            if User.fetch_by_email(form_data["email"]):
                flash(
                    display_language.get(
                        "USER-ACCOUNT-email-already-exists",
                        "Email already exists."
                    ),
                    "danger"
                )
                validated = False
            else:
                user_account_values_to_update["email"] = form_data["email"]

        # +- [+] password ----------------------------------------------------+
        if password1:
            if not is_valid_password(password1):
                flash(
                    display_language.get(
                        "USER-ACCOUNT-invalid-password",
                        "Invalid password"
                    ),
                    "danger"
                )
                validated = False
            elif password1 != password2:
                flash(
                    display_language.get(
                        "USER-ACCOUNT-passwords-dont-match",
                        "Passwords don't match"
                    ),
                    "danger"
                )
                validated = False
            else:
                user_account_values_to_update["password"] = password1

        # +- [+] validation and update  --------------------------------------+
        if validated and len(user_account_values_to_update) > 0:
            User.update_user(
                user_account.id,
                **user_account_values_to_update
            )

            user_account = User.fetch_by_id(user_account.id)
            
    return render_template(
        "admin/user-account.html",
        user_account=user_account,
        display_language=display_language,
    )
