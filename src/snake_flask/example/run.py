# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/example/run.py]                              |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-05-19 11:33:46 UTC                                     |
# | Updated     : 2026-06-30 11:20:17 UTC                                     |
# | Description : Snake-Example run.                                          |
# +---------------------------------------------------------------------------+

from app import create_app

app = create_app(
    {"SECRET_KEY": "test-secret"}
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8069, debug=True)
