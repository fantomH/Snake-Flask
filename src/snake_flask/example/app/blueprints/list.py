# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/example/app/blueprints/list.py]              |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-07-02 15:31:19 UTC                                     |
# | Updated     : 2026-07-02 15:31:19 UTC                                     |
# | Description : List example.                                               |
# +---------------------------------------------------------------------------+

from pathlib import Path

from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import url_for

from snake_flask.lists import List
from snake_vault.converter import toml_to_list

bp = Blueprint("list", __name__)

def get_bookmarks():

    return toml_to_list(
        Path(current_app.instance_path) / "data" / "bookmarks.toml",
        "bookmark"
    )

def get_bookmark_list():
    return List(
        name="bookmarks",
        items=get_bookmarks(),
        search_fields=[
            "name",
            "url",
            "description",
            "tags",
        ],
        card_template="lists/_bk_card.html",
        data_url=url_for("list.list_data"),
        default_per_page=25,
        fuzz_threshold=60,
    ).from_request()


@bp.route("/lists/")
def list_example():
    b_list = get_bookmark_list()

    return render_template(
        "lists/list.html",
        b_list=b_list,
    )


@bp.route("/lists/data/")
def list_data():
    b_list = get_bookmark_list()

    return b_list.render_body()
