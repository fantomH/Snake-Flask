# [ INFO ] ------------------------------------------------------------------ +
# | [Snake-Flask/src/snake_flask/access/blueprints/mfa.py]                    |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-06 12:14:49 UTC                                     |
# | Updated     : 2026-07-06 12:14:49 UTC                                     |
# | Description : MFA blueprints.                                             |
# + ------------------------------------------------------------------------- +

import base64
from io import BytesIO

import qrcode
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash,
)

from snake_flask.access import MFA
from app.models.user import User

bp = Blueprint(
    "mfa",
    __name__,
    template_folder="../templates",
    url_prefix="/auth",
)

mfa = MFA()

@bp.route("/mfa/setup/", methods=["GET", "POST"])
def mfa_setup():
    user_id = session.get("pending_user_id")

    if user_id is None:
        return redirect(url_for("auth.login"))

    user = User.fetch_by_id(user_id)

    if user is None:
        session.pop("pending_user_id", None)
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        encrypted_secret = session.get("pending_mfa_secret")
        code = request.form.get("code", "").strip()

        if not encrypted_secret:
            flash("MFA setup expired. Please try again.", "warning")
            return redirect(url_for("auth.login"))

        if mfa.verify_code(
            encrypted_secret=encrypted_secret,
            code=code,
        ):
            User.update_user(
                user.id,
                mfa_secret=encrypted_secret,
                mfa_enabled=True,
            )

            session.pop("pending_mfa_secret", None)
            session.pop("pending_user_id", None)

            session.clear()
            session["user_id"] = user.id
            session.permanent = True

            flash("MFA configured successfully.", "success")
            return redirect(url_for("index"))

        flash("Invalid MFA code.", "danger")

    setup = mfa.generate_setup(username=user.username)

    session["pending_mfa_secret"] = setup.encrypted_secret

    qr_image = BytesIO()

    qrcode.make(setup.provisioning_uri).save(
        qr_image,
        format="PNG",
    )

    qr_base64 = base64.b64encode(
        qr_image.getvalue()
    ).decode("utf-8")

    return render_template(
        "snake_access/mfa_setup.html",
        user=user,
        secret=setup.secret,
        qr_base64=qr_base64,
    )

@bp.route("/mfa/verify-mfa/", methods=("GET", "POST"))
def verify_mfa():
    """
    Verify a user's MFA code after successful password authentication.
    """

    user_id = session.get("pending_user_id")

    if user_id is None:
        return redirect(url_for("auth.login"))

    user = User.fetch_by_id(user_id)

    if user is None:
        session.pop("pending_user_id", None)
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        code = request.form.get("code", "").strip()

        if mfa.verify_code(
            encrypted_secret=user.mfa_secret,
            code=code,
        ):
            session.pop("pending_user_id", None)

            session.clear()
            session["user_id"] = user.id
            session.permanent = True

            flash(
                "Welcome back!",
                "success",
            )

            return redirect(url_for("index"))

        flash(
            "Invalid authentication code.",
            "danger",
        )

    return render_template(
        "snake_access/verify_mfa.html",
        user=user,
    )
