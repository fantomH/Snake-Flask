# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/permissions/permissions.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-06-17 20:38:00 UTC
# Updated     : 2026-07-10 13:40:54 UTC
# Description : SnakePermissions permissions.
# +---------------------------------------------------------------------------+

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from flask import g
from flask import current_app
from flask import url_for

from snake_flask.database import get_db
from snake_flask.linguae import get_language_dictionary
from snake_flask.tables import Table

from .db import execute

@dataclass
class Permission:
    name: str
    description: str
    id: int | None = None

    TABLE_NAME = "permissions"

    # +-----------------------------------------------------------------------+
    # [+] CREATE PERMISSION
    # +-----------------------------------------------------------------------+
    @classmethod
    def create_permission(
        cls,
        name: str,
        description: str = "") -> None:
        """
        Create a permission if it does not already exist.
        """

        conn = get_db("permissions")

        conn.execute(
            """
            INSERT OR IGNORE INTO permissions (name, description)
            VALUES (?, ?)
            """,
            (
                name,
                description,
            ),
        )

        conn.commit()

    # +-----------------------------------------------------------------------+
    # [+] UPDATE PERMISSION
    # +-----------------------------------------------------------------------+
    @classmethod
    def update_permission(cls, permission_id, **fields):

        if not fields:
            return

        conn = get_db("permissions")

        allowed_fields = {
            "name",
            "description",
        }

        updates = []
        values = []

        for field, value in fields.items():
            if field not in allowed_fields:
                continue

            updates.append(f"{field} = ?")

            values.append(value)

        if not updates:
            return

        values.append(permission_id)

        conn.execute(f"""
            UPDATE {cls.TABLE_NAME}
            SET {", ".join(updates)}
            WHERE id = ?
        """, values)

        conn.commit()

def generate_permissions_table():

    # +-----------------------------------------------------------------------+
    # [+] CUSTOM DICTIONARY
    # +-----------------------------------------------------------------------+

    PERMISSIONS_CUSTOM_DICTIONARIES = {
        "english": {},
        "french": {}
    }

    display_language = get_language_dictionary(custom=PERMISSIONS_CUSTOM_DICTIONARIES)

    # +-----------------------------------------------------------------------+
    # [+] COLUMNS DEFINITION
    # +-----------------------------------------------------------------------+

    PERMISSIONS_TABLE = [
        {
            "name": "name",
            "label": display_language.get("permcol-name", "Name"),
            "sortable": True,
            "searchable": True,
        },
        {
            "name": "description",
            "label": display_language.get("permcol-description", "Description"),
            "sortable": True,
            "searchable": True,
        },
    ]

    return Table(
        table_id="permissions-table",
        data_url=url_for("permissions.permissions_data"),
        data_update_url=url_for("permissions.permissions_update"),
        db=get_db("permissions"),
        source_table="permissions",
        columns=PERMISSIONS_TABLE,
        default_order_by="name ASC",
    )

def create_user_group(
    name: str,
    description: str = "",
) -> None:
    """
    Create a user group if it does not already exist.
    """

    execute(
        """
        INSERT OR IGNORE INTO user_groups (name, description)
        VALUES (?, ?)
        """,
        (
            name,
            description,
        ),
    )


def create_permission_group(
    name: str,
    description: str = "",
) -> None:
    """
    Create a permission group if it does not already exist.
    """

    execute(
        """
        INSERT OR IGNORE INTO permission_groups (name, description)
        VALUES (?, ?)
        """,
        (
            name,
            description,
        ),
    )


def get_permission_id(permission_name: str) -> int:
    """
    Return the ID of a permission.
    """

    db = get_db()

    row = db.execute(
        """
        SELECT id
        FROM permissions
        WHERE name = ?
        """,
        (permission_name,),
    ).fetchone()

    if row is None:
        raise ValueError(f"Permission does not exist: {permission_name}")

    return int(row["id"])


def get_user_group_id(group_name: str) -> int:
    """
    Return the ID of a user group.
    """

    db = get_db()

    row = db.execute(
        """
        SELECT id
        FROM user_groups
        WHERE name = ?
        """,
        (group_name,),
    ).fetchone()

    if row is None:
        raise ValueError(f"User group does not exist: {group_name}")

    return int(row["id"])


def get_permission_group_id(permission_group_name: str) -> int:
    """
    Return the ID of a permission group.
    """

    db = get_db()

    row = db.execute(
        """
        SELECT id
        FROM permission_groups
        WHERE name = ?
        """,
        (permission_group_name,),
    ).fetchone()

    if row is None:
        raise ValueError(
            f"Permission group does not exist: {permission_group_name}"
        )

    return int(row["id"])


def add_permission_to_user(
    user_id: int,
    permission_name: str,
) -> None:
    """
    Add a direct permission to a user.

    This permission stays attached to the user even if groups are removed.
    """

    create_permission(permission_name)
    permission_id = get_permission_id(permission_name)

    execute(
        """
        INSERT OR IGNORE INTO user_permissions (user_id, permission_id)
        VALUES (?, ?)
        """,
        (
            user_id,
            permission_id,
        ),
    )


def remove_permission_from_user(
    user_id: int,
    permission_name: str,
) -> None:
    """
    Remove a direct permission from a user.
    """

    permission_id = get_permission_id(permission_name)

    execute(
        """
        DELETE FROM user_permissions
        WHERE user_id = ?
        AND permission_id = ?
        """,
        (
            user_id,
            permission_id,
        ),
    )


