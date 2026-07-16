# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/database/cli.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-01 17:01:02 UTC
# Updated     : 2026-07-13 10:52:40 UTC
# Description : SnakeDatabase CLI.
# +---------------------------------------------------------------------------+

from __future__ import annotations

from pathlib import Path

import click
from flask import current_app
from flask.cli import with_appcontext

from .migrations import apply_migration, create_migration_table

@click.command("init-snake-db")
@with_appcontext
def init_snake_db_command() -> None:
    initialized = 0

    for extension_name, extension in current_app.extensions.items():
        initializer = getattr(extension, "init_db", None)

        if not callable(initializer):
            continue

        click.echo(f"Initializing {extension_name}...")

        try:
            initializer()
        except Exception as error:
            raise click.ClickException(
                f"Could not initialize {extension_name}: {error}"
            ) from error

        initialized += 1

    if initialized == 0:
        click.echo("No database-enabled Snake extensions are registered.")
        return

    click.echo("Snake extension databases initialized.")

@click.command("db-init-migrations")
@click.option("--database", default="default")
@with_appcontext
def init_migrations_command(database: str) -> None:
    create_migration_table(database)

    click.echo(f"Migration table initialized: {database}")

@click.command("db-migrate")
@click.option("--database", default="default")
@click.argument("migration_file")
@with_appcontext
def migrate_command(database: str, migration_file: str) -> None:
    migration_path = (
        Path(current_app.root_path)
        .parent
        / "migrations"
        / migration_file
    )

    apply_migration(
        migration_path=migration_path,
        database=database,
    )

    click.echo(f"Migration applied: {migration_file}")
