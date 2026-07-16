# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/database/database.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-05-19 11:56:16 UTC
# Updated     : 2026-07-13 11:03:10 UTC
# Description : Database.
# +---------------------------------------------------------------------------+

import sqlite3
from pathlib import Path

from flask import current_app
from flask import g

def get_db(database):

    if "databases" not in g:
        g.databases = {}

    if database not in g.databases:

        conn = sqlite3.connect(database)

        conn.row_factory = sqlite3.Row

        g.databases[database] = conn

    return g.databases[database]

def close_db(error=None):

    databases = g.pop("databases", {})

    for conn in databases.values():
        conn.close()
