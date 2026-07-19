# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/common/extension.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-06-30 10:55:08 UTC
# Updated     : 2026-07-16 10:53:03 UTC
# Description : SnakeCommon extions.
# +---------------------------------------------------------------------------+

from __future__ import annotations

import json

from flask import Flask
from flask import current_app
from flask import url_for
from markupsafe import Markup
from markupsafe import escape

from snake_flask.linguae import ensure_linguae

from .http_errors import HTTP_ERROR_PAGES
from .http_errors import render_status

class SnakeCommon:
    "Common resources shared by Snake-Flask extensions."

    def __init__(self, app):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize SnakeCommon inside a Flask app.
        """

        if "snake_common" in app.extensions:
            return app.extensions["snake_common"]

        app.extensions["snake_common"] = self

        # +-------------------------------------------------------------------+
        # [+] EXTENSIONS
        # +-------------------------------------------------------------------+
        linguae = ensure_linguae(app)
        linguae.register_package("snake_flask.common.dictionaries")
        
        # +-------------------------------------------------------------------+
        # [+] CONFIGURATION
        # +-------------------------------------------------------------------+
        _default_configuration = {
            "SNAKE_COMMON_CONFIGURATION_URL_PREFIX": "/configuration",
            "SNAKE_COMMON_BASE_TEMPLATE": None,
            "SNAKE_ACCESS_INACTIVITY_TIMEOUT": None,
        }

        for key, value in _default_configuration.items():
            app.config.setdefault(key, value)

        # +-------------------------------------------------------------------+
        # [+] JINJA
        # +-------------------------------------------------------------------+
        app.jinja_env.globals.update(
            load_common_css=load_common_css,
            _load_common_js=_load_common_js,
            load_common_js=load_common_js,
        )

        # +-------------------------------------------------------------------+
        # [+] BLUEPRINTS + TEMPLATES
        # +-------------------------------------------------------------------+
        @app.context_processor
        def inject_base_template():
            _base_template = app.config["SNAKE_COMMON_BASE_TEMPLATE"]

            if _base_template is None:
                _internal_base_template = ("snake_common/base_standalone.html")
            else:
                _internal_base_template = ("snake_common/base_extension.html")

            return {
                "_snake_common_internal_base_template": _internal_base_template,
                "_snake_common_base_template": _base_template,
            }

        from .blueprint import bp
        app.register_blueprint(bp)

        from .blueprints.config import bp
        app.register_blueprint(
        bp,
        url_prefix=app.config["SNAKE_COMMON_CONFIGURATION_URL_PREFIX"],
        )

        # +-------------------------------------------------------------------+
        # [+] HTTP ERRORS HANDLER.
        # +-------------------------------------------------------------------+
        for code in HTTP_ERROR_PAGES:
            app.register_error_handler(
                code,
                lambda error, code=code: render_status(code),
            )

def ensure_snake_common(app):
    if "snake_common" not in app.extensions:
        SnakeCommon(app)

    return app.extensions["snake_common"]

def load_common_css():
    return Markup(
        f'<link rel="stylesheet" '
        f'href="{url_for("snake_common.static", filename="snake-common.css")}">'
    )

def _load_common_js():
    config = {
        "inactivityTimeoutMinutes": current_app.config.get(
            "SNAKE_ACCESS_INACTIVITY_TIMEOUT"
        ),
        "logoutUrl": url_for("authentication.logout"),
    }

    config_json = (
        json.dumps(config)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )

    return Markup(
        f"""
<script>
window.SNAKE_ACCESS = Object.assign(
    {{}},
    window.SNAKE_ACCESS || {{}},
    {config_json}
);
</script>

<script defer src="{url_for("snake_common.static", filename="snake-common.js")}"></script>
"""
    )

def _config_to_json(config):
    return (
        json.dumps(config)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )

def load_common_js(*names):
    scripts = []

    if "inactivity" in names:
        config = {
            "inactivityTimeoutMinutes": current_app.config.get(
                "SNAKE_ACCESS_INACTIVITY_TIMEOUT"
            ),
            "logoutUrl": url_for("authentication.logout"),
        }

        config_json = _config_to_json(config)

        scripts.append(
            f"""
<script>
window.SNAKE_ACCESS = Object.assign(
    {{}},
    window.SNAKE_ACCESS || {{}},
    {config_json}
);
</script>
""".strip()
        )

    scripts.extend(
        (
            '<script defer src="'
            f'{url_for("snake_common.static", filename=f"js/{name}.js")}'
            '"></script>'
        )
        for name in names
    )

    return Markup("\n".join(scripts))
