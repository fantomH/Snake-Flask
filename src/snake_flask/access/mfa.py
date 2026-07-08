# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/access/mfa.py]                               |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-05 15:28:04 UTC                                     |
# | Updated     : 2026-07-05 15:28:04 UTC                                     |
# | Description : MFA.                                                        |
# +---------------------------------------------------------------------------+

from __future__ import annotations

import base64
import hashlib
from collections.abc import Callable
from dataclasses import dataclass

import pyotp
from cryptography.fernet import Fernet
from flask import Flask, current_app

SecretProvider = str | Callable[[], str]

@dataclass
class MFASetup:
    secret: str
    encrypted_secret: str
    provisioning_uri: str

class MFA:
    """
    Snake-Access MFA helper.

    Config:

        SNAKE_ACCESS_SECRET_KEY
        SNAKE_ACCESS_MFA_ISSUER
        SNAKE_ACCESS_MFA_VALID_WINDOW
    """

    def __init__(self, app: Flask | None = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.extensions["snake_access_mfa"] = self

        # [+] --------------------------------------------------------------- +
        # | Configuration
        # + ----------------------------------------------------------------- +
        app.config.setdefault("SNAKE_ACCESS_MFA_ISSUER", "Snake-Access")
        app.config.setdefault("SNAKE_ACCESS_MFA_VALID_WINDOW", 1)
        app.config.setdefault("SNAKE_ACCESS_MFA_REQUIRED", False)
        app.config.setdefault("SNAKE_ACCESS_MFA_ENABLED", False)
        app.config.setdefault("SNAKE_ACCESS_MFA_CONFIRM_TIMEOUT", 10) # time in seconds

    def get_secret_key(self) -> str:
        value: SecretProvider | None = current_app.config.get(
            "SNAKE_ACCESS_SECRET_KEY"
        )

        if value is None:
            raise RuntimeError(
                "Missing SNAKE_ACCESS_SECRET_KEY. "
                "This key is required to encrypt MFA secrets."
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

    def encrypt_secret(self, secret: str) -> str:
        fernet = self.get_fernet()

        return fernet.encrypt(secret.encode("utf-8")).decode("utf-8")

    def decrypt_secret(self, encrypted_secret: str) -> str:
        fernet = self.get_fernet()

        return fernet.decrypt(
            encrypted_secret.encode("utf-8")
        ).decode("utf-8")

    def generate_setup(self, username: str) -> MFASetup:
        secret = pyotp.random_base32()

        encrypted_secret = self.encrypt_secret(secret)

        issuer = current_app.config.get(
            "SNAKE_ACCESS_MFA_ISSUER",
            "Snake-Access",
        )

        provisioning_uri = pyotp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name=issuer,
        )

        return MFASetup(
            secret=secret,
            encrypted_secret=encrypted_secret,
            provisioning_uri=provisioning_uri,
        )

    def verify_code(
        self,
        *,
        encrypted_secret: str,
        code: str,
        valid_window: int | None = None,
    ) -> bool:
        if valid_window is None:
            valid_window = current_app.config.get(
                "SNAKE_ACCESS_MFA_VALID_WINDOW",
                1,
            )

        secret = self.decrypt_secret(encrypted_secret)

        totp = pyotp.TOTP(secret)

        return bool(
            totp.verify(
                code,
                valid_window=valid_window,
            )
        )
