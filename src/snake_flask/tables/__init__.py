# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/tables/__init__.py]                          |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-24 15:36:36 UTC                                     |
# | Updated     : 2026-06-24 15:36:36 UTC                                     |
# | Description : SnakeTables API.                                            |
# +---------------------------------------------------------------------------+

from .extension import SnakeTables
from .table import Table

__all__ = [
    "SnakeTables",
    "Table",
]
