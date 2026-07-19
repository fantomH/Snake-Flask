# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/common/http_errors.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-16 21:40:02 UTC
# Updated     : 2026-07-16 21:40:02 UTC
# Description : Statuses.
# +---------------------------------------------------------------------------+

from flask import render_template

HTTP_ERROR_PAGES = {
    401: {
        "title": "Authentication required",
        "message": "Please log in to continue.",
        "image": "401-unauthorized.png",
    },
    403: {
        "title": "Access denied",
        "message": "You do not have permission to access this page.",
        "image": "403-forbidden.png",
    },
    404: {
        "title": "Page not found",
        "message": "The requested page could not be found.",
        "image": "404-not-found.png",
    },
}

def render_status(code):
    http_error_info = HTTP_ERROR_PAGES[code]

    return (
        render_template(
            "snake_common/http_errors.html",
            code=code,
            **http_error_info,
        ),
        code,
    )
