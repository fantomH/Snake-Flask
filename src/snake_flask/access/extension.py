# [ INFO ] ------------------------------------------------------------------ +
# | [Snake-Flask/src/snake_flask/access/extension.py]                         |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-06 11:31:03 UTC                                     |
# | Updated     : 2026-07-06 20:00:00 UTC                                     |
# | Description : SnakeAccess extention.                                      |
# + ------------------------------------------------------------------------- +

from __future__ import annotations

from snake_flask.common import ensure_snake_common
from snake_flask.linguae import ensure_linguae

from .mfa import MFA
from .pin import PIN

class SnakeAccess:

    def __init__(self, app=None):
        self.mfa = MFA()
        self.pin = PIN()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if "snake_access" in app.extensions:
            raise RuntimeError(
                "[!] SnakeAccess has already been initialized."
            )

        app.extensions["snake_access"] = self

        self.mfa.init_app(app)
        self.pin.init_app(app)

        linguae = ensure_linguae(app)
        linguae.register_package("snake_flask.access.dictionaries")
        ensure_snake_common(app)

        # [+] --------------------------------------------------------------- +
        # | Configuration                                                     |
        # + ----------------------------------------------------------------- +

        app.config.setdefault(
            "SNAKE_ACCESS_BASE_TEMPLATE",
            None,
        )

        # Value in seconds.
        app.config.setdefault(
            "SNAKE_ACCESS_PASSWORD_CONFIRM_TIMEOUT",
            60,
        )

        # [+] --------------------------------------------------------------- +
        # | Blueprints and Templates                                          |
        # + ----------------------------------------------------------------- +

        @app.context_processor
        def inject_base_template():
            _base_template = app.config[
                "SNAKE_ACCESS_BASE_TEMPLATE"
            ]

            if _base_template is None:
                _internal_base_template = (
                    "snake_access/base_standalone.html"
                )
            else:
                _internal_base_template = (
                    "snake_access/base_extension.html"
                )

            return {
                "_snake_access_internal_base_template": _internal_base_template,
                "_snake_access_base_template": _base_template,
            }

        from .blueprints.authentication import bp as _authentication
        from .blueprints.mfa import bp as _mfa
        from .blueprints.pin import bp as _pin

        app.register_blueprint(_authentication)
        app.register_blueprint(_mfa)
        app.register_blueprint(_pin)
