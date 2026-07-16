# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/permissions/blueprints/permission_sets.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-14 15:25:01 UTC
# Updated     : 2026-07-14 15:25:05 UTC
# Description : SnakePermissions permission sets routes.
# +---------------------------------------------------------------------------+

from __future__ import annotations

from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect
from flask import url_for

from snake_flask.linguae import get_language_dictionary

from .. import db as _database
from .. import permissions as _perm
from .. permission_sets import generate_permission_sets_table
from .. permission_sets import PermissionSet

bp = Blueprint(
    "permission-sets",
    __name__,
    template_folder="../templates",
    static_folder="static",
)

# +---------------------------------------------------------------------------+
# [+] PERMISSION SETS MANAGEMENT
# +---------------------------------------------------------------------------+
@bp.route("/permission-sets/", methods=["GET", "POST"])
def permission_sets():
    """
    List and create permission sets.
    """

    display_language = get_language_dictionary()
    permission_sets_table = generate_permission_sets_table()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if name:
            PermissionSet.create_permission_set(
                name=name,
                description=description,
            )

        return redirect(url_for("permission-sets.permission_sets"))

    return render_template(
        "snake_permissions/permission_sets.html",
        permission_sets_table=permission_sets_table,
        display_language=display_language,
    )

@bp.route("/permission-sets/data/")
def permission_sets_data():

    permission_sets_table=generate_permission_sets_table()

    return jsonify(
        permission_sets_table.get_data()
    )

@bp.route("/permission-sets/update", methods=["POSTS"])
def permission_sets_update():

    data = request.get_json()

    PermissionSet.update_permission_set(
        data.get("id"),
        **{
            data.get("column"): data.get("value")
        }
    )

    return jsonify({
        "ok": True,
    })
