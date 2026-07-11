# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/permissions/__init__.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-06-17 20:31:24 UTC
# Updated     : 2026-07-09 12:23:19 UTC
# Description : SnakePermissions API.
# +---------------------------------------------------------------------------+

from .extension import *
from .permissions import can, get_effective_permissions
from .decorators import permission_required

from .extension import SnakePermissions

__all__ = [
    "SnakePermissions",
    "can",
    "get_effective_permissions",
    "permission_required",
]
