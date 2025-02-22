"""Core application configuration and initialization."""

import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from dotenv import load_dotenv
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_app.routes import api_bp, register_api_docs

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()

# Load environment variables from .env file
load_dotenv()


def create_app(config=None):
    """Create and configure the Flask application.

    Args:
        config (dict, optional): Override default configuration.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") or (
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'flask_app')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Configure API documentation
    app.config.update(
        {
            "APISPEC_SPEC": APISpec(
                title="Pingdom Come API",
                version="v1",
                openapi_version="2.0",
                plugins=[FlaskPlugin(), MarshmallowPlugin()],
            ),
            "APISPEC_SWAGGER_URL": "/swagger/",
            "APISPEC_SWAGGER_UI_URL": "/",
        }
    )

    # Override with any provided config
    if config:
        app.config.update(config)

    # Initialize core extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure and enable CORS before registering any routes
    allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
    domain_patterns = os.getenv('ALLOWED_DOMAIN_PATTERNS', '.vercel.app').split(',')
    
    CORS(app, resources={
        r"/api/v1/*": {
            "origins": [*allowed_origins,  # Exact matches
                      # Add pattern-based origins (all subdomains)
                      *[f'https://*.{pattern.lstrip(".*")}'
                        for pattern in domain_patterns if pattern]],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Register routes and documentation after CORS is configured
    app.register_blueprint(api_bp)
    docs = FlaskApiSpec(app)
    
    with app.test_request_context():
        register_api_docs(docs)

    return app
