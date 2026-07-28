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

---

## Overview

The `snake_flask.access` extension provides:

* Basic login, sign-up and logout pages.
* Multi-factor and PIN setup and access capability.
* A set of required condiditional decorator such as `@login_required` to manage access to routes.

---

## Default Configuration

### *config* SNAKE_ACCESS_DATABASE

Defautl: `access.sqlite`

### `SNAKE_ACCESS_URL_PREFIX`

Default: `/authentication`

| `SNAKE_ACCESS_BASE_TEMPLATE` | Base template used by the extension | None |
| `SNAKE_ACCESS_SECRET_KEY` | Secret key used by MFA | None |
| `SNAKE_ACCESS_PASSWORD_CONFIRM_TIMEOUT` | | 60 (seconds) |

| Class | Description |    |
| :------------ | :---------- | :- |

| Function | Description |    |
| :------------ | :---------- | :- |

