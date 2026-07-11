# +-------------------------------------------------------------------- INFO -+
# | [Snake-Permissions/snake_permissions/db.py]                               |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-17 20:41:56 UTC                                     |
# | Updated     : 2026-06-17 20:41:56 UTC                                     |
# | Description : SQLite helpers for Snake-Permissions.                       |
# +---------------------------------------------------------------------------+

from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Any

from flask import current_app, g


def get_db() -> sqlite3.Connection:
    """
    Return the Snake-Permissions SQLite connection.
    """

    if "snake_permissions_db" not in g:
        database = current_app.config["SNAKE_PERMISSIONS_DATABASE"]

        Path(database).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        connection = sqlite3.connect(database)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        g.snake_permissions_db = connection

    return g.snake_permissions_db


def close_db(error: Exception | None = None) -> None:
    """
    Close the database connection at the end of the request.
    """

    connection = g.pop("snake_permissions_db", None)

    if connection is not None:
        connection.close()


def init_db() -> None:
    """
    Initialize the Snake-Permissions database schema.
    """

    db = get_db()

    schema_path = Path(__file__).parent / "schema.sql"

    with schema_path.open("r", encoding="utf-8") as schema_file:
        db.executescript(schema_file.read())

    db.commit()


def execute(
    query: str,
    parameters: tuple[Any, ...] = (),
) -> sqlite3.Cursor:
    """
    Execute a SQL query and commit immediately.
    """

    db = get_db()
    cursor = db.execute(query, parameters)
    db.commit()

    return cursor
