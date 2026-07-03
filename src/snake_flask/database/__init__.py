# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/database/__init__.py]                        |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-25 11:24:51 UTC                                     |
# | Updated     : 2026-07-01 20:31:42 UTC                                     |
# | Description : Database API.                                               |
# +---------------------------------------------------------------------------+

from .backends import DatabaseBackend, PostgreSQLBackend, SQLiteBackend
from .cli import migrate_command
from .extension import SnakeDatabase, close_db, get_backend, get_db

__all__ = [
    "DatabaseBackend",
    "PostgreSQLBackend",
    "SQLiteBackend",
    "SnakeDatabase",
    "close_db",
    "get_backend",
    "get_db",
    "migrate_command",
]
