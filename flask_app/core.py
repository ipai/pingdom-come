import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from dotenv import load_dotenv
from flask import Blueprint, Flask
from flask_apispec import FlaskApiSpec
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_app.routes import api_bp, api_root, get_status, echo_message, receive_data

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
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or (
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'flask_app')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure API documentation
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Pingdom Come API',
            version='v1',
            openapi_version='2.0',
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
        'APISPEC_ENABLE_SWAGGER_UI': True,
    })
    
    # Override with any provided config
    if config:
        app.config.update(config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Initialize API documentation
    docs = FlaskApiSpec(app)
    
    # Register API routes with documentation
    with app.test_request_context():
        docs.register(api_root, blueprint='api')
        docs.register(get_status, blueprint='api')
        docs.register(echo_message, blueprint='api')
        docs.register(receive_data, blueprint='api')
    
    return app
