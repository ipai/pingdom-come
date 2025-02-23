import asyncio
import logging

from waitress import serve
from waitress.adjustments import Adjustments

from src.api.app import create_app
from src.core.database import init_db


def configure_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def get_server_config() -> dict:
    """Get Waitress server configuration."""
    return {
        "host": "0.0.0.0",
        "port": 5000,
        "threads": 4,
        "log_socket_errors": True,
        # Increase max request header size to 512KB
        "max_request_header_size": 524288,
        # Set reasonable request body size limit (100MB)
        "max_request_body_size": 104857600,
    }


async def init():
    """Initialize the application."""
    await init_db()


if __name__ == "__main__":
    configure_logging()
    logger = logging.getLogger(__name__)

    # Initialize the database
    logger.info("Initializing database...")
    asyncio.run(init())

    logger.info("Initializing Flask application...")
    app = create_app()

    config = get_server_config()
    logger.info(f"Starting Waitress server on {config['host']}:{config['port']}")
    serve(app, **config)
