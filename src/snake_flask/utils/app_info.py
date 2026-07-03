# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/utils/app_info.py] |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-22 16:22:17 UTC                                     |
# | Updated     : 2026-06-22 16:22:17 UTC                                     |
# | Description : Flask app info.                                             |
# +---------------------------------------------------------------------------+

from flask import current_app
from flask import has_app_context


def display_app_context() -> None:
    """Print attributes accessible through current_app."""

    if not has_app_context():
        print("No Flask application context active.")
        return

    print()
    print("=" * 80)
    print("[!] Attributes accessible within app_context:")

    for attr_name in dir(current_app):
        if not attr_name.startswith("_"):
            try:
                attr_value = getattr(current_app, attr_name)
                print(f"{attr_name}: {attr_value}")
            except Exception as error:
                print(f"{attr_name}: <error: {error}>")

    print("=" * 80)
    print()
