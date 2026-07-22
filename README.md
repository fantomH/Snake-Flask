<!--
+-----------------------------------------------------------------------------+ 
[+] INFO
+-----------------------------------------------------------------------------+
[Snake-Flask/README.md]

Author      : Pascal Malouin (https://github.com/fantomH)
Created     : 2026-06-05 14:30:59 UTC
Updated     : 2026-07-20 11:21:52 UTC
Description : Flask utilities and extensions.
+-----------------------------------------------------------------------------+
-->

# Snake-Flask

Flask utilities and extensions.

## API

| Module | Description | |
| :- | :- | :- |
| access | Authentication and User management extension. | see [Snake-Flask/access](https://github.com/fantomH/Snake-Flask/blob/main/src/snake_flask/access/README.md) |
| common | Shared assets. | see [Snake-Flask/common](https://github.com/fantomH/Snake-Flask/blob/main/src/snake_flask/common/README.md) |
| database | Database management. | see [Snake-Flask/database](https://github.com/fantomH/Snake-Flask/blob/main/src/snake_flask/database/README.md) |
| linguae | Multi-language display extension. | see [Snake-Flask/linguae](https://github.com/fantomH/Snake-Flask/blob/main/src/snake_flask/linguae/README.md) |
| lists | List generator extension. | see [Snake-Flask/lists](https://github.com/fantomH/Snake-Flask/blob/main/src/snake_flask/lists/README.md) |
| permissions | Permissions management extension. | see [Snake-Flask/permissions](https://github.com/fantomH/Snake-Flask/blob/main/src/snake_flask/permissions/README.md) |
| quiz | Quiz generator extension. | see [Snake-Flask/quiz](https://github.com/fantomH/Snake-Flask/blob/main/src/snake_flask/quiz/README.md) |
| tables | Table generator extension. | see [Snake-Flask/tables](https://github.com/fantomH/Snake-Flask/blob/main/src/snake_flask/tables/README.md) |
| utils | Miscellaneous utilities | see [Snake-Flask/Utils](https://github.com/fantomH/Snake-Flask/blob/main/src/snake_flask/utils/README.md) |

| Function | Description | |
| :- | :- | :- |
| get_client_ip() | Return the IP address of the connected client. | |
| display_session() | Display session information in terminal. ||
| display_config() | Display configuration information in terminal. ||
| display_debug() | Display debug information in terminal. ||
| display_app_context() | Display app context information in terminal. ||

## Installation

## Quick Start

Snake-Flask is designed as a set of extensions or plugins.

You choose and initiate what you need.

```python

import os
from datetime import timedelta
from pathlib import Path

from flask import Flask
from flask import g
from flask import render_template

from snake_flask.access import SnakeAccess
from snake_flask.access import authentication_manager
from snake_flask.common import ensure_snake_common
from snake_flask.database import SQLiteBackend
from snake_flask.database import SnakeDatabase
from snake_flask.database import close_db
from snake_flask.linguae import ensure_linguae
from snake_flask.permissions import SnakePermissions
from snake_flask.tables import SnakeTables

access = SnakeAccess()
db = SnakeDatabase()
permissions = SnakePermissions()
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
        DEFAULT_LANGUAGE="french",
        SECRET_KEY="secret",
        SESSION_TIMEOUT=60,
        SNAKE_ACCESS_SECRET_KEY="encryptme",
        SNAKE_ACCESS_BASE_TEMPLATE="base.html",
        SNAKE_PERMISSIONS_DATABASE=Path(app.instance_path) / "snake_permissions.sqlite",
    )

    # +-----------------------------------------------------------------------+
    # [+] CONFIGURATION FROM FILE
    #
    # Loads instance/config.py if exists.
    # +-----------------------------------------------------------------------+
    app.config.from_pyfile("config.py", silent=True)

    # [*] Makes sure ./instance exists.
    os.makedirs(app.instance_path, exist_ok=True)

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

    permissions.init_app(app)

    # +-----------------------------------------------------------------------+
    # [+] ROUTES + BLUEPRINTS
    # +-----------------------------------------------------------------------+
    @app.route("/", methods=["GET"])
    def index():

        return render_template(
            'index.html'
        )

    return app
```
