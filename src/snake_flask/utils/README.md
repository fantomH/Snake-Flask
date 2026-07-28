<!--
+-----------------------------------------------------------------------------+ 
[+] INFO
+-----------------------------------------------------------------------------+
[Snake-Flask/src/snake_flask/utils/README.md]

Author      : Pascal Malouin (https://github.com/fantomH)
Created     : 2026-06-05 14:30:59 UTC
Updated     : 2026-07-27 12:14:38 UTC
Description : Snake-Flask Utils README.
+-----------------------------------------------------------------------------+
-->

# snake_flask.utils

Utilities for Flask applications.

## Overview

The `snake_flask.utils` module contains reusable helper functions that simplify common Flask development tasks.

## API

| Function | Description | |
| :- | :- | :- |
| `display_app_context()` | Display app context information in terminal. |
| `display_config()` | Display configuration information in terminal. |
| `display_debug()` | Display debug information in terminal. |
| `display_session()` | Display session information in terminal. |
| `get_client_ip()` | Return the IP address of the connected client. |

---

## Functions

### utils.app_info.display_app_context() -> None

|  ⚠️ | This function is part of the `snake_flask` root API, thus we suggest using:<br><br>`from snake_flask import display_app_context`<br><br>This avoids code breaking upon `snake_flask.utils` structural changes. |
| :-: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

Display app context information in the terminal.

### utils.app_info.display_config() -> None

|  ⚠️ | This function is part of the `snake_flask` root API, thus we suggest using:<br><br>`from snake_flask import display_config`<br><br>This avoids code breaking upon `snake_flask.utils` structural changes. |
| :-: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

Display configuration information in the terminal.

### utils.app_info.display_debug(*values*: dict) -> None

|  ⚠️ | This function is part of the `snake_flask` root API, thus we suggest using:<br><br>`from snake_flask import display_debug`<br><br>This avoids code breaking upon `snake_flask.utils` structural changes. |
| :-: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

Display debug information in the terminal.

This is quite useful to get debug information at different stage.

```python
from snake_flask import display_debug

display_debug({
    "id(session)": id(session),
    "session": dict(session),
})
```

### utils.display_session() -> None

|  ⚠️ | This function is part of the `snake_flask` root API, thus we suggest using:<br><br>`from snake_flask import display_session`<br><br>This avoids code breaking upon `snake_flask.utils` structural changes. |
| :-: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

Display session information in the terminal.

### utils.network.get_client_ip(*trust_proxy=True*) -> str

|  ⚠️ | This function is part of the `snake_flask` root API, thus we suggest using:<br><br>`from snake_flask import get_client_ip`<br><br>This avoids code breaking upon `snake_flask.utils` structural changes. |
| :-: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

Returns the IP address of the connected client.

When `trust_proxy` is enabled, the function checks the `X-Forwarded-For` HTTP header before falling back to Flask's `request.remote_addr`.

This is useful when the application is deployed behind a reverse proxy such as Nginx, Apache, HAProxy, Cloudflare, or a load balancer.

```python
from flask import Flask
from snake_flask import get_client_ip

app = Flask(__name__)

@app.route("/")
def index():
    return f"Your IP address is {get_client_ip()}"
```

When running behind a reverse proxy, ensure that the proxy is configured to set the `X-Forwarded-For` header correctly.

Because HTTP headers can be forged by clients, `trust_proxy=True` should only be used when requests are received through a trusted proxy infrastructure.

---
