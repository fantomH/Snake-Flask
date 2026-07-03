# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/example/app/db.py]                           |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-01 20:32:16 UTC                                     |
# | Updated     : 2026-07-01 20:32:16 UTC                                     |
# | Description : Database.                                                   |
# +---------------------------------------------------------------------------+

import shutil
import sqlite3
from pathlib import Path

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext

@click.command("init-db")
@with_appcontext
def init_db():
    """
    Run in terminal `flask --app run init-db` to initialize the db.
    """

    from .models.user import User

    User.create_table()
    User.create_user(
        username="admin",
        firstname="",
        lastname="",
        email="not@email.com",
        password="password"
    )

    click.echo(
        "DATABASE db initialized. "
        "Default login: admin / password"
    )
