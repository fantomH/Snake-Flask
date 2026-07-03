# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/__init__.py]                                 |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-22 11:14:34 UTC                                     |
# | Updated     : 2026-06-30 11:33:35 UTC                                     |
# | Description : Snake-Flask API.                                            |
# +---------------------------------------------------------------------------+

from . import common
from . import linguae
from . import quiz
from . import tables
from . import utils
from .utils import get_client_ip

__all__ = [
    "common",
    "linguae",
    "quiz",
    "tables",
    "utils",
    "get_client_ip",
]
