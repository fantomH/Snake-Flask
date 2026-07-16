# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/access/db.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-14 17:35:22 UTC
# Updated     : 2026-07-14 17:35:22 UTC
# Description : SnakeAccess db.
# +---------------------------------------------------------------------------+

from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Any

import click
from flask import current_app
from flask import g

from snake_flask.database import get_db

def init_db() -> None:
    """
    Initialize SnakeAccess database schema.
    """

    db = get_db("access")

    schema_path = Path(__file__).parent / "schema.sql"

    with schema_path.open("r", encoding="utf-8") as schema_file:
        db.executescript(schema_file.read())

    # +-----------------------------------------------------------------------+
    # [+] CREATE ADMIN USER
    # +-----------------------------------------------------------------------+
    from .user import User

    User.create_user(
        username="admin",
        firstname="",
        lastname="",
        email="not@email.com",
        password="password",
        is_active=1
    )

    db.commit()

    click.echo(
        "SnakeAccess db initialized."
    )

