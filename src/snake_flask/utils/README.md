<!--
+---------------------------------------------------------------------- INFO -+
| [Snake-Flask/src/snake_flask/utils/README.md]                               |
|                                                                             |
| Author      : Pascal Malouin (https://github.com/fantomH)                   |
| Created     : 2026-06-05 14:30:59 UTC                                       |
| Updated     : 2026-06-30 12:46:24 UTC                                       |
| Description : Utilities for Flask applications.                             |
+-----------------------------------------------------------------------------+
-->

# snake_flask.utils

Utilities for Flask applications.

## Overview

The `snake_flask.utils` contains reusable helper functions that simplify common Flask development tasks.

### API

| Function          | Description                                    |
| ----------------- | ---------------------------------------------- |
| `display_app_context()` | Print app context. |
| `get_client_ip()` | Return the IP address of the connected client. |

---

#### utils.display_app_context() -> None

Prints the app context. Useful for debugging.

---

#### utils.get_client_ip(*trust_proxy=True*) -> str

Returns the IP address of the connected client.

When `trust_proxy` is enabled, the function checks the `X-Forwarded-For` HTTP header before falling back to Flask's `request.remote_addr`.

This is useful when the application is deployed behind a reverse proxy such as Nginx, Apache, HAProxy, Cloudflare, or a load balancer.

##### Examples

```python
from flask import Flask
from snake_flask.utils import get_client_ip

app = Flask(__name__)

@app.route("/")
def index():
    return f"Your IP address is {get_client_ip()}"
```

`get_client_ip()` is also exposed at the root level of `snake_flask`.

Thus, `from snake_flask import get_client` or `from snake_flask.utils import get_client` are equivalent.

If `from snake_flask import utils` is used, then `utils.get_client_ip()` must be used.

##### Notes

When running behind a reverse proxy, ensure that the proxy is configured to set the `X-Forwarded-For` header correctly.

Because HTTP headers can be forged by clients, `trust_proxy=True` should only be used when requests are received through a trusted proxy infrastructure.
