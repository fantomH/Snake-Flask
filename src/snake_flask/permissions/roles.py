# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/permissions/roles.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-13 01:13:08 UTC
# Updated     : 2026-07-13 15:01:50 UTC
# Description : SnakePermissions roles.
# +---------------------------------------------------------------------------+

from __future__ import annotations

import sqlite3
from collections.abc import Iterable
from dataclasses import dataclass

from flask import g
from flask import current_app
from flask import url_for

from snake_flask.database import get_db
from snake_flask.linguae import get_language_dictionary
from snake_flask.tables import Table

@dataclass
class Role:
    name: str
    description: str
    id: int | None = None

    TABLE_NAME = "roles"
    USER_TABLE_NAME = "user_roles"

    # +-----------------------------------------------------------------------+
    # [+] CREATE ROLE
    # +-----------------------------------------------------------------------+
    @classmethod
    def create_role(
        cls,
        name: str,
        description: str = "") -> None:
        """
        Create a role if it does not already exist.
        """

        conn = get_db("permissions")

        conn.execute(
            """
            INSERT OR IGNORE INTO roles (name, description)
            VALUES (?, ?)
            """,
            (
                name,
                description,
            ),
        )

        conn.commit()

    # +-----------------------------------------------------------------------+
    # [+] UPDATE ROLES
    # +-----------------------------------------------------------------------+
    @classmethod
    def update_role(cls, role_id, **fields):

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

    # +-----------------------------------------------------------------------+
    # [+] ROLES -> FETCH ALL
    # +-----------------------------------------------------------------------+
    @classmethod
    def fetch_all(cls) -> list[Role]:
        db = get_db("permissions")

        rows = db.execute(
            """
            SELECT
                id,
                name,
                description
            FROM roles
            ORDER BY name COLLATE NOCASE
            """
        ).fetchall()

        return [
            cls(
                id=row["id"],
                name=row["name"],
                description=row["description"],
            )
            for row in rows
        ]

    # +-----------------------------------------------------------------------+
    # [+] USER -> FETCH USER ROLES
    # +-----------------------------------------------------------------------+
    @classmethod
    def fetch_assigned_to_user(
        cls,
        user_id: int,
    ) -> list[Role]:
        db = get_db("permissions")

        rows = db.execute(
            """
            SELECT
                roles.id,
                roles.name,
                roles.description
            FROM roles

            INNER JOIN user_roles
                ON user_roles.role_id = roles.id

            WHERE user_roles.user_id = ?

            ORDER BY roles.name COLLATE NOCASE
            """,
            (user_id,),
        ).fetchall()

        return [
            cls(
                id=row["id"],
                name=row["name"],
                description=row["description"],
            )
            for row in rows
        ]

    # +-----------------------------------------------------------------------+
    # [+] USER -> REPLACE USER ROLES
    # +-----------------------------------------------------------------------+
    @classmethod
    def replace_for_user(
        cls,
        user_id: int,
        role_ids: Iterable[int],
    ) -> None:
        db = get_db("permissions")

        role_ids = sorted(
            {
                int(role_id)
                for role_id in role_ids
            }
        )

        valid_role_ids = cls._filter_valid_ids(role_ids)

        db.execute(
            """
            DELETE FROM user_roles
            WHERE user_id = ?
            """,
            (user_id,),
        )

        db.executemany(
            """
            INSERT INTO user_roles (
                user_id,
                role_id
            )
            VALUES (?, ?)
            """,
            [
                (user_id, role_id)
                for role_id in valid_role_ids
            ],
        )

    @classmethod
    def _filter_valid_ids(
        cls,
        role_ids: list[int],
    ) -> list[int]:
        if not role_ids:
            return []

        placeholders = ", ".join(
            "?"
            for _ in role_ids
        )

        db = get_db("permissions")

        rows = db.execute(
            f"""
            SELECT id
            FROM roles
            WHERE id IN ({placeholders})
            """,
            role_ids,
        ).fetchall()

        return [
            row["id"]
            for row in rows
        ]


def generate_roles_table():

    # +-----------------------------------------------------------------------+
    # [+] CUSTOM DICTIONARY
    # +-----------------------------------------------------------------------+

    ROLES_CUSTOM_DICTIONARIES = {
        "english": {},
        "french": {}
    }

    display_language = get_language_dictionary(custom=ROLES_CUSTOM_DICTIONARIES)

    # +-----------------------------------------------------------------------+
    # [+] COLUMNS DEFINITION
    # +-----------------------------------------------------------------------+

    ROLES_TABLE = [
        {
            "name": "name",
            "label": display_language.get("rolescol-name", "Name"),
            "sortable": True,
            "searchable": True,
        },
        {
            "name": "description",
            "label": display_language.get("rolescol-description", "Description"),
            "sortable": True,
            "searchable": True,
        },
    ]

    return Table(
        table_id="roles-table",
        data_url=url_for("roles.roles_data"),
        data_update_url=url_for("roles.roles_update"),
        db=get_db("permissions"),
        source_table="roles",
        columns=ROLES_TABLE,
        default_order_by="name ASC",
    )
