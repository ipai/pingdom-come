from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from flask_apispec import doc, marshal_with, use_kwargs
from marshmallow import ValidationError

from .schemas import (
    DataRequestSchema, DataResponseSchema, EchoSchema,
    EndpointSchema, ErrorSchema, StatusSchema
)

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/', methods=['GET'])
@doc(tags=['API'], description='List all available API endpoints')
@marshal_with(EndpointSchema)
def api_root():
    """List all available API endpoints."""
    endpoints = {
        'available_endpoints': {
            'status': '/api/v1/status - Get API status',
            'echo': '/api/v1/echo/<message> - Echo a message',
            'data': '/api/v1/data - POST endpoint for JSON data'
        }
    }
    return jsonify(EndpointSchema().dump(endpoints))

@api_bp.route('/status', methods=['GET'])
@doc(tags=['API'], description='Get current API status')
@marshal_with(StatusSchema)
def get_status():
    """Get current API status."""
    return jsonify(StatusSchema().dump({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc)
    }))

@api_bp.route('/echo/<message>', methods=['GET'])
@doc(tags=['API'],
     description='Echo back a message',
     params={'message': {'description': 'Message to echo back', 'type': 'string'}})
@marshal_with(EchoSchema)
def echo_message(message):
    """Echo back a message."""
    return jsonify(EchoSchema().dump({
        'message': message,
        'received_at': datetime.now(timezone.utc)
    }))

@api_bp.route('/data', methods=['POST'])
@doc(tags=['API'], description='Process JSON data')
@use_kwargs(DataRequestSchema, location='json')
@marshal_with(DataResponseSchema)
def receive_data():
    """Process JSON data."""
    try:
        request_data = DataRequestSchema().load(request.get_json())
        return jsonify(DataResponseSchema().dump({
            'received_data': request_data['data'],
            'status': 'success'
        }))
    except ValidationError:
        return jsonify(ErrorSchema().dump({
            'error': 'Invalid request data',
            'status_code': 400
        })), 400

@api_bp.errorhandler(404)
def handle_404(error):
    """Handle 404 Not Found errors."""
    return jsonify(ErrorSchema().dump({
        'error': 'Resource not found',
        'status_code': 404
    })), 404
