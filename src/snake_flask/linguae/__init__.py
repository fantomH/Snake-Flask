# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/linguae/__init__.py]                         |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-22 13:02:40 UTC                                     |
# | Updated     : 2026-06-30 12:47:53 UTC                                     |
# | Description : SnakeLinguae API.                                           |
# +---------------------------------------------------------------------------+

from .extension import SnakeLinguae
from .extension import ensure_linguae
from .extension import get_display_language
from .extension import get_language_dictionary

__all__ = [
    "SnakeLinguae",
    "ensure_linguae"
    "get_display_language",
    "get_language_dictionary",
]
