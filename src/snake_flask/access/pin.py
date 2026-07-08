# [INFO] -------------------------------------------------------------------- +
# | [Snake-Flask/src/snake_flask/access/pin.py]
# |
# | Author      : Pascal Malouin (https://github.com/fantomH)
# | Created     : 2026-07-06 20:00:00 UTC
# | Updated     : 2026-07-06 20:00:00 UTC
# | Description : PIN helper and @pin_required decorator.
# + ------------------------------------------------------------------------- +

from __future__ import annotations

import base64
import hashlib
from collections.abc import Callable
from functools import wraps
from typing import Any

from cryptography.fernet import Fernet
from flask import Flask, current_app, redirect, request, session, url_for

SecretProvider = str | Callable[[], str]

class PIN:
    """
    Snake-Access PIN helper.

    Config:

        SNAKE_ACCESS_SECRET_KEY
        SNAKE_ACCESS_PIN_LENGTH

    User table fields expected:

        pin_enabled: bool
        pin_secret: str | None

    The PIN is encrypted because Snake-Access needs to compare the entered PIN
    against the configured PIN. If you later do not need to recover the PIN,
    prefer hashing instead of encryption.
    """

    def __init__(self, app: Flask | None = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.extensions["snake_access_pin"] = self

        # [+] --------------------------------------------------------------- +
        # | Configuration
        # + ----------------------------------------------------------------- +
        app.config.setdefault("SNAKE_ACCESS_PIN_LENGTH", 4)
        app.config.setdefault("SNAKE_ACCESS_PIN_REQUIRED", False)
        app.config.setdefault("SNAKE_ACCESS_PIN_ENABLED", False)
        app.config.setdefault("SNAKE_ACCESS_PIN_CONFIRM_TIMEOUT", 10) # time in seconds

    def get_secret_key(self) -> str:
        value: SecretProvider | None = current_app.config.get(
            "SNAKE_ACCESS_SECRET_KEY"
        )

        if value is None:
            raise RuntimeError(
                "Missing SNAKE_ACCESS_SECRET_KEY. "
                "This key is required to encrypt PIN secrets."
            )

        if callable(value):
            value = value()

        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(
                "SNAKE_ACCESS_SECRET_KEY must be a non-empty string "
                "or a callable returning a non-empty string."
            )

        return value

    def get_fernet(self) -> Fernet:
        """
        Derive a Fernet encryption key from SNAKE_ACCESS_SECRET_KEY.
        """

        secret_key = self.get_secret_key()

        digest = hashlib.sha256(secret_key.encode("utf-8")).digest()
        key = base64.urlsafe_b64encode(digest)

        return Fernet(key)

    def encrypt_secret(self, pin: str) -> str:
        fernet = self.get_fernet()

        return fernet.encrypt(pin.encode("utf-8")).decode("utf-8")

    def decrypt_secret(self, encrypted_secret: str) -> str:
        fernet = self.get_fernet()

        return fernet.decrypt(
            encrypted_secret.encode("utf-8")
        ).decode("utf-8")

    def verify_pin(
        self,
        *,
        encrypted_secret: str,
        pin: str,
    ) -> bool:
        if not encrypted_secret:
            return False

        secret = self.decrypt_secret(encrypted_secret)

        return secret == pin


def _get_current_user() -> Any | None:
    """
    Fetch the current user using the same User model style as the MFA routes.
    """

    try:
        from app.models.user import User
    except ImportError:
        return None

    user_id = session.get("user_id")

    if user_id is None:
        return None

    return User.fetch_by_id(user_id)
