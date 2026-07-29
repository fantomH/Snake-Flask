<!--
+-----------------------------------------------------------------------------+ 
[+] INFO
+-----------------------------------------------------------------------------+
 [Snake-Flask/src/snake_flask/access/README.md]

 Author      : Pascal Malouin (https://github.com/fantomH)
 Created     : 2026-07-27 20:39:23 UTC
 Updated     : 2026-07-27 20:39:23 UTC
 Description : Snake-Flask Access README
+-----------------------------------------------------------------------------+
-->

# snake_flask.access

Flask extension to manage access, authentication and users.

Extension name: `snake_access`.

---

## Overview

The `snake_flask.access` extension provides:

* Basic login, sign-up and logout pages.
* Multi-factor and PIN setup and access capability.
* A set of required condiditional decorator such as `@login_required` to manage access to routes.

---

## Default Configuration

### *config* `SNAKE_ACCESS_DATABASE`

Defautl: `access.sqlite`

By default, SnakeAccess will use the URI `instance/access.sqlite`.

Only SQLite database can be used for the moment.

### *config* `SNAKE_ACCESS_URL_PREFIX`

Default: `/authentication`

### *config* `SNAKE_ACCESS_BASE_TEMPLATE`

Default: `None`

If no "base" template is specified, `snake_access` will use it own internal base template.

You can integrate `snake_access` templates into your own by setting `SNAKE_ACCESS_BASE_TEMPLATE` to, for example, `base.html`.

### *config* `SNAKE_ACCESS_SECRET_KEY`

Default: `None`

### *config* `SNAKE_ACCESS_PASSWORD_CONFIRM_TIMEOUT`

Default: `60` seconds

### *config* `SNAKE_ACCESS_MFA_ISSUER`

Default: `Snake-Access`

### *config* `SNAKE_ACCESS_MFA_VALID_WINDOW`

Default: `1`

### *config* `SNAKE_ACCESS_MFA_REQUIRED`

Default: `False`

### *config* `SNAKE_ACCESS_MFA_ENABLED`

Default: `False`

### *config* `SNAKE_ACCESS_MFA_CONFIRM_TIMEOUT`

Default: `10` seconds.

### *config* `SNAKE_ACCESS_PIN_LENGTH`

Default: `4`

### *config* `SNAKE_ACCESS_PIN_REQUIRED`

Default: `False`

### *config* `SNAKE_ACCESS_PIN_ENABLED`

Default: `False`

### *config* `SNAKE_ACCESS_PIN_CONFIRM_TIMEOUT`

Default: `10` seconds.

---

## *class* SnakeAccess

Main `snake_access` class. This must be initated in your app.

```python
from flask import Flask, render_template

from snake_flask.access import SnakeAccess

access = SnakeAccess()

def create_app(instance_path=None):

    app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)

    app.config.from_pyfile("config.py", silent=True)

    access.init_app(app)

    @app.route("/", methods=["GET"])
    def index():
        return render_template('index.html')

    return app

```

As of now, a landing "index" must be defined by the developper, which is required to complete the login and authentication routine.
