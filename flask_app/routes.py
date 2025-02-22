"""API routes for the Pingdom Come service."""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from flask_apispec import FlaskApiSpec, doc, marshal_with, use_kwargs
from marshmallow import ValidationError

from .schemas import (
    DataRequestSchema,
    DataResponseSchema,
    EchoSchema,
    EndpointSchema,
    ErrorSchema,
    StatusSchema,
)

# Create API blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/", methods=["GET"])
@doc(tags=["API"], description="List all available API endpoints")
@marshal_with(EndpointSchema)
def api_root():
    """List all available API endpoints.

    Returns:
        dict: A dictionary containing all available endpoints and their descriptions.
    """
    return {
        "available_endpoints": {
            "status": "/api/v1/status - Get API status",
            "echo": "/api/v1/echo/<message> - Echo a message",
            "data": "/api/v1/data - POST endpoint for JSON data",
        }
    }


@api_bp.route("/status", methods=["GET"])
@doc(tags=["API"], description="Get current API status")
@marshal_with(StatusSchema)
def get_status():
    """Get current API health status.

    Returns:
        dict: Current API status and timestamp.
    """
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}


@api_bp.route("/echo/<message>", methods=["GET"])
@doc(
    tags=["API"],
    description="Echo back a message",
    params={"message": {"description": "Message to echo back", "type": "string"}},
)
@marshal_with(EchoSchema)
def echo_message(message):
    """Echo back a message with timestamp.

    Args:
        message (str): Message to echo back.

    Returns:
        dict: Echo response containing the message and timestamp.
    """
    return {"message": message, "received_at": datetime.now(timezone.utc)}


@api_bp.route("/data", methods=["POST"])
@doc(tags=["API"], description="Process JSON data")
@use_kwargs(DataRequestSchema, location="json")
@marshal_with(DataResponseSchema)
def receive_data():
    """Process incoming JSON data.

    Returns:
        dict: Processed data response.

    Raises:
        ValidationError: If the request data is invalid.
    """
    try:
        request_data = request.get_json()
        return {"received_data": request_data["data"], "status": "success"}
    except ValidationError:
        return {"error": "Invalid request data", "status_code": 400}, 400


@api_bp.errorhandler(404)
@marshal_with(ErrorSchema)
def handle_404(error):
    """Handle 404 Not Found errors.

    Args:
        error: The error that triggered this handler.

    Returns:
        tuple: Error response and 404 status code.
    """
    return {"error": "Resource not found", "status_code": 404}, 404


def register_api_docs(docs: FlaskApiSpec) -> None:
    """Register API documentation for all routes.

    Args:
        docs: FlaskApiSpec instance to register routes with.
    """
    docs.register(api_root, blueprint="api")
    docs.register(get_status, blueprint="api")
    docs.register(echo_message, blueprint="api")
    docs.register(receive_data, blueprint="api")
