# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/permissions/blueprints/users.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-14 15:44:13 UTC
# Updated     : 2026-07-14 15:44:13 UTC
# Description : SnakePermissions Users blueprints.
# +---------------------------------------------------------------------------+

from __future__ import annotations

import sqlite3

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from snake_flask.access.authentication_manager import login_required
from snake_flask.database import get_db

from .. permissions import Permission
from .. permission_sets import PermissionSet
from .. roles import Role


bp = Blueprint(
    "permission_users",
    __name__,
    template_folder="../templates",
    static_folder="static",
)


def get_selected_ids(field_name: str) -> set[int]:
    selected_ids: set[int] = set()

    for value in request.form.getlist(field_name):
        try:
            selected_ids.add(int(value))
        except (TypeError, ValueError):
            continue

    return selected_ids


@bp.route(
    "/user/<int:user_id>/",
    methods=("GET", "POST"),
)
@login_required
def user(user_id: int):
    if request.method == "POST":
        db = get_db("permissions")

        try:
            with db:
                Role.replace_for_user(
                    user_id,
                    get_selected_ids("role_ids"),
                )

                PermissionSet.replace_for_user(
                    user_id,
                    get_selected_ids(
                        "permission_set_ids"
                    ),
                )

                Permission.replace_for_user(
                    user_id,
                    get_selected_ids(
                        "permission_ids"
                    ),
                )

        except sqlite3.IntegrityError:
            flash(
                "The user permissions could not be updated.",
                "danger",
            )

        else:
            flash(
                "The user permissions were updated successfully.",
                "success",
            )

        return redirect(
            url_for(
                ".user",
                user_id=user_id,
            )
        )

    roles = Role.fetch_all()
    user_roles = Role.fetch_assigned_to_user(user_id)

    permission_sets = PermissionSet.fetch_all()
    user_permission_sets = (
        PermissionSet.fetch_assigned_to_user(user_id)
    )

    permissions = Permission.fetch_all()
    user_permissions = Permission.fetch_assigned_to_user(
        user_id
    )

    return render_template(
        "snake_permissions/user.html",
        user_id=user_id,
        roles=roles,
        selected_role_ids={
            role.id
            for role in user_roles
        },
        permission_sets=permission_sets,
        selected_permission_set_ids={
            permission_set.id
            for permission_set in user_permission_sets
        },
        permissions=permissions,
        selected_permission_ids={
            permission.id
            for permission in user_permissions
        },
    )
