# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/permissions/roles.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-13 01:30:59 UTC
# Updated     : 2026-07-13 01:31:05 UTC
# Description : SnakePermissions roles routes.
# +---------------------------------------------------------------------------+

from __future__ import annotations

from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect
from flask import url_for

from snake_flask.access.authentication_manager import login_required
from snake_flask.linguae import get_language_dictionary

from .. import db as _database
from .. import permissions as _perm
from .. roles import generate_roles_table
from .. roles import Role

bp = Blueprint(
    "roles",
    __name__,
    template_folder="../templates",
    static_folder="static",
)

# +---------------------------------------------------------------------------+
# [+] ROLES MANAGEMENT
# +---------------------------------------------------------------------------+
@bp.route("/roles/", methods=["GET", "POST"])
@login_required
def roles():
    """
    List and create roles.
    """

    display_language = get_language_dictionary()
    roles_table = generate_roles_table()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if name:
            Role.create_role(
                name=name,
                description=description,
            )

        return redirect(url_for("roles.roles"))

    return render_template(
        "snake_permissions/roles.html",
        roles_table=roles_table,
        display_language=display_language,
    )

@bp.route("/roles/data/")
@login_required
def roles_data():

    roles_table=generate_roles_table()

    return jsonify(
        roles_table.get_data()
    )

@bp.route("/roles/update", methods=["POSTS"])
@login_required
def roles_update():

    data = request.get_json()

    Role.update_role(
        data.get("id"),
        **{
            data.get("column"): data.get("value")
        }
    )

    return jsonify({
        "ok": True,
    })
