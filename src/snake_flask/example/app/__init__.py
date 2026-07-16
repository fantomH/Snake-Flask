# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/example/app/__init__.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-05-19 11:30:00 UTC
# Updated     : 2026-07-15 11:13:14 UTC
# Description : FlaskExample.
# +---------------------------------------------------------------------------+

import os
from datetime import timedelta
from pathlib import Path

from flask import Flask
from flask import g
from flask import render_template

from snake_flask import get_client_ip
from snake_flask.access import SnakeAccess
from snake_flask.access import authentication_manager
from snake_flask.access.authentication_manager import login_required
from snake_flask.common import ensure_snake_common
from snake_flask.database import SQLiteBackend
from snake_flask.database import SnakeDatabase
from snake_flask.database import close_db
from snake_flask.linguae import ensure_linguae
from snake_flask.linguae import get_language_dictionary
from snake_flask.lists import SnakeLists
from snake_flask.permissions import SnakePermissions
from snake_flask.quiz import SnakeQuiz
from snake_flask.tables import SnakeTables
from snake_flask.utils import display_app_context
from snake_vault.snake_utils.logger import SnakeLogger

from snake_scribe import SnakeScribe

from .db import init_db
# from .login_manager import init_app
# from .login_manager import login_required

access = SnakeAccess()
db = SnakeDatabase()
lists = SnakeLists()
log = SnakeLogger(profile="development")
permissions = SnakePermissions()
quiz = SnakeQuiz()
scribe=SnakeScribe()
tables = SnakeTables()

def create_app(test_config=None, instance_path=None):

    app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)

    # +-----------------------------------------------------------------------+
    # [+] Default Configuration
    #
    # Example of app configuration inside the app factory.
    # It is suggested to insert the config in instance/config.py instead.
    # +-----------------------------------------------------------------------+
    app.config.from_mapping(
        # DEFAULT_LANGUAGE="english",
        DEFAULT_LANGUAGE="french",
        SECRET_KEY="secret",
        SESSION_TIMEOUT=60,
        SNAKE_QUIZ_BASE_TEMPLATE="base.html",
        SNAKE_SCRIBE_APP_BASE_TEMPLATE="base.html",
        SNAKE_SCRIBE_REQUIRE_LOGIN=False,
        SNAKE_ACCESS_SECRET_KEY="encryptme",
        SNAKE_ACCESS_BASE_TEMPLATE="base.html",
        SNAKE_ACCESS_MFA_ENABLED=True,
        SNAKE_ACCESS_PIN_ENABLED=True,
        SNAKE_PERMISSIONS_DATABASE=Path(app.instance_path) / "snake_permissions.sqlite",
        # SNAKE_PERMISSIONS_BASE_TEMPLATE="base.html",
    )

    # +-----------------------------------------------------------------------+
    # [+] CONFIGURATION FROM FILE
    #
    # Loads instance/config.py if exists.
    # +-----------------------------------------------------------------------+
    app.config.from_pyfile("config.py", silent=True)

    # +-----------------------------------------------------------------------+
    # [+] TEST CONFIGURATION
    #
    # Override config for testing.
    #
    # Example (/run.py):
    #
    # ```python
    # app = create_app({
    #     "SECRET_KEY": "test-secret"
    # })
    # ```
    # +-----------------------------------------------------------------------+
    if test_config is not None:
        app.config.update(test_config)

    # [*] Makes sure ./instance exists.
    os.makedirs(app.instance_path, exist_ok=True)

    # log.info(f"***** INSTANCE******: {app.instance_path}")

    app.teardown_appcontext(close_db)

    # +-----------------------------------------------------------------------+
    # [+] DATABASES
    # +-----------------------------------------------------------------------+

    db.register(
        "access",
        SQLiteBackend(Path(app.instance_path) / "data.sqlite"),
    )

    db.register(
        "permissions",
        SQLiteBackend(app.config["SNAKE_PERMISSIONS_DATABASE"]),
    )

    db.init_app(app)

    app.cli.add_command(init_db)

    # +-----------------------------------------------------------------------+
    # [+] SESSION
    # +-----------------------------------------------------------------------+

    app.permanent_session_lifetime = timedelta(minutes=app.config.get("SESSION_TIMEOUT", 60))

    # +-----------------------------------------------------------------------+
    # [+] EXTENSIONS
    # +-----------------------------------------------------------------------+
    linguae = ensure_linguae(app)
    # linguae.register_package("snake_vault.flask.example.app.dictionaries")

    access.init_app(app)

    ensure_snake_common(app)

    authentication_manager.init_app(app)

    tables.init_app(app)

    quiz.init_app(app)

    scribe.init_app(app)

    permissions.init_app(app)

    lists.init_app(app)

    # +-----------------------------------------------------------------------+
    # [+] ROUTES + BLUEPRINTS
    # +-----------------------------------------------------------------------+
    @app.route("/", methods=["GET"])
    @login_required
    def index():

        display_language = get_language_dictionary()

        # log.info(str(getattr(g, "current_user", None).username) + " from " + get_client_ip(), category="ACCESS")

        # display_app_context()

        return render_template(
            'index.html',
            title=display_language.get("HOME-Welcome", "Welcome"),
            display_language=display_language
        )

    # from .blueprints.auth import bp as _auth
    # app.register_blueprint(_auth, url_prefix="/")

    # from .blueprints.admin import bp as _admin
    # app.register_blueprint(_admin, url_prefix="/")

    from .blueprints.list import bp as _list
    app.register_blueprint(_list, url_prefix="/")

    return app
