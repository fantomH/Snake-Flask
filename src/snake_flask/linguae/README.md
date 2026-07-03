<!--
+---------------------------------------------------------------------- INFO -+
| [Snake-Flask/src/snake_flask/linguae/README.md]                             |
|                                                                             |
| Author      : Pascal Malouin (https://github.com/fantomH)                   |
| Created     : 2026-06-22 14:47:52 UTC                                       |
| Updated     : 2026-06-22 14:47:52 UTC                                       |
| Description : SnakeLinguae README.                                          |
+-----------------------------------------------------------------------------+
-->

# snake_flask.linguae

Multi language display extensions for Flask applications.

---

## API

Extension name: `snake_linguae`.

| | Description | |
| :- | :- | :- |
| SnakeLinguae | extension *class* responsible for managing languages and translation dictionaries.  |
| get_display_language() | Return the display language. Default: english. |
| get_language_dictionary() | Return the language dictionary. |
| ensure_linguae() | Verification helper for SnakeLinguae extension. |

### *class* linguae.SnakeLinguae
        app.config.setdefault("DEFAULT_LANGUAGE", "english")
        app.config.setdefault("LINGUAE_PACKAGES", [])
        app.config.setdefault("LINGUAE_CUSTOM", {})

        app.extensions["snake_linguae"] = self

### linguae.get_display_language() -> str

### linguae.get_language_dictionary(*language, prefix, custom*) -> dict

    language: str | None = None,
    prefix: str | None = None,
    custom: dict[str, dict] | None = None,

### linguae.ensure_linguae(*app*) -> SnakeLinguae

Initiates SnakeLinguae only if the extension does not exist.

This avoids creating multiple conflicting instances of SnakeLinguae.

Example:

Instead of the traditional way of initiating the extension.

```python
from flask import Flask
from snake_flask.linguae import SnakeLinguae

linguae = SnakeLinguae()

def create_app():

    app = Flask(__name__)

    linguae.init_app(app)
    linguae.register_package("snake_vault.flask.example.app.linguae")
    linguae.register_package("snake_vault.flask.snake_tables.linguae")

    return app
```

We recommand using `ensure_linguae()`.

```python
from flask import Flask
from snake_flask.linguae import ensure_linguae

def create_app():

    app = Flask(__name__)

    linguae = ensure_linguae(app)
    linguae.register_package("snake_vault.flask.example.app.linguae")
    linguae.register_package("snake_vault.flask.snake_tables.linguae")

    return app
```

## Default Configuration

        app.config.setdefault("DEFAULT_LANGUAGE", "english")
        app.config.setdefault("LINGUAE_PACKAGES", [])
        app.config.setdefault("LINGUAE_CUSTOM", {})

