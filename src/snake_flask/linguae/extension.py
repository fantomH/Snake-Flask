# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/linguae/extension.py]                        |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-03 17:48:07 UTC                                     |
# | Updated     : 2026-06-30 12:53:13 UTC                                     |
# | Description : SnakeLinguae extension.                                     |
# +---------------------------------------------------------------------------+

from __future__ import annotations

from importlib import import_module
from types import ModuleType

from flask import Flask
from flask import current_app
from flask import g

class SnakeLinguae:
    def __init__(self, app=None):
        self.language_packages: list[str] = []

        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        if "snake_linguae" in app.extensions:
            return app.extensions["snake_linguae"]

        app.extensions["snake_linguae"] = self

        app.config.setdefault("DEFAULT_LANGUAGE", "english")
        app.config.setdefault("LINGUAE_PACKAGES", [])
        app.config.setdefault("LINGUAE_CUSTOM", {})

        @app.before_request
        def load_display_language():
            g.display_language = self.get_display_language()

        app.jinja_env.globals["get_display_language"] = get_display_language
        app.jinja_env.globals["get_language_dictionary"] = get_language_dictionary

    def register_package(self, package_path: str) -> None:
        if package_path not in self.language_packages:
            self.language_packages.append(package_path)

    def get_display_language(self) -> str:
        user = getattr(g, "current_user", None)

        if user and getattr(user, "language", None):
            return user.language

        return current_app.config.get("DEFAULT_LANGUAGE", "english")

    def _load_module(self, package_path: str, language: str) -> ModuleType | None:
        module_path = f"{package_path}.{language}"

        try:
            return import_module(module_path)
        except ModuleNotFoundError as error:
            if error.name == module_path:
                return None
            raise

    def _load_dicts_from_package(
        self,
        package_path: str,
        language: str,
        prefix: str | None = None,
    ) -> dict:
        module = self._load_module(package_path, language)

        if module is None:
            return {}

        merged = {}

        for name in dir(module):
            if name.startswith("_"):
                continue

            if prefix and not name.startswith(prefix):
                continue

            value = getattr(module, name)

            if isinstance(value, dict):
                merged.update(value)

        return merged

    def get_language_dictionary(
        self,
        language: str | None = None,
        prefix: str | None = None,
        custom: dict[str, dict] | None = None,
    ) -> dict:
        language = language or self.get_display_language()

        merged = {}

        # [*] Linguae's own default dictionary.
        merged.update(
            self._load_dicts_from_package(
                "snake_flask.linguae.dictionaries",
                language,
                prefix="LINGUAE",
            )
        )

        packages = [
            *current_app.config.get("LINGUAE_PACKAGES", []),
            *self.language_packages,
        ]

        for package_path in packages:
            merged.update(
                self._load_dicts_from_package(
                    package_path,
                    language,
                    prefix=prefix,
                )
            )

        config_custom = current_app.config.get("LINGUAE_CUSTOM", {})
        merged.update(config_custom.get(language, {}))

        if custom:
            merged.update(custom.get(language, {}))

        return merged

def ensure_linguae(app) -> SnakeLinguae:
    """
    Initiate SnakeLinguae only if the extension does not exists.

    This avoids creating multiple conflicting instances of SnakeLinguae.
    """
    if "snake_linguae" not in app.extensions:
        SnakeLinguae(app)

    return app.extensions['snake_linguae']

def get_display_language() -> str:
    extension = current_app.extensions["snake_linguae"]
    return extension.get_display_language()

def get_language_dictionary(
    language: str | None = None,
    prefix: str | None = None,
    custom: dict[str, dict] | None = None,
) -> dict:
    extension = current_app.extensions["snake_linguae"]
    return extension.get_language_dictionary(language, prefix, custom)
