from flask import Flask
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def register_blueprints(app):
    """Register all blueprints for the application"""
    from flask_app.routes import api_bp
    
    app.register_blueprint(api_bp)  # API routes under /api/v1/
    
    logger.info(f'Registered blueprints: {[bp.name for bp in app.blueprints.values()]}')

def create_app():
    """Application factory function"""
    # Log the module name and root path
    logger.info(f'Creating Flask app with module name: {__name__}')
    
    app = Flask(__name__)
    logger.info(f'App root path: {app.root_path}')
    logger.info(f'Static folder: {app.static_folder}')
    logger.info(f'Template folder: {app.template_folder}')
    
    # Register blueprints
    register_blueprints(app)
    
    return app
