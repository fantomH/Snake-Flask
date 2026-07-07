# [INFO] -------------------------------------------------------------------- +
# | [Snake-Flask/src/snake_flask/utils/app_info.py]                           |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-22 16:22:17 UTC                                     |
# | Updated     : 2026-07-07 19:48:23 UTC                                     |
# | Description : Flask app info.                                             |
# +---------------------------------------------------------------------------+

from datetime import datetime
from inspect import currentframe
from inspect import getframeinfo
from pathlib import Path
from textwrap import wrap

from flask import current_app
from flask import g
from flask import request
from flask import session
from flask import has_app_context

TOTAL_WIDTH = 80

def _line(prefix: str) -> None:
    suffix = " +"
    dash_count = TOTAL_WIDTH - len(prefix) - len(suffix)
    print(prefix + "-" * dash_count + suffix)


def _header(title: str) -> None:
    frame = currentframe().f_back.f_back
    info = getframeinfo(frame)

    filename = Path(info.filename)
    location = f"{filename.parent.name}/{filename.name} line {info.lineno}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print()
    _line(f"# [ {title.upper()} ] ")
    print(f"# | [{location}] at {timestamp}")
    print("# |")


def _footer() -> None:
    _line("# + ")
    print()


def _print_wrapped_key_value(
    key: str,
    value,
    longest: int,
) -> None:
    value = repr(value)

    prefix = f"# | {key:<{longest}} : "
    continuation = "# | " + " " * (longest + 3)

    available_width = TOTAL_WIDTH - len(prefix)

    first_line = True

    for paragraph in value.splitlines() or [""]:
        wrapped_lines = wrap(
            paragraph,
            width=available_width,
            break_long_words=False,
            break_on_hyphens=False,
        ) or [""]

        for line in wrapped_lines:
            if first_line:
                print(prefix + line)
                first_line = False
            else:
                print(continuation + line)


def _dictionary(title: str, mapping) -> None:
    _header(title)

    if not mapping:
        print("# | (empty)")
        _footer()
        return

    longest = max(len(str(key)) for key in mapping)

    for key, value in sorted(mapping.items()):
        _print_wrapped_key_value(
            key=str(key),
            value=value,
            longest=longest,
        )

    _footer()

def display_session():
    _dictionary("SESSION", session)

def display_config():
    _dictionary("CONFIG", current_app.config)

def display_debug(values: dict):
    _dictionary("DEBUG", values)

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
