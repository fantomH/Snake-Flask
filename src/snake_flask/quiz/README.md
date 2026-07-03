<!--
+---------------------------------------------------------------------- INFO -+
| [Snake-Flask/src/snake_flask/quiz/README.md]                                |
|                                                                             |
| Author      : Pascal Malouin (https://github.com/fantomH)                   |
| Created     : 2026-06-03 19:23:14 UTC                                       |
| Updated     : 2026-06-24 15:31:07 UTC                                       |
| Description : SnakeQuiz README.                                             |
+-----------------------------------------------------------------------------+
-->

# snake_flask.quiz

Snake-Quiz is a lightweight Flask extension that provides a multiple-choice quiz system based on Markdown files.

Questionnaires are stored as simple `.md` files, making it easy for non-developers to create and maintain quizzes without touching Python code.

---

## API

Extension name: `snake_quiz`.

| | Description | |
| :- | :- | :- |
| SnakeQuiz | extension *class* responsible for managing quizzes.  |

---

## Default Configuration

| Name | Description | Default |
| :--- | :---------- | :------ |
| `SNAKE_QUIZ_DIR` | Quizzes directory | `str(Path(app.instance_path) / "snake_quiz" / "quizzes")` |
| `SNAKE_QUIZ_BASE_TEMPLATE` | Name of template to extend for the content. | `None` |

### `SNAKE_QUIZ_BASE_TEMPLATE`

By default, SnakeQuiz will use it's own internal base template.

If, for example, you have your own base template in which you want to incorporate the quizzes, use this configuration.

```python
    app.config["SNAKE_QUIZ_BASE_TEMPLATE"] = "base.html"
```

---

## Quick Start

### Application Setup

```python
from flask import Flask
from snake_flask.quiz import SnakeQuiz

app = Flask(__name__)

SnakeQuiz(app)
```

The quiz blueprint will automatically be registered at:

```text
/quiz/
```

## Routes

### List Questionnaires

```text
GET /quiz/
```

Displays all available questionnaires.

---

### Take a Quiz

```text
GET /quiz/<quiz_name>/
```

Displays the selected questionnaire.

Example:

```text
/quiz/python-basics/
```

---

### Submit a Quiz

```text
POST /quiz/<quiz_name>/
```

Calculates:

* Total score
* Correct answers
* Incorrect answers
* Explanations

---

## Questionnaire Format

Questionnaires are written in Markdown.

Example:

```markdown
# Python Basics

---

## Question

What keyword defines a function in Python?

### Choices

- class
- function
- def
- lambda

### Answer

def

### Explanation

The `def` keyword is used to define a function.

---

## Question

What data type is returned by `len()`?

### Choices

- str
- bool
- int
- float

### Answer

int

### Explanation

The `len()` function returns an integer.
```

## Display language

Quizzes are always displayed in the language used in the markdown files.

That said, SnakeQuiz relies on SnakeLinguae for messages and basic navigation button.

By default, SnakeQuiz uses an English dictionary. French is also supported.

Add the following SnakeLinguae configuration to your app if you wish to use another language.

```python
app.config["DEFAULT_LANGUAGE"] = "french"
```
