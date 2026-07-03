# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/lists/list.py]                               |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-02 15:22:16 UTC                                     |
# | Updated     : 2026-07-03 14:35:37 UTC                                     |
# | Description : Snake-Lists main class.                                     |
# +---------------------------------------------------------------------------+

from math import ceil
from typing import Any

from flask import render_template
from flask import request
from markupsafe import Markup

try:
    from rapidfuzz import fuzz
except ImportError:
    fuzz = None


class List:
    """Searchable, paginated card list."""

    def __init__(
        self,
        name: str,
        items: list[Any],
        search_fields: list[str],
        card_template: str,
        data_url: str,
        per_page_options: list[int] | None = None,
        default_per_page: int = 25,
        fuzz_threshold: int = 60,
    ):
        self.name = name
        self.list_id = f"snake-list-{name}"

        self.items = list(items)
        self.search_fields = search_fields
        self.card_template = card_template
        self.data_url = data_url

        self.per_page_options = per_page_options or [10, 25, 50, 100]
        self.default_per_page = default_per_page
        self.fuzz_threshold = fuzz_threshold

        self.query = ""
        self.page = 1
        self.per_page = default_per_page

        self.filtered_items: list[Any] = []
        self.page_items: list[Any] = []

        self.total_items = 0
        self.total_pages = 1
        self.has_previous = False
        self.has_next = False

    def from_request(self):
        """Read query, page, and page size from request args."""

        self.query = request.args.get("q", "").strip()

        self.page = self._safe_int(
            request.args.get("page"),
            default=1,
        )

        self.per_page = self._safe_int(
            request.args.get("page_size"),
            default=self.default_per_page,
        )

        if self.per_page not in self.per_page_options:
            self.per_page = self.default_per_page

        self.filtered_items = self._search_items()
        self.total_items = len(self.filtered_items)

        self.total_pages = max(1, ceil(self.total_items / self.per_page))
        self.page = max(1, min(self.page, self.total_pages))

        start = (self.page - 1) * self.per_page
        end = start + self.per_page

        self.page_items = self.filtered_items[start:end]

        self.has_previous = self.page > 1
        self.has_next = self.page < self.total_pages

        return self

    def render(self):
        """Render the complete list widget."""

        return Markup(
            render_template(
                "snake_lists/list.html",
                list=self,
            )
        )

    def render_body(self):
        """Render only the AJAX-refreshable body."""

        return Markup(
            render_template(
                "snake_lists/_body.html",
                list=self,
            )
        )

    def previous_page(self) -> int:
        return max(1, self.page - 1)

    def next_page(self) -> int:
        return min(self.total_pages, self.page + 1)

    def _search_items(self) -> list[Any]:
        if not self.query:
            return self.items

        results: list[tuple[int, Any]] = []

        for item in self.items:
            haystack = self._item_haystack(item)
            score = self._score(self.query, haystack)

            if score >= self.fuzz_threshold:
                results.append((score, item))

        results.sort(key=lambda row: row[0], reverse=True)

        return [item for score, item in results]

    def _item_haystack(self, item: Any) -> str:
        values = []

        for field in self.search_fields:
            value = self._get_value(item, field)

            if value is not None:
                values.append(str(value))

        return " ".join(values)

    def _get_value(self, item: Any, field: str) -> Any:
        if isinstance(item, dict):
            return item.get(field, "")

        return getattr(item, field, "")

    def _normalize(self, value: str) -> str:
        """Normalize text for case-insensitive comparisons."""
        return value.casefold()

    def _score(self, query: str, haystack: str) -> int:
        """Return a match score between the query and haystack."""

        if not haystack:
            return 0

        query = self._normalize(query)
        haystack = self._normalize(haystack)

        if fuzz is not None:
            return max(
                fuzz.WRatio(query, haystack),
                fuzz.partial_ratio(query, haystack),
                fuzz.token_set_ratio(query, haystack),
            )

        if query in haystack:
            return 100

        return 0

    def _safe_int(self, value: str | None, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default
