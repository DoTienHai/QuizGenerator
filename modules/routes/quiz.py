from flask import Blueprint, jsonify

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api')

@quiz_bp.route('/quizzes', methods=['POST'])
def upload_quiz():
    """Upload Excel file with questions (create quiz)"""
    return jsonify({'message': 'Upload quiz endpoint'}), 201

@quiz_bp.route('/quizzes', methods=['GET'])
def list_quizzes():
    """Get list of all quizzes"""
    return jsonify({'message': 'List quizzes endpoint'}), 200

@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get quiz by ID"""
    return jsonify({'message': f'Get quiz {quiz_id} endpoint'}), 200

@quiz_bp.route('/quizzes/<int:quiz_id>/results', methods=['GET'])
def get_quiz_results(quiz_id):
    """Get all results for a quiz"""
    return jsonify({'message': f'Get results for quiz {quiz_id} endpoint'}), 200

@quiz_bp.route('/quizzes/<int:quiz_id>/statistics', methods=['GET'])
def get_quiz_statistics(quiz_id):
    """Get statistics for a quiz"""
    return jsonify({'message': f'Get statistics for quiz {quiz_id} endpoint'}), 200
