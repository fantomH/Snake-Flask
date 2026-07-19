# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/common/blueprints/config.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-15 11:28:14 UTC
# Updated     : 2026-07-15 11:28:14 UTC
# Description : Configuration routes.
# +---------------------------------------------------------------------------+

from __future__ import annotations

from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from snake_flask.access.authentication_manager import login_required
from snake_flask.linguae import get_language_dictionary

bp = Blueprint(
    "app-config",
    __name__,
    template_folder="../templates",
)

@bp.route("/app-config/")
@login_required
def configuration():
    """
    List app configuration.
    """

    # display_language = get_language_dictionary()

    cfg = dict(sorted(current_app.config.items()))

    return render_template(
        "snake_common/app-configuration.html",
        cfg=cfg,
    )
