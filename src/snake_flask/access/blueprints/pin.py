# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/access/blueprints/pin.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-06 20:00:00 UTC
# Updated     : 2026-07-15 16:24:52 UTC
# Description : PIN routes.
# +---------------------------------------------------------------------------+

from time import time

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from snake_flask.access.authentication_manager import login_required
from snake_flask.linguae import get_language_dictionary

from ..user import User

bp = Blueprint(
    "pin",
    __name__,
    template_folder="../templates",
    url_prefix="/auth",
)

@bp.route("/pin-setup/", methods=["GET", "POST"])
@login_required
def pin_setup():

    pin = current_app.extensions["snake_access"].pin
    display_language = get_language_dictionary()
    pin_length = current_app.config["SNAKE_ACCESS_PIN_LENGTH"]

    user_id = session.get("user_id")

    if user_id is None:
        return redirect(url_for("authentication.auth_routine"))

    user = User.fetch_by_id(user_id)

    if user is None:
        session.pop("user_id", None)
        return redirect(url_for("authentication.auth_routine"))

    if request.method == "POST":

        pin_value = request.form.get("pin", "").strip()
        pin_confirm = request.form.get("pin_confirm", "").strip()


        if not ( len(pin_value) == pin_length
            and pin_value.isdigit()):

            flash(
                display_language.get(
                    "SNAKE_ACCESS-PIN-invalid_format",
                    f"PIN must be exactly {pin_length} digits.",
                ),
                "danger",
            )
            return redirect(url_for("pin.pin_setup"))

        if pin_value != pin_confirm:
            flash(
                display_language.get(
                    "SNAKE_ACCESS-PIN-confirmation_mismatch",
                    "PIN confirmation does not match.",
                ),
                "danger",
            )
            return redirect(url_for("pin.pin_setup"))

        encrypted_secret = pin.encrypt_secret(pin_value)

        User.update_user(
            user.id,
            pin_secret=encrypted_secret,
            pin_enabled=True,
        )

        flash(
            display_language.get(
                "SNAKE_ACCESS-PIN-configured_successfully",
                "PIN configured successfully.",
            ),
            "success",
        )

        return redirect(url_for("authentication.auth_routine"))

    return render_template(
        "snake_access/pin_setup.html",
        user=user,
        pin_length=pin_length,
        display_language=display_language,
    )


@bp.route("/pin-verification/", methods=("GET", "POST"))
@login_required
def verify_pin():
    """
    Verify a user's PIN after successful password authentication.
    """

    pin = current_app.extensions["snake_access"].pin
    display_language = get_language_dictionary()

    user_id = session.get("user_id")

    if user_id is None:
        return redirect(url_for("authentication.auth_routine"))

    user = User.fetch_by_id(user_id)

    if user is None:
        session.pop("user_id", None)
        return redirect(url_for("authentication.auth_routine"))

    pin_secret = getattr(user, "pin_secret", None)

    if not pin_secret:
        session["pending_user_id"] = user.id
        return redirect(url_for("pin.pin_setup"))

    pin_length = current_app.config["SNAKE_ACCESS_PIN_LENGHT"]

    if request.method == "POST":

        pin_value = request.form.get("pin", "").strip()

        if pin.verify_pin(
            encrypted_secret=pin_secret,
            pin=pin_value,
        ):
            session["pin_confirm_at"] = time()

            return redirect(url_for("authentication.auth_routine"))

        flash(
            display_language.get(
                "SNAKE_ACCESS-PIN-invalid_pin",
                "Invalid PIN.",
            ),
            "danger",
        )

    return render_template(
        "snake_access/pin_verify.html",
        user=user,
        pin_length=pin_length,
        display_language=display_language,
    )

@bp.route("/pin-confirmation/", methods=["GET", "POST"])
@login_required
def pin_confirm():

    pin = current_app.extensions["snake_access"].pin
    display_language = get_language_dictionary()

    if g.current_user is None:
        return redirect(url_for("auth.login"))

    if not g.current_user.pin_enabled:
        return "Your account is not configured to use PIN."

    if not g.current_user.pin_secret:
        return redirect(url_for("pin.pin_setup", next=request.path))
        
    if request.method == "POST":

        _pin = request.form.get("pin")

        if pin.verify_pin(
            encrypted_secret=g.current_user.pin_secret,
            pin=_pin):
            session["pin_confirmed_at"] = time()

            next_page = request.args.get("next")

            if (
                not next_page
                or not next_page.startswith("/")
                or next_page.startswith("/logout")
            ):
                next_page = url_for("index")

            return redirect(next_page)

        flash(display_language.get("SNAKE_ACCESS_wrong_pin", "Wrong PIN."), "danger")

    return render_template(
        "snake_access/pin_confirm.html",
        title=display_language.get("SNAKE_ACCESS-confirm_pin", "Confirm PIN"),
        display_language=display_language,
    )
