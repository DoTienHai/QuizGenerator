from flask import Blueprint, jsonify

result_bp = Blueprint('result', __name__, url_prefix='/api')

@result_bp.route('/results/<session_id>', methods=['GET'])
def get_results(session_id):
    """Get exam results"""
    return jsonify({'message': f'Get results for session {session_id} endpoint'}), 200
