# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/common/extension.py]                         |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-30 10:55:08 UTC                                     |
# | Updated     : 2026-06-30 10:55:08 UTC                                     |
# | Description : Snake-Common extension.                                     |
# +---------------------------------------------------------------------------+

from .blueprint import bp

class SnakeCommon:
    "Common resources shared by Snake-Flask extensions."

    def __init__(self, app):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        if "snake_common" in app.extensions:
            return app.extensions["snake_common"]

        app.extensions["snake_common"] = self

        app.register_blueprint(bp)

def ensure_snake_common(app):
    if "snake_common" not in app.extensions:
        SnakeCommon(app)

    return app.extensions["snake_common"]
