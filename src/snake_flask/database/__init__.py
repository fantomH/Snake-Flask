# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/database/__init__.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-06-25 11:24:51 UTC
# Updated     : 2026-07-13 10:59:43 UTC
# Description : SnakeDatabase API.
# +---------------------------------------------------------------------------+

from .backends import DatabaseBackend
from .backends import PostgreSQLBackend
from .backends import SQLiteBackend
from .extension import SnakeDatabase
from .extension import close_db
from .extension import get_backend
from .extension import get_db

__all__ = [
    "DatabaseBackend",
    "PostgreSQLBackend",
    "SQLiteBackend",
    "SnakeDatabase",
    "close_db",
    "get_backend",
    "get_db",
]
