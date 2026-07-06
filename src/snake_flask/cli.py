# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/cli.py]                                      |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-03 19:21:42 UTC                                     |
# | Updated     : 2026-07-03 19:21:42 UTC                                     |
# | Description : Snake-Flask command line interface.                         |
# +---------------------------------------------------------------------------+

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import click

def get_version() -> str:
    """Return the installed Snake-Flask version."""

    try:
        return version("Snake-Flask")
    except PackageNotFoundError:
        return "unknown"

@click.group()
def main() -> None:
    """Snake-Flask developer tools."""

@main.command()
def version() -> None:
    """Show installed Snake-Flask version."""

    click.echo(get_version())

@main.command()
@click.option("--host", default="0.0.0.0", show_default=True)
@click.option("--port", default=8070, show_default=True, type=int)
@click.option("--debug", is_flag=True, help="Run Flask in debug mode.")
def demo(host: str, port: int, debug: bool) -> None:
    """Run the Snake-Flask showcase example."""

    from snake_flask.example.app import create_app

    instance_path = Path("~/main/Snake-Flask/src/snake_flask/example/instance").expanduser()

    app = create_app(
        {"SECRET_KEY": "test-secret"},
        instance_path=instance_path,
    )

    app.run(
        host=host,
        port=port,
        debug=debug,
    )
