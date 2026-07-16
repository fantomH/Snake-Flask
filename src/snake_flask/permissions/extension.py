# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/permissions/extension.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-06-17 20:36:16 UTC
# Updated     : 2026-07-14 17:29:58 UTC
# Description : SnakePermissions.
# +---------------------------------------------------------------------------+

from __future__ import annotations

from pathlib import Path

from flask import Flask

from snake_flask.common import ensure_snake_common
from snake_flask.linguae import ensure_linguae
from snake_flask.database import close_db

from .db import init_db as initialize_permissions_db

class SnakePermissions:
    """
    Flask extension used to manage users and roles permissions.
    """

    def __init__(self, app: Flask | None = None) -> None:

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize SnakePermissions inside a Flask app.
        """

        if "snake_permissions" in app.extensions:
            return app.extensions["snake_permissions"]

        app.extensions["snake_permissions"] = self

        # +-------------------------------------------------------------------+
        # [+] EXTENSIONS
        # +-------------------------------------------------------------------+
        linguae = ensure_linguae(app)
        linguae.register_package("snake_flask.permissions.dictionaries")
        ensure_snake_common(app)

        # +-------------------------------------------------------------------+
        # [+] CONFIGURATION
        # +-------------------------------------------------------------------+
        _default_configuration = {
            "SNAKE_PERMISSIONS_DATABASE": str(Path(app.instance_path) / "permissions.sqlite"),
            "SNAKE_PERMISSIONS_URL_PREFIX": "/permissions",
            "SNAKE_PERMISSIONS_BASE_TEMPLATE": None,
        }

        for key, value in _default_configuration.items():
            app.config.setdefault(key, value)

        app.teardown_appcontext(close_db)

        # +-------------------------------------------------------------------+
        # [+] BLUEPRINTS + TEMPLATES
        # +-------------------------------------------------------------------+
        @app.context_processor
        def inject_base_template():
            _base_template = app.config["SNAKE_PERMISSIONS_BASE_TEMPLATE"]

            if _base_template is None:
                _internal_base_template = ("snake_common/base_standalone.html")
            else:
                _internal_base_template = ("snake_permissions/base_extension.html")

            return {
                "_snake_permissions_internal_base_template": _internal_base_template,
                "_snake_permissions_base_template": _base_template,
            }

        _url_prefix = app.config["SNAKE_PERMISSIONS_URL_PREFIX"]

        from .blueprints.permissions import bp
        app.register_blueprint(bp, url_prefix=_url_prefix)

        from .blueprints.roles import bp
        app.register_blueprint(bp, url_prefix=_url_prefix)

        from .blueprints.permission_sets import bp
        app.register_blueprint(bp, url_prefix=_url_prefix)

        from .blueprints.users import bp
        app.register_blueprint(bp, url_prefix=_url_prefix)

    # +-----------------------------------------------------------------------+
    # [+] INIT DATABASE
    # +-----------------------------------------------------------------------+
    def init_db(self) -> None:
        initialize_permissions_db()
