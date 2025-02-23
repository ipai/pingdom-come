import asyncio
import logging
import os
import time

from temporalio.client import Client
from temporalio.worker import Worker

from .workflows import (
    AnalyticsCollectionWorkflow,
    fetch_cloudflare_analytics,
    generate_report,
    store_analytics_data,
)


def configure_logging():
    """Configure logging for the worker."""
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure all loggers to use our format
    for name in logging.root.manager.loggerDict:
        logger = logging.getLogger(name)
        logger.handlers = []
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(handler)
        logger.propagate = False  # Prevent duplicate logs


async def run_worker():
    """Run the Temporal worker with retry logic."""
    max_retries = 5
    retry_delay = 5  # seconds
    attempt = 0
    logger = logging.getLogger(__name__)

    while attempt < max_retries:
        try:
            # Connect to temporal server
            logger.info(f"Attempting to connect to Temporal server (attempt {attempt + 1}/{max_retries})")
            client = await Client.connect(os.getenv("TEMPORAL_HOST", "localhost:7233"))
            logger.info("Successfully connected to Temporal server")

            # Run the worker
            worker = Worker(
                client,
                task_queue="analytics-queue",
                workflows=[AnalyticsCollectionWorkflow],
                activities=[
                    fetch_cloudflare_analytics,
                    store_analytics_data,
                    generate_report,
                ],
            )

            logger.info("Starting worker...")
            await worker.run()
            return  # If we get here, everything worked

        except Exception as e:
            attempt += 1
            if attempt >= max_retries:
                logger.error(f"Failed to connect after {max_retries} attempts. Last error: {e}")
                raise
            logger.warning(f"Connection attempt {attempt} failed: {e}. Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)


def main():
    """Main entry point for the worker."""
    configure_logging()
    while True:
        try:
            asyncio.run(run_worker())
            break  # If run_worker() completes successfully, exit the loop
        except Exception as e:
            logging.error(f"Worker failed: {e}")
            logging.info("Restarting worker in 5 seconds...")
            time.sleep(5)  # Use time.sleep since we're in synchronous context


if __name__ == "__main__":
    main()
