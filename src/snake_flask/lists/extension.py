# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/lists/extension.py]                          |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-02 15:20:06 UTC                                     |
# | Updated     : 2026-07-02 15:20:06 UTC                                     |
# | Description : Snake-Lists extension.                                      |
# +---------------------------------------------------------------------------+

from __future__ import annotations

from flask import Flask
from flask import Blueprint

from snake_flask.common import ensure_snake_common

class SnakeLists:
    """Snake-Lists Flask extension."""

    def __init__(self, app: Flask | None = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        app.extensions["snake_lists"] = self

        ensure_snake_common(app)

        bp = Blueprint(
            "snake_lists",
            __name__,
            template_folder="templates",
            static_folder="static",
            static_url_path="/snake_lists/static",
        )

        app.register_blueprint(bp)
