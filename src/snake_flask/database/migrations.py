# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/database/migration.py]                       |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-05-19 11:56:16 UTC                                     |
# | Updated     : 2026-06-25 11:19:05 UTC                                     |
# | Description : Migration.                                                  |
# +---------------------------------------------------------------------------+
from __future__ import annotations

import shutil
from pathlib import Path

import click

from .extension import get_backend, get_db


def create_migration_table(database: str = "default") -> None:
    conn = get_db(database)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

def migration_exists(
    version: str,
    database: str = "default",
) -> bool:

    create_migration_table(database)

    conn = get_db(database)

    backend = get_backend(database)

    placeholder = backend.placeholder()

    row = conn.execute(
        f"""
        SELECT 1
        FROM schema_migrations
        WHERE version = {placeholder}
        """,
        (version,),
    ).fetchone()

    return row is not None

def record_migration(
    version: str,
    database: str = "default",
) -> None:

    create_migration_table(database)

    conn = get_db(database)

    backend = get_backend(database)

    placeholder = backend.placeholder()

    conn.execute(
        f"""
        INSERT INTO schema_migrations (version)
        VALUES ({placeholder})
        """,
        (version,),
    )

def apply_migration(
    migration_path: str | Path,
    database: str = "default",
    backup_path: str | Path | None = None,
) -> None:
    migration_path = Path(migration_path)

    if not migration_path.exists():
        raise click.ClickException(
            f"Migration file not found: {migration_path}"
        )

    version = migration_path.name

    if migration_exists(version, database):
        raise click.ClickException(
            f"Migration already applied: {version}"
        )

    conn = get_db(database)

    if backup_path is not None:
        shutil.copy2(backup_path, f"{backup_path}.backup-{version}")

    sql = migration_path.read_text(encoding="utf-8")

    backend = get_backend(database)

    try:
        conn.execute("BEGIN")

        backend.execute_script(conn, sql)

        record_migration(version, database)

        conn.commit()

    except Exception as e:

        conn.rollback()

        raise click.ClickException(
            f"Migration failed: {e}"
        ) from e
