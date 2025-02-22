"""Flask application entry point."""

from flask_app.core import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
