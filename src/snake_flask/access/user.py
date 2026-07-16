# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/access/user.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-05-20 12:31:46 UTC
# Updated     : 2026-07-14 19:50:34 UTC
# Description : User model.
# +---------------------------------------------------------------------------+

import sqlite3
from dataclasses import dataclass

from flask import current_app
from flask import url_for
from werkzeug.security import generate_password_hash

from snake_flask.linguae import get_language_dictionary
from snake_flask.tables import Table
from snake_flask.database import get_db

@dataclass
class User:
    username: str
    firstname: str
    lastname: str
    password_hash: str

    id: int | None = None
    email: str | None = None
    is_active: bool = False
    mfa_enabled: bool = False
    mfa_secret: str | None = None
    pin_enabled: bool = False
    pin_secret: str | None = None

    TABLE_NAME = "users"

    # +-----------------------------------------------------------------------+
    # [+] CREATE USER
    # +-----------------------------------------------------------------------+
    @classmethod
    def create_user(
        cls,
        username,
        firstname,
        lastname,
        password,
        email=None,
        is_active=False,
        mfa_enabled=False,
        mfa_secret=None,
        pin_enabled=False,
        pin_secret=None):

        password_hash = generate_password_hash(password)

        conn = get_db("access")

        conn.execute(f"""
            INSERT INTO {cls.TABLE_NAME} (
                username,
                firstname,
                lastname,
                email,
                password_hash,
                is_active,
                mfa_enabled,
                mfa_secret,
                pin_enabled,
                pin_secret
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            firstname,
            lastname,
            email,
            password_hash,
            int(is_active),
            int(mfa_enabled),
            mfa_secret,
            int(pin_enabled),
            pin_secret
        ))

        conn.commit()

    # +-----------------------------------------------------------------------+
    # [+] UPDATE USER
    # +-----------------------------------------------------------------------+
    @classmethod
    def update_user(cls, user_id, **fields):

        if not fields:
            return

        if "password" in fields:
            fields["password_hash"] = generate_password_hash(
                fields.pop("password")
            )

        conn = get_db("access")

        allowed_fields = {
            "username",
            "firstname",
            "lastname",
            "email",
            "password_hash",
            "is_active",
            "mfa_enabled",
            "mfa_secret",
            "pin_enabled",
            "pin_secret"
        }

        updates = []
        values = []

        for field, value in fields.items():
            if field not in allowed_fields:
                continue

            updates.append(f"{field} = ?")

            if field == {"is_active", "mfa_enabled", "pin_enabled"}:
                value = int(bool(value))

            values.append(value)

        if not updates:
            return

        values.append(user_id)

        conn.execute(f"""
            UPDATE {cls.TABLE_NAME}
            SET {", ".join(updates)}
            WHERE id = ?
        """, values)

        conn.commit()

    # +-----------------------------------------------------------------------+
    # [+] FETCH BY USERNAME
    # +-----------------------------------------------------------------------+
    @classmethod
    def fetch_by_username(cls, username):

        conn = get_db("access")

        user = conn.execute(f"""
            SELECT *
            FROM {cls.TABLE_NAME}
            WHERE username = ?
        """, (
            username,
        )).fetchone()

        if user is None:
            return None

        return cls(**dict(user))

    # +-----------------------------------------------------------------------+
    # [+] FETCH BY ID
    # +-----------------------------------------------------------------------+
    @classmethod
    def fetch_by_id(cls, id):

        conn = get_db("access")

        user = conn.execute(f"""
            SELECT *
            FROM {cls.TABLE_NAME}
            WHERE id = ?
        """, (
            id,
        )).fetchone()

        if user is None:
            return None

        return cls(**dict(user))

    # +-----------------------------------------------------------------------+
    # [+] FETCH BY EMAIL
    # +-----------------------------------------------------------------------+
    @classmethod
    def fetch_by_email(cls, email):

        conn = get_db("access")

        user = conn.execute(f"""
            SELECT *
            FROM {cls.TABLE_NAME}
            WHERE email = ?
        """, (
            email,
        )).fetchone()

        if user is None:
            return None

        return cls(**dict(user))


def generate_users_table():

    # +-----------------------------------------------------------------------+
    # [+] CUSTOM DICTIONARY
    # +-----------------------------------------------------------------------+
    USERS_CUSTOM_DICTIONARIES = {
        "english": {
            "column-edit-text": "Modify",
            "column-username-label": "Username",
            "column-is_active-label": "Active",
            "column-mfa_enabled-label": "MFA Enabled",
            "column-pin_enabled-label": "PIN Enabled",
        },
        "french": {
            "column-edit-text": "Modifier",
            "column-username-label": "Utilisateurs",
            "column-is_active-label": "Actif",
            "column-mfa_enabled-label": "MFA activé",
            "column-pin_enabled-label": "NIP activé",
        }
    }

    display_language = get_language_dictionary(custom=USERS_CUSTOM_DICTIONARIES)

    # +-----------------------------------------------------------------------+
    # [+] COLUMNS DEFINITION
    # +-----------------------------------------------------------------------+
    USERS_TABLE = [
        {
            "name": "username",
            "label": display_language.get("column-username-label", "Username"),
            "sortable": True,
            "searchable": True
        },
        {
            "name": "email",
            "label": "Email",
            "sortable": True,
            "searchable": True
        },
        {
            "name": "is_active",
            "label": display_language.get("column-is_active-label", "Active"),
            "type": "checkbox",
            "sortable": True
        },

        {
            "name": "mfa_enabled",
            "label": display_language.get("column-mfa_enabled-label", "MFA Enabled"),
            "type": "checkbox",
            "sortable": True
        },
        {
            "name": "pin_enabled",
            "label": display_language.get("column-pin_enabled-label", "PIN Enabled"),
            "type": "checkbox",
            "sortable": True
        },
        {
            "name": "edit",
            "label": "",
            "type": "link-button",
            "text": display_language.get("column-edit-text", "Modify"),
            "url": "/authentication/admin/users/account/{username}/",
            "db": False,
        },
    ]

    return Table(
        table_id="users-table",
        data_url=url_for("admin.users_data"),
        data_update_url=url_for("admin.users_update"),
        db = get_db("access"),
        source_table="users",
        columns=USERS_TABLE,
        default_order_by="username ASC",
    )
