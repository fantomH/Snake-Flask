# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/database/extension.py]                       |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-01 16:50:53 UTC                                     |
# | Updated     : 2026-07-01 16:50:53 UTC                                     |
# | Description : Snake-Database extension.                                   |
# +---------------------------------------------------------------------------+

from __future__ import annotations

from typing import Any

from flask import Flask, current_app, g

from .backends import DatabaseBackend


class SnakeDatabase:

    def __init__(
        self,
        app: Flask | None = None,
        databases: dict[str, DatabaseBackend] | None = None,
    ):
        self.databases = databases or {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.extensions["snake_database"] = self
        app.teardown_appcontext(close_db)

    def register(
        self,
        name: str,
        backend: DatabaseBackend,
    ) -> None:
        self.databases[name] = backend

    def get_backend(self, name: str) -> DatabaseBackend:
        if name not in self.databases:
            raise RuntimeError(f"Database is not registered: {name}")

        return self.databases[name]


def get_database_extension() -> SnakeDatabase:
    if "snake_database" not in current_app.extensions:
        raise RuntimeError(
            "SnakeDatabase is not initialized. "
            "Call SnakeDatabase().init_app(app)."
        )

    return current_app.extensions["snake_database"]


def get_db(name: str = "default") -> Any:
    extension = get_database_extension()

    if "snake_databases" not in g:
        g.snake_databases = {}

    if name not in g.snake_databases:
        backend = extension.get_backend(name)
        g.snake_databases[name] = backend.connect()

    return g.snake_databases[name]


def get_backend(name: str = "default") -> DatabaseBackend:
    extension = get_database_extension()
    return extension.get_backend(name)


def close_db(error: Exception | None = None) -> None:
    extension = get_database_extension()

    databases = g.pop("snake_databases", {})

    for name, conn in databases.items():
        backend = extension.get_backend(name)
        backend.close(conn)
