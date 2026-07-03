# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/example/app/models/user.py]                  |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-05-20 12:31:46 UTC                                     |
# | Updated     : 2026-07-01 17:25:00 UTC                                     |
# | Description : User model.                                                 |
# +---------------------------------------------------------------------------+

import sqlite3
from dataclasses import dataclass

from flask import current_app
from werkzeug.security import generate_password_hash

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

    TABLE_NAME = "users"

    # +- [ CREATE TABLE ] ----------------------------------------------------+
    # |                                                                       |
    # +-----------------------------------------------------------------------+
    @classmethod
    def create_table(cls):

        conn = get_db("default")

        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 0
            )
        """)

        conn.commit()

    # +- [ CREATE USER ] -----------------------------------------------------+
    # |                                                                       |
    # +-----------------------------------------------------------------------+
    @classmethod
    def create_user(
        cls,
        username,
        firstname,
        lastname,
        password,
        email=None,
        is_active=False):

        password_hash = generate_password_hash(password)

        conn = get_db("default")

        conn.execute(f"""
            INSERT INTO {cls.TABLE_NAME} (
                username,
                firstname,
                lastname,
                email,
                password_hash,
                is_active
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            username,
            firstname,
            lastname,
            email,
            password_hash,
            int(is_active)
        ))

        conn.commit()

    # +- [ UPDATE USER ] -----------------------------------------------------+
    # |                                                                       |
    # +-----------------------------------------------------------------------+
    @classmethod
    def update_user(cls, user_id, **fields):

        if not fields:
            return

        if "password" in fields:
            fields["password_hash"] = generate_password_hash(
                fields.pop("password")
            )

        conn = get_db("default")

        allowed_fields = {
            "username",
            "firstname",
            "lastname",
            "email",
            "password_hash",
            "is_active",
        }

        updates = []
        values = []

        for field, value in fields.items():

            if field not in allowed_fields:
                continue

            updates.append(f"{field} = ?")

            if field == "is_active":
                value = int(value)

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

    # +---------- { QUERIES } ------------------------------------------------+
    # |                                                                       |
    # +-----------------------------------------------------------------------+

    # +- [ FETCH BY USERNAME ] -----------------------------------------------+
    # |                                                                       |
    # +-----------------------------------------------------------------------+
    @classmethod
    def fetch_by_username(cls, username):

        conn = get_db("default")

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

    # +- [ FETCH BY ID ] -----------------------------------------------------+
    # |                                                                       |
    # +-----------------------------------------------------------------------+
    @classmethod
    def fetch_by_id(cls, id):

        conn = get_db("default")

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

    # +- [ FETCH BY EMAIL ] --------------------------------------------------+
    # |                                                                       |
    # +-----------------------------------------------------------------------+
    @classmethod
    def fetch_by_email(cls, email):

        conn = get_db("default")

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
