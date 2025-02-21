import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()

def register_blueprints(app):
    """Register all blueprints for the application"""
    from flask_app.routes import api_bp
    
    app.register_blueprint(api_bp)  # API routes under /api/v1/
    
    logger.info(f'Registered blueprints: {[bp.name for bp in app.blueprints.values()]}')

def create_app(config=None):
    """Application factory function"""
    # Log the module name and root path
    logger.info(f'Creating Flask app with module name: {__name__}')
    
    app = Flask(__name__)
    
    # Default configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or (
        'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            db=os.getenv('DB_NAME', 'flask_app')
        )
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Override with any provided config
    if config:
        app.config.update(config)
    
    logger.info(f'App root path: {app.root_path}')
    logger.info(f'Static folder: {app.static_folder}')
    logger.info(f'Template folder: {app.template_folder}')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    register_blueprints(app)
    
    return app
