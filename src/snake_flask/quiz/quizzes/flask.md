# Flask Basics

---

## Question

What does `@app.route("/")` do?

### Choices

- Defines a URL route
- Creates a database table
- Starts the Flask server
- Installs Flask

### Answer

Defines a URL route

### Explanation

`@app.route("/")` tells Flask which function should run when the user visits `/`.

Excellent.

---

## Question

Which function renders an HTML template?

### Choices

- redirect()
- url_for()
- render_template()
- jsonify()

### Answer

render_template()

### Explanation

`render_template()` loads an HTML file from the `templates/` directory and returns it as a response.
