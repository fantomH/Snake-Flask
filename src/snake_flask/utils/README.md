<!--
+-----------------------------------------------------------------------------+ 
[+] INFO
+-----------------------------------------------------------------------------+
[Snake-Flask/src/snake_flask/utils/README.md]

Author      : Pascal Malouin (https://github.com/fantomH)
Created     : 2026-06-05 14:30:59 UTC
Updated     : 2026-07-21 12:10:02 UTC
Description : Snake-Flask Utils README.
+-----------------------------------------------------------------------------+
-->

# snake_flask.utils

Utilities for Flask applications.

## Overview

The `snake_flask.utils` module contains reusable helper functions that simplify common Flask development tasks.

### API

| Function | Description | |
| :- | :- | :- |
| `display_app_context()` | Display app context information in terminal. |
| `display_config()` | Display configuration information in terminal. |
| `display_debug()` | Display debug information in terminal. |
| `display_session()` | Display session information in terminal. |
| `get_client_ip()` | Return the IP address of the connected client. |

The following functions are exposed at the root Snake-Flask API:

- `display_app_context()`
- `display_config()`
- `display_debug()`
- `display_session()`
- `get_client_ip()`

It is suggested to use, for example `snake_flask.get_client_ip()` instead of `snake_flask.utils.get_client_ip()`. This would avoid code breaking upon changes in the modules' structure.

---

#### `utils.display_app_context()` -> None

Display app context information in the terminal.

#### `utils.display_config()` -> None

Display configuration information in the terminal.

#### `utils.display_debug()` -> None

Display debug information in the terminal.

#### `utils.display_session()` -> None

Display session information in the terminal.

#### utils.get_client_ip(*trust_proxy=True*) -> str

Returns the IP address of the connected client.

When `trust_proxy` is enabled, the function checks the `X-Forwarded-For` HTTP header before falling back to Flask's `request.remote_addr`.

This is useful when the application is deployed behind a reverse proxy such as Nginx, Apache, HAProxy, Cloudflare, or a load balancer.

```python
from flask import Flask
from snake_flask.utils import get_client_ip

app = Flask(__name__)

@app.route("/")
def index():
    return f"Your IP address is {get_client_ip()}"
```

When running behind a reverse proxy, ensure that the proxy is configured to set the `X-Forwarded-For` header correctly.

Because HTTP headers can be forged by clients, `trust_proxy=True` should only be used when requests are received through a trusted proxy infrastructure.
