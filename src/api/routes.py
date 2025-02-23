import logging
from datetime import datetime, timedelta
from typing import Any, Dict

from flask import Flask, jsonify, request

from .temporal import create_temporal_client
from ..temporal.workflows import AnalyticsCollectionWorkflow

logger = logging.getLogger(__name__)


def register_routes(app: Flask) -> None:
    """Register all application routes."""

    @app.route("/")
    def index() -> Dict[str, Any]:
        """Root endpoint that lists available API endpoints."""
        return jsonify(
            {
                "status": "ok",
                "message": "Pingdom API is running",
                "endpoints": {
                    "GET /api/reports/last-24h": "Get analytics report for last 24 hours",
                    "GET /api/reports/last-7d": "Get analytics report for last 7 days",
                    "POST /api/config/schedule": "Configure report generation schedule",
                },
            }
        )

    @app.route("/api/reports/last-24h", methods=["GET"])
    async def get_last_24h_report() -> Dict[str, str]:
        """Generate a report for the last 24 hours."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)

        logger.info(f"Generating 24h report from {start_date} to {end_date}")

        # Start workflow
        client = await create_temporal_client()
        handle = await client.start_workflow(
            AnalyticsCollectionWorkflow.run,
            start_date.isoformat(),  # Convert datetime to ISO format string
            id=f"analytics-24h-{end_date.isoformat()}",
            task_queue="analytics-queue",
        )

        # Wait for result
        await handle.result()
        return jsonify({"status": "success", "message": "Report generated"})

    @app.route("/api/reports/last-7d", methods=["GET"])
    async def get_last_7d_report() -> Dict[str, str]:
        """Generate a report for the last 7 days."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        logger.info(f"Generating 7d report from {start_date} to {end_date}")

        # Start workflow
        client = await create_temporal_client()
        handle = await client.start_workflow(
            AnalyticsCollectionWorkflow.run,
            start_date,
            id=f"analytics-7d-{end_date.isoformat()}",
            task_queue="analytics-queue",
        )

        # Wait for result
        await handle.result()
        return jsonify({"status": "success", "message": "Report generated"})

    @app.route("/api/config/schedule", methods=["POST"])
    async def configure_schedule() -> Dict[str, str]:
        """Configure the schedule for report generation.

        Expected request body:
        {
            "daily_report": {
                "enabled": true,
                "time": "00:00"
            },
            "weekly_report": {
                "enabled": true,
                "day": "monday",
                "time": "00:00"
            }
        }
        """
        data = request.get_json()
        logger.info(f"Configuring schedule with data: {data}")

        # TODO: Implement schedule configuration using Temporal Schedules
        return jsonify({"status": "success", "message": "Schedule updated"})