def add_user_to_group(
    user_id: int,
    group_name: str,
) -> None:
    """
    Add a user to a user group.
    """

    create_user_group(group_name)
    group_id = get_user_group_id(group_name)

    execute(
        """
        INSERT OR IGNORE INTO user_group_members (user_id, group_id)
        VALUES (?, ?)
        """,
        (
            user_id,
            group_id,
        ),
    )


def remove_user_from_group(
    user_id: int,
    group_name: str,
) -> None:
    """
    Remove a user from a user group.

    Direct user permissions are not affected.
    """

    group_id = get_user_group_id(group_name)

    execute(
        """
        DELETE FROM user_group_members
        WHERE user_id = ?
        AND group_id = ?
        """,
        (
            user_id,
            group_id,
        ),
    )


def add_permission_to_user_group(
    group_name: str,
    permission_name: str,
) -> None:
    """
    Add a permission to a user group.
    """

    create_user_group(group_name)
    create_permission(permission_name)

    group_id = get_user_group_id(group_name)
    permission_id = get_permission_id(permission_name)

    execute(
        """
        INSERT OR IGNORE INTO user_group_permissions
        (group_id, permission_id)
        VALUES (?, ?)
        """,
        (
            group_id,
            permission_id,
        ),
    )


def add_permission_to_permission_group(
    permission_group_name: str,
    permission_name: str,
) -> None:
    """
    Add a permission to a permission group.
    """

    create_permission_group(permission_group_name)
    create_permission(permission_name)

    permission_group_id = get_permission_group_id(permission_group_name)
    permission_id = get_permission_id(permission_name)

    execute(
        """
        INSERT OR IGNORE INTO permission_group_permissions
        (permission_group_id, permission_id)
        VALUES (?, ?)
        """,
        (
            permission_group_id,
            permission_id,
        ),
    )


def add_permission_group_to_user(
    user_id: int,
    permission_group_name: str,
) -> None:
    """
    Add a permission group directly to a user.
    """

    create_permission_group(permission_group_name)
    permission_group_id = get_permission_group_id(permission_group_name)

    execute(
        """
        INSERT OR IGNORE INTO user_permission_groups
        (user_id, permission_group_id)
        VALUES (?, ?)
        """,
        (
            user_id,
            permission_group_id,
        ),
    )


def add_permission_group_to_user_group(
    group_name: str,
    permission_group_name: str,
) -> None:
    """
    Add a permission group to a user group.
    """

    create_user_group(group_name)
    create_permission_group(permission_group_name)

    group_id = get_user_group_id(group_name)
    permission_group_id = get_permission_group_id(permission_group_name)

    execute(
        """
        INSERT OR IGNORE INTO user_group_permission_groups
        (group_id, permission_group_id)
        VALUES (?, ?)
        """,
        (
            group_id,
            permission_group_id,
        ),
    )


def get_effective_permissions(user_id: int) -> set[str]:
    """
    Return all permissions for a user.

    Sources:
    - direct user permissions
    - permissions from user groups
    - permissions from permission groups attached to the user
    - permissions from permission groups attached to the user's groups
    """

    db = get_db()

    rows = db.execute(
        """
        SELECT permissions.name
        FROM permissions
        JOIN user_permissions
            ON user_permissions.permission_id = permissions.id
        WHERE user_permissions.user_id = ?

        UNION

        SELECT permissions.name
        FROM permissions
        JOIN user_group_permissions
            ON user_group_permissions.permission_id = permissions.id
        JOIN user_group_members
            ON user_group_members.group_id = user_group_permissions.group_id
        WHERE user_group_members.user_id = ?

        UNION

        SELECT permissions.name
        FROM permissions
        JOIN permission_group_permissions
            ON permission_group_permissions.permission_id = permissions.id
        JOIN user_permission_groups
            ON user_permission_groups.permission_group_id =
               permission_group_permissions.permission_group_id
        WHERE user_permission_groups.user_id = ?

        UNION

        SELECT permissions.name
        FROM permissions
        JOIN permission_group_permissions
            ON permission_group_permissions.permission_id = permissions.id
        JOIN user_group_permission_groups
            ON user_group_permission_groups.permission_group_id =
               permission_group_permissions.permission_group_id
        JOIN user_group_members
            ON user_group_members.group_id =
               user_group_permission_groups.group_id
        WHERE user_group_members.user_id = ?
        """,
        (
            user_id,
            user_id,
            user_id,
            user_id,
        ),
    ).fetchall()

    return {str(row["name"]) for row in rows}


def permission_matches(
    permission: str,
    required_permission: str,
) -> bool:
    """
    Check if a permission matches the required permission.

    Exact match:
        document.123.edit == document.123.edit

    Wildcard match:
        document.*.edit == document.123.edit
    """

    permission_parts = permission.split(".")
    required_parts = required_permission.split(".")

    if len(permission_parts) != len(required_parts):
        return False

    for permission_part, required_part in zip(
        permission_parts,
        required_parts,
    ):
        if permission_part == "*":
            continue

        if permission_part != required_part:
            return False

    return True


def can(required_permission: str, user_id: int | None = None) -> bool:
    """
    Return True if the user has the required permission.

    If user_id is not provided, this function tries to use:
        g.current_user.id
    """

    if user_id is None:
        current_user = getattr(g, "current_user", None)

        if current_user is None:
            return False

        user_id = int(current_user.id)

    permissions = get_effective_permissions(user_id)

    for permission in permissions:
        if permission_matches(permission, required_permission):
            return True

    return False
