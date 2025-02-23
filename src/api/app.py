import logging

from flask import Flask
from flask_cors import CORS

from .routes import register_routes

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Create and configure the Flask application."""
    logger.info("Initializing Flask application...")
    app = Flask(__name__)

    # Configure CORS and other middleware
    CORS(app)

    # Register routes
    register_routes(app)

    logger.info("Flask application initialized successfully")
    return app
