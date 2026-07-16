# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/permissions/permission_sets.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-14 14:57:23 UTC
# Updated     : 2026-07-14 14:57:23 UTC
# Description : SnakePermissions permission set.
# +---------------------------------------------------------------------------+

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from flask import url_for

from snake_flask.database import get_db
from snake_flask.linguae import get_language_dictionary
from snake_flask.tables import Table

@dataclass
class PermissionSet:
    name: str
    description: str = ""
    id: int | None = None

    TABLE_NAME = "permission_sets"
    USER_TABLE_NAME = "user_permission_sets"

    # +-----------------------------------------------------------------------+
    # [+] CREATE PERMISSION SET
    # +-----------------------------------------------------------------------+
    @classmethod
    def create_permission_set(
        cls,
        name: str,
        description: str = "") -> None:
        """
        Create a permission set if it does not already exist.
        """

        conn = get_db("permissions")

        conn.execute(
            f"""
            INSERT OR IGNORE INTO {cls.TABLE_NAME} (name, description)
            VALUES (?, ?)
            """,
            (
                name,
                description,
            ),
        )

        conn.commit()

    # +-----------------------------------------------------------------------+
    # [+] UPDATE PERMISSION SET
    # +-----------------------------------------------------------------------+
    @classmethod
    def update_permission_set(cls, permission_set_id, **fields):

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
    # [+] FETCHALL
    # +-----------------------------------------------------------------------+
    @classmethod
    def fetch_all(cls) -> list[PermissionSet]:
        db = get_db("permissions")

        rows = db.execute(
            """
            SELECT
                id,
                name,
                description
            FROM permission_sets
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
    # [+] USER -> FETCH USER PERMISSION SETS
    # +-----------------------------------------------------------------------+
    @classmethod
    def fetch_assigned_to_user(
        cls,
        user_id: int,
    ) -> list[PermissionSet]:
        db = get_db("permissions")

        rows = db.execute(
            """
            SELECT
                permission_sets.id,
                permission_sets.name,
                permission_sets.description
            FROM permission_sets

            INNER JOIN user_permission_sets
                ON user_permission_sets.permission_set_id =
                   permission_sets.id

            WHERE user_permission_sets.user_id = ?

            ORDER BY permission_sets.name COLLATE NOCASE
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
    # [+] USER -> REPLACE USER PERMISSION SETS
    # +-----------------------------------------------------------------------+
    @classmethod
    def replace_for_user(
        cls,
        user_id: int,
        permission_set_ids: Iterable[int],
    ) -> None:
        db = get_db("permissions")

        permission_set_ids = sorted(
            {
                int(permission_set_id)
                for permission_set_id in permission_set_ids
            }
        )

        valid_ids = cls._filter_valid_ids(
            permission_set_ids
        )

        db.execute(
            """
            DELETE FROM user_permission_sets
            WHERE user_id = ?
            """,
            (user_id,),
        )

        db.executemany(
            """
            INSERT INTO user_permission_sets (
                user_id,
                permission_set_id
            )
            VALUES (?, ?)
            """,
            [
                (user_id, permission_set_id)
                for permission_set_id in valid_ids
            ],
        )

    @classmethod
    def _filter_valid_ids(
        cls,
        permission_set_ids: list[int],
    ) -> list[int]:
        if not permission_set_ids:
            return []

        placeholders = ", ".join(
            "?"
            for _ in permission_set_ids
        )

        db = get_db("permissions")

        rows = db.execute(
            f"""
            SELECT id
            FROM permission_sets
            WHERE id IN ({placeholders})
            """,
            permission_set_ids,
        ).fetchall()

        return [
            row["id"]
            for row in rows
        ]

def generate_permission_sets_table():

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

    PERMISSION_SETS_TABLE = [
        {
            "name": "name",
            "label": display_language.get("persetcol-name", "Name"),
            "sortable": True,
            "searchable": True,
        },
        {
            "name": "description",
            "label": display_language.get("permsetcol-description", "Description"),
            "sortable": True,
            "searchable": True,
        },
    ]

    return Table(
        table_id="permission-sets-table",
        data_url=url_for("permission-sets.permission_sets_data"),
        data_update_url=url_for("permission-sets.permission_sets_update"),
        db=get_db("permissions"),
        source_table="permission_sets",
        columns=PERMISSION_SETS_TABLE,
        default_order_by="name ASC",
    )
