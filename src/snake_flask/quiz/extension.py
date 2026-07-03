# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/quiz/extension.py]                           |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-02 18:51:23 UTC                                     |
# | Updated     : 2026-06-22 20:14:14 UTC                                     |
# | Description : SnakeQuiz extension.                                        |
# +---------------------------------------------------------------------------+

from importlib.resources import files
from markdown import markdown
from pathlib import Path
import shutil

from snake_flask.common import ensure_snake_common
from snake_flask.linguae import ensure_linguae

from .blueprints import bp

class SnakeQuiz:

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions["snake_quiz"] = self

        # [*] SnakeLinguae initiation.
        linguae = ensure_linguae(app)
        linguae.register_package("snake_flask.quiz.dictionaries")

        # [*] SnakeCommon.
        ensure_snake_common(app)

        app.config.setdefault(
            "SNAKE_QUIZ_DIR",
            str(Path(app.instance_path) / "snake_quiz" / "quizzes"),
        )

        app.config.setdefault(
            "SNAKE_QUIZ_BASE_TEMPLATE",
            None,
        )

        # [*] Copy quizzes' examples.
        quizzes_dir = Path(app.config["SNAKE_QUIZ_DIR"])

        if not quizzes_dir.exists():
            quizzes_dir.mkdir(parents=True)

            self.install_examples(quizzes_dir)

        @app.template_filter("markdown")
        def markdown_filter(text):
            return markdown(
                text or "",
                extensions=["fenced_code", "tables"],
            )

        @app.context_processor
        def inject_base_template():
            _base_template = app.config[
                "SNAKE_QUIZ_BASE_TEMPLATE"
            ]

            if _base_template is None:
                _internal_base_template = (
                    "snake_quiz/base_standalone.html"
                )
            else:
                _internal_base_template = (
                    "snake_quiz/base_extension.html"
                )

            return {
                "_internal_base_template": _internal_base_template,
                "_base_template": _base_template,
            }

        app.register_blueprint(bp)

    def install_examples(self, quizzes_dir):

        examples = files("snake_flask.quiz.quizzes")

        for example in examples.iterdir():
            shutil.copy(example, quizzes_dir)
