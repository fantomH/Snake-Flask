# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/tables/extension.py]                         |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-04 12:30:25 UTC                                     |
# | Updated     : 2026-07-01 12:37:04 UTC                                     |
# | Description : SnakeTables extension.                                      |
# +---------------------------------------------------------------------------+

from __future__ import annotations

from flask import Flask
from flask import Blueprint

from snake_flask.linguae import ensure_linguae

from .table import Table

class SnakeTables:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        if "snake_tables" in app.extensions:
            return app.extensions["snake_tables"]

        app.extensions["snake_tables"] = self

        # [-] SnakeLinguae initiation.
        linguae = ensure_linguae(app)

        bp = Blueprint(
            "snake_tables",
            __name__,
            static_url_path="/snake-tables/static",
            static_folder="static",
            template_folder="templates",
        )

        app.register_blueprint(bp)
