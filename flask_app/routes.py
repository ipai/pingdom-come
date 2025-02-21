from flask import Blueprint, jsonify, request
from datetime import datetime

# Create a blueprint with a url_prefix
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Root route to show available endpoints
@api_bp.route('/', methods=['GET'])
def api_root():
    return jsonify({
        'available_endpoints': {
            'status': '/api/v1/status - Get API status',
            'echo': '/api/v1/echo/<message> - Echo back a message',
            'data': '/api/v1/data - POST endpoint for JSON data'
        }
    })

# Example route using GET method
@api_bp.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

# Example route with parameters
@api_bp.route('/echo/<message>', methods=['GET'])
def echo_message(message):
    return jsonify({
        'message': message,
        'received_at': datetime.utcnow().isoformat()
    })

# Example route using POST method with JSON data
@api_bp.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    return jsonify({
        'received_data': data,
        'status': 'success'
    })

# Example error handler for this blueprint
@api_bp.errorhandler(404)
def handle_404(error):
    return jsonify({
        'error': 'Resource not found',
        'status_code': 404
    }), 404
