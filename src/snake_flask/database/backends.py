# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/database/backends.py]                        |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-01 16:48:09 UTC                                     |
# | Updated     : 2026-07-01 16:48:09 UTC                                     |
# | Description : Database backkends.                                         |
# +---------------------------------------------------------------------------+

from __future__ import annotations

import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    psycopg = None
    dict_row = None

class DatabaseBackend(ABC):
    """
    Base class for all database backends.
    """

    @abstractmethod
    def connect(self) -> Any:
        """
        Return a new database connection.
        """

    @abstractmethod
    def close(self, conn: Any) -> None:
        """
        Close the database connection.
        """

    @abstractmethod
    def placeholder(self) -> str:
        """
        Return the SQL placeholder style.

        SQLite uses ?
        PostgreSQL uses %s
        """

    @abstractmethod
    def execute_script(self, conn: Any, sql: str) -> None:
        """
        Execute a migration SQL script.
        """

class SQLiteBackend(DatabaseBackend):

    def __init__(self, path: str | Path):
        self.path = str(path)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def close(self, conn: sqlite3.Connection) -> None:
        conn.close()

    def placeholder(self) -> str:
        return "?"

    def execute_script(self, conn: sqlite3.Connection, sql: str) -> None:
        conn.executescript(sql)

class PostgreSQLBackend(DatabaseBackend):

    def __init__(self, uri: str):
        self.uri = uri

    def connect(self):
        if psycopg is None:
            raise RuntimeError(
                "psycopg is required for PostgreSQL support. "
                "Install it with: pip install psycopg"
            )

        return psycopg.connect(
            self.uri,
            row_factory=dict_row,
        )

    def close(self, conn) -> None:
        conn.close()

    def placeholder(self) -> str:
        return "%s"

    def execute_script(self, conn, sql: str) -> None:
        with conn.cursor() as cur:
            cur.execute(sql)
