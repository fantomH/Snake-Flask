# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/common/extension.py]                         |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-30 10:55:08 UTC                                     |
# | Updated     : 2026-06-30 10:55:08 UTC                                     |
# | Description : Snake-Common extension.                                     |
# +---------------------------------------------------------------------------+

from snake_flask.linguae import ensure_linguae


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
        }

        for key, value in _default_configuration.items():
            app.config.setdefault(key, value)

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

def ensure_snake_common(app):
    if "snake_common" not in app.extensions:
        SnakeCommon(app)

    return app.extensions["snake_common"]
