# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/tables/table.py]                             |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-04 12:32:04 UTC                                     |
# | Updated     : 2026-06-24 16:13:08 UTC                                     |
# | Description : SnakeTables table generator.                                |
# +---------------------------------------------------------------------------+

from flask import current_app
from flask import render_template
from flask import request

from snake_flask.linguae import get_language_dictionary

class Table:

    def __init__(
        self,
        table_id,
        data_url,
        data_update_url=None,
        db=None,
        columns=None,
        source_table=None,
        row_identifier="id",
        default_order_by=None,
    ):
        self.table_id = table_id
        self.data_url = data_url
        self.data_update_url = data_update_url or ""
        self.db = db
        self.columns = columns or []
        self.source_table = source_table
        self.row_identifier = row_identifier
        self.default_order_by = default_order_by

    def load(self):

        display_language = get_language_dictionary()

        return render_template(
            "snake_tables/table.html",
            table=self,
            display_language=display_language,
        )

    def get_searchable_columns(self):
        return [
            column["name"]
            for column in self.columns
            if column.get("searchable")
        ]

    def get_db_columns(self):
        columns = [
            column["name"]
            for column in self.columns
            if column.get("db", True)
        ]

        if self.row_identifier not in columns:
            columns.insert(0, self.row_identifier)

        return columns

    def get_select_clause(self):
        return ", ".join(self.get_db_columns())

    def build_search_where(self, search):
        searchable_columns = self.get_searchable_columns()

        if not search or not searchable_columns:
            return "", []

        conditions = [
            f"{column} LIKE ?"
            for column in searchable_columns
        ]

        where = f"WHERE {' OR '.join(conditions)}"
        params = [f"%{search}%"] * len(searchable_columns)

        return where, params

    def get_sortable_columns(self):
        return [
            column["name"]
            for column in self.columns
            if column.get("sortable") and column.get("db", True)
        ]

    def build_order_clause(self, sort_column, sort_direction):
        sortable_columns = self.get_sortable_columns()

        if sort_column not in sortable_columns:
            if self.default_order_by:
                return f"ORDER BY {self.default_order_by}"

            return ""

        if sort_direction not in ["asc", "desc"]:
            sort_direction = "asc"

        return f"ORDER BY {sort_column} {sort_direction.upper()}"

    def get_data(self):
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 25))
        search = request.args.get("search", "").strip()
        sort_column = request.args.get("sort_column", "").strip()
        sort_direction = request.args.get("sort_direction", "asc").strip().lower()

        offset = (page - 1) * page_size

        select_clause = self.get_select_clause()
        where, params = self.build_search_where(search)

        order_clause = self.build_order_clause(
            sort_column,
            sort_direction,
        )

        total = self.db.execute(
            f"""
            SELECT COUNT(*)
            FROM {self.source_table}
            {where}
            """,
            params,
        ).fetchone()[0]

        rows = self.db.execute(
            f"""
            SELECT {select_clause}
            FROM {self.source_table}
            {where}
            {order_clause}
            LIMIT ? OFFSET ?
            """,
            params + [page_size, offset],
        ).fetchall()

        return {
            "rows": [dict(row) for row in rows],
            "page": page,
            "page_size": page_size,
            "total": total,
        }
