# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/common/blueprint.py]                         |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-30 10:50:35 UTC                                     |
# | Updated     : 2026-06-30 10:50:35 UTC                                     |
# | Description : Flask-Common blueprints.                                    |
# +---------------------------------------------------------------------------+

from flask import Blueprint

bp = Blueprint(
    "snake_common",
    __name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="/snake-common/static",
)
