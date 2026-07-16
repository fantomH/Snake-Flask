# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/access/extension.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-06 11:31:03 UTC
# Updated     : 2026-07-14 16:36:11 UTC
# Description : SnakeAccess extension.
# +---------------------------------------------------------------------------+

from __future__ import annotations

from pathlib import Path

from snake_flask.common import ensure_snake_common
from snake_flask.linguae import ensure_linguae
from snake_flask.database import close_db

from .db import init_db as initialize_access_db
from .mfa import MFA
from .pin import PIN

class SnakeAccess:
    """
    Flask extension providing user management, access and authentication.
    """

    def __init__(self, app: Flask | None = None) -> None:
        self.mfa = MFA()
        self.pin = PIN()

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize SnakeAccess inside a Flask app.
        """

        if "snake_access" in app.extensions:
            return app.extensions["snake_access"]

        app.extensions["snake_access"] = self

        # +-------------------------------------------------------------------+
        # [+] EXTENSIONS
        # +-------------------------------------------------------------------+
        self.mfa.init_app(app)
        self.pin.init_app(app)

        linguae = ensure_linguae(app)
        linguae.register_package("snake_flask.access.dictionaries")
        ensure_snake_common(app)

        # +------------------------------------------------------------------ +
        # [+] CONFIGURATION
        # + ----------------------------------------------------------------- +
        _default_configuration = {
            "SNAKE_ACCESS_DATABASE": str(Path(app.instance_path) / "access.sqlite"),
            "SNAKE_ACCESS_URL_PREFIX": "/authentication",
            "SNAKE_ACCESS_BASE_TEMPLATE": None,
            "SNAKE_ACCESS_SECRET_KEY": None,
            "SNAKE_ACCESS_PASSWORD_CONFIRM_TIMEOUT": 60, # time in seconds.
        }

        for key, value in _default_configuration.items():
            app.config.setdefault(key, value)

        app.teardown_appcontext(close_db)

        # +------------------------------------------------------------------ +
        # [+] BLUEPRINTS + TEMPLATES
        # + ----------------------------------------------------------------- +
        @app.context_processor
        def inject_base_template():
            _base_template = app.config["SNAKE_ACCESS_BASE_TEMPLATE"]

            if _base_template is None:
                _internal_base_template = ("snake_access/base_standalone.html")
            else:
                _internal_base_template = ("snake_access/base_extension.html")

            return {
                "_snake_access_internal_base_template": _internal_base_template,
                "_snake_access_base_template": _base_template,
            }

        _url_prefix = app.config["SNAKE_ACCESS_URL_PREFIX"]

        from .blueprints.authentication import bp
        app.register_blueprint(bp, url_prefix=_url_prefix)

        from .blueprints.mfa import bp
        app.register_blueprint(bp, url_prefix=_url_prefix)

        from .blueprints.pin import bp
        app.register_blueprint(bp, url_prefix=_url_prefix)

        from .blueprints.admin import bp
        app.register_blueprint(bp, url_prefix=_url_prefix)

    # +-----------------------------------------------------------------------+
    # [+] INIT DATABASE
    # +-----------------------------------------------------------------------+
    def init_db(self) -> None:
        initialize_access_db()
