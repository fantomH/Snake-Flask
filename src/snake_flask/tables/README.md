<!--
+---------------------------------------------------------------------- INFO -+
| [Snake-Flask/src/snake_flask/tables/README.md]                              |
|                                                                             |
| Author      : Pascal Malouin (https://github.com/fantomH)                   |
| Created     : 2026-06-03 19:23:14 UTC                                       |
| Updated     : 2026-06-24 15:31:07 UTC                                       |
| Description : SnakeTables README.                                           |
+-----------------------------------------------------------------------------+
-->

# snake_flask.tables

`snake_flask.tables is a lightweight Flask extension that provides simple tables construction from SQLite tables.

---

## API

Extension name: `snake_tables`.

| | Description | |
| :- | :- | :- |
| `SnakeTables` | extension *class* responsible for managing tables. |
| `Table` | *class* responsible to build tables. |

---

## Quick Start

### Application Setup

```python
from flask import Flask
from snake_flask.tables import SnakeTables

app = Flask(__name__)

SnakeTables(app)
```

---

## Building a table with `Table`

- Source of data.
- Columns definition.
- Building required routes.
- Build template.

We suggest to create a function that returns a Table object.

```python
from snake_flask.tables import Table
# import db as well here

def get_some_table():

    _columns = [...]

    return Table(
        table_id=< table ID >,
        data_url=< data URL >,
        data_update_url=< data update URL >,
        db = < database URI >,
        source_table=< database table name >,
        columns=_columns,
        default_order_by=< column name to sort and sort method >,
    )
```

The variable `table_id` can be anything, but we suggest to use an intelligible naming convention like "user-table".

### Source of data

As of now, SnakeTables supports SQLite database only.

`db` is the database URI and `source_table` is the database table name.

### Columns definition

The columns definition is a list of dictionaries.

#### Columns keys

Multiples keys must be defined in order to create the columns.

- name
- label
- type
- text
- url
- db
- sortable
- searchable

##### `name`

The class `Table` uses this variable to two purposes.

1. As an ID, in the table template.
2. To query the database. In this case, it must be equivalent to the database column name.

##### `label`

The display name of the column header.

##### `type`

SnakeTables supports different types of columns.

__checkbox__: Displays a checkbox for boolean value. Updates the database with a POST to the `data_update_url`. Thus, this must be a value from the database.
__link-button__: Displays buttons opening a hyperlink when clicked (requires `text` and `url` to be set).

If type is omitted, simple text will be displayed.

##### `text`

Text used for the button for the `link-button` type.

##### `url`

URL used for the `link-button` type.

##### `db`

By default, the value of `db` is set to True. This indicates to `Table` to query the database.
If the data of a column is not from the database, you must set it to False (for example, when using the type `link-button`).

##### `sortable`

Set to True to allow the column to be sortable.

##### `searchable`

Set to True to allow the column to be searchable.

### Building required routes

SnakeTables uses a route to display the table, a route to post the data and, if needed, a route to update the table "live".

#### Table display

This route is required to display the table.

```python
from flask import render_template

@app.route("/table-display/")
def table_display():

    return render_template(
        "some_table.html",
        some_table=get_some_table(),
        )
```

#### Data

This will be the route used to fecth the data.

```python
from flask import jsonify

@app.route("/table_display/data/")
def table_data()

    return jsonify(
        get_some_table.get_data()
    )
```

#### Live update of a table

```python
from flask import request, jsonify
from .models import User

@app.route("/display_table/update/", methods=["POST"])
def update_table():

    data = request.get_json()

    # Change to fit your db update routine.
    User.update_user(
        data.get("id"),
        **{
            data.get("column"): data.get("value")
        }
    )

    return jsonify({
        "ok": True,
    })
```

---

## Display language

SnakeTables relies on SnakeLinguae for messages and basic navigation button.

By default, SnakeTables uses an English dictionary. French is also supported.

Add the following SnakeLinguae configuration to your app if you wish to use another language.

```python
app.config["DEFAULT_LANGUAGE"] = "french"
```
