# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/utils/network.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-06-04 20:28:00 UTC
# Updated     : 2026-07-21 11:59:15 UTC
# Description : Network helpers.
# +---------------------------------------------------------------------------+

from flask import request

def get_client_ip(trust_proxy: bool = True) -> str | None:
    """
    Return the client's IP address.

    Parameters
    ----------
    trust_proxy : bool
        If True, use X-Forwarded-For when present.
        If False, use REMOTE_ADDR only.
    """

    if trust_proxy:
        xff: str | None = request.headers.get("X-Forwarded-For")

        if xff:
            return xff.split(",")[0].strip()

    return request.remote_addr
