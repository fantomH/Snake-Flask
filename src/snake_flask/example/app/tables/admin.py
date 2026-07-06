# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/example/app/tables/admin.py]                 |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-05-24 16:34:45 UTC                                     |
# | Updated     : 2026-07-01 17:37:47 UTC                                     |
# | Description : Table definitions.                                          |
# +---------------------------------------------------------------------------+

from flask import current_app

from snake_flask.database import get_db
from snake_flask.linguae import get_language_dictionary
from snake_flask.tables import Table

def get_users_table():

    # +- [ COLUMNS DICTIONARY ] ----------------------------------------------+
    # |                                                                       |
    # | Custom dictionary for Users table columns.                            |
    # +-----------------------------------------------------------------------+
    columns_lang_display = {
        "english": {
            "column-edit-text": "Modify",
            "column-username-label": "Username",
            "column-is_active-label": "Active",
            "column-mfa_enabled-label": "MFA Enabled",
        },
        "french": {
            "column-edit-text": "Modifier",
            "column-username-label": "Utilisateurs",
            "column-is_active-label": "Actif",
            "column-mfa_enabled-label": "MFA activé",
        }
    }

    display_language = get_language_dictionary(custom=columns_lang_display)

    # +- [ COLUMNS DEFINITION ] ----------------------------------------------+
    # |                                                                       |
    # | Using Snake-Tables.                                                   |
    # +-----------------------------------------------------------------------+
    ADMIN_USERS_TABLE = [
        {
            "name": "username",
            "label": display_language.get("column-username-label", "Username"),
            "sortable": True,
            "searchable": True
        },
        {
            "name": "email",
            "label": "Email",
            "sortable": True,
            "searchable": True
        },
        {
            "name": "is_active",
            "label": display_language.get("column-is_active-label", "Active"),
            "type": "checkbox",
            "sortable": True
        },

        {
            "name": "mfa_enabled",
            "label": display_language.get("column-mfa_enabled-label", "MFA Enabled"),
            "type": "checkbox",
            "sortable": True
        },
        {
            "name": "edit",
            "label": "",
            "type": "link-button",
            "text": display_language.get("column-edit-text", "Modify"),
            "url": "/admin/users/account/{username}/",
            "db": False,
        },
    ]

    return Table(
        table_id="users-table",
        data_url="/admin/users/data/",
        data_update_url="/admin/users/update/",
        db = get_db(),
        source_table="users",
        columns=ADMIN_USERS_TABLE,
        default_order_by="username ASC",
    )
