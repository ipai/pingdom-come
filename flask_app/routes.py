from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from marshmallow import ValidationError
from .schemas import *

# Create a blueprint with a url_prefix
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Root route to show available endpoints
@api_bp.route('/', methods=['GET'])
def api_root():
    endpoints = {
        'available_endpoints': {
            'status': '/api/v1/status - Get API status',
            'echo': '/api/v1/echo/<message> - Echo back a message',
            'data': '/api/v1/data - POST endpoint for JSON data'
        }
    }
    return jsonify(EndpointSchema().dump(endpoints))

# Example route using GET method
@api_bp.route('/status', methods=['GET'])
def get_status():
    status_data = {
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc)
    }
    return jsonify(StatusSchema().dump(status_data))

# Example route with parameters
@api_bp.route('/echo/<message>', methods=['GET'])
def echo_message(message):
    message_data = {
        'message': message,
        'received_at': datetime.now(timezone.utc)
    }
    return jsonify(EchoSchema().dump(message_data))

# Example route using POST method with JSON data
@api_bp.route('/data', methods=['POST'])
def receive_data():
    try:
        # Validate request data
        request_data = DataRequestSchema().load(request.get_json())
        
        # Prepare and validate response
        response_data = {
            'received_data': request_data['data'],
            'status': 'success'
        }
        return jsonify(DataResponseSchema().dump(response_data))
    except ValidationError as err:
        error_response = {
            'error': 'Invalid request data',
            'status_code': 400
        }
        return jsonify(ErrorSchema().dump(error_response)), 400

# Example error handler for this blueprint
@api_bp.errorhandler(404)
def handle_404(error):
    error_data = {
        'error': 'Resource not found',
        'status_code': 404
    }
    return jsonify(ErrorSchema().dump(error_data)), 404
