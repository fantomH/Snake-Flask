# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/permissions/permissions.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-06-18 19:51:47 UTC
# Updated     : 2026-07-09 15:15:43 UTC
# Description : SnakePermissions permissions routes.
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
from .. permissions import generate_permissions_table
from .. permissions import Permission

bp = Blueprint(
    "permissions",
    __name__,
    template_folder="../templates",
    static_folder="static",
)

@bp.route("/")
@login_required
def index():
    """
    Display the Snake-Permissions admin dashboard.
    """

    return render_template(
        "snake_permissions/index.html",
    )

# +---------------------------------------------------------------------------+
# [+] PERMISSIONS MANAGEMENT
# +---------------------------------------------------------------------------+
@bp.route("/permissions/", methods=["GET", "POST"])
@login_required
def permissions():
    """
    List and create permissions.
    """

    display_language = get_language_dictionary()
    permissions_table = generate_permissions_table()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if name:
            Permission.create_permission(
                name=name,
                description=description,
            )

        return redirect(url_for("permissions.permissions"))

    return render_template(
        "snake_permissions/permissions.html",
        permissions_table=permissions_table,
        display_language=display_language,
    )

@bp.route("/permissions/data/")
@login_required
def permissions_data():

    permissions_table=generate_permissions_table()

    return jsonify(
        permissions_table.get_data()
    )

@bp.route("/permissions/update", methods=["POSTS"])
@login_required
def permissions_update():

    data = request.get_json()

    Permission.update_permission(
        data.get("id"),
        **{
            data.get("column"): data.get("value")
        }
    )

    return jsonify({
        "ok": True,
    })

@bp.route("/user-groups/", methods=["GET", "POST"])
@login_required
def user_groups():
    """
    List and create user groups.
    """

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if name:
            _perm.create_user_group(
                name=name,
                description=description,
            )

        return redirect(url_for("snake_permissions.user_groups"))

    db = _database.get_db()

    rows = db.execute(
        """
        SELECT id, name, description
        FROM user_groups
        ORDER BY name
        """
    ).fetchall()

    return render_template(
        "snake_permissions/user_groups.html",
        user_groups=rows,
    )

@bp.route("/permission-groups/", methods=["GET", "POST"])
@login_required
def permission_groups():
    """
    List and create permission groups.
    """

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if name:
            _perm.create_permission_group(
                name=name,
                description=description,
            )

        return redirect(url_for("snake_permissions.permission_groups"))

    db = _database.get_db()

    rows = db.execute(
        """
        SELECT id, name, description
        FROM permission_groups
        ORDER BY name
        """
    ).fetchall()

    return render_template(
        "snake_permissions/permission_groups.html",
        permission_groups=rows,
    )
