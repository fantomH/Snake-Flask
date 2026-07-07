# [ INFO ] ------------------------------------------------------------------ +
# | [Snake-Flask/src/snake_flask/access/blueprints/pin.py]                    |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-06 20:00:00 UTC                                     |
# | Updated     : 2026-07-06 20:00:00 UTC                                     |
# | Description : PIN blueprints.                                             |
# + ------------------------------------------------------------------------- +

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from snake_flask.linguae import get_language_dictionary

from app.models.user import User

bp = Blueprint(
    "pin",
    __name__,
    template_folder="../templates",
    url_prefix="/auth",
)


def _get_pending_user():
    user_id = session.get("pending_user_id") or session.get("user_id")

    if user_id is None:
        return None

    return User.fetch_by_id(user_id)


@bp.route("/pin/setup/", methods=["GET", "POST"])
def pin_setup():
    pin = current_app.extensions["snake_access"].pin
    display_language = get_language_dictionary()
    user = _get_pending_user()

    if user is None:
        session.pop("pending_user_id", None)
        return redirect(url_for("auth.login"))

    pin_length = pin.get_length()

    if request.method == "POST":
        pin_value = request.form.get("pin", "").strip()
        pin_confirm = request.form.get("pin_confirm", "").strip()

        if not pin.is_valid_format(pin_value):
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

        session.pop("pending_user_id", None)
        session["pin_verified_user_id"] = user.id

        flash(
            display_language.get(
                "SNAKE_ACCESS-PIN-configured_successfully",
                "PIN configured successfully.",
            ),
            "success",
        )

        next_url = session.pop("pin_next", None)

        if next_url:
            return redirect(next_url)

        return redirect(url_for("index"))

    return render_template(
        "snake_access/pin_setup.html",
        user=user,
        pin_length=pin_length,
        display_language=display_language,
    )


@bp.route("/pin/verify-pin/", methods=("GET", "POST"))
def verify_pin():
    """
    Verify a user's PIN after successful password authentication.
    """

    pin = current_app.extensions["snake_access"].pin
    display_language = get_language_dictionary()
    user = _get_pending_user()

    if user is None:
        session.pop("pending_user_id", None)
        return redirect(url_for("auth.login"))

    pin_secret = getattr(user, "pin_secret", None)

    if not pin_secret:
        session["pending_user_id"] = user.id
        return redirect(url_for("pin.pin_setup"))

    pin_length = pin.get_length()

    if request.method == "POST":
        pin_value = request.form.get("pin", "").strip()

        if pin.verify_pin(
            encrypted_secret=pin_secret,
            pin=pin_value,
        ):
            session.pop("pending_user_id", None)
            session["pin_verified_user_id"] = user.id

            next_url = session.pop("pin_next", None)

            if next_url:
                return redirect(next_url)

            return redirect(url_for("index"))

        flash(
            display_language.get(
                "SNAKE_ACCESS-PIN-invalid_pin",
                "Invalid PIN.",
            ),
            "danger",
        )

    return render_template(
        "snake_access/verify_pin.html",
        user=user,
        pin_length=pin_length,
        display_language=display_language,
    )
