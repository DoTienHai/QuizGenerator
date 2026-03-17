"""
Result Routes: Exam results and scoring
Integrated with ScoringEngine
"""

from flask import Blueprint, jsonify
from ..services import ScoringEngine

result_bp = Blueprint('result', __name__, url_prefix='/api')


@result_bp.route('/results/<session_id>', methods=['GET'])
def get_results(session_id):
    """
    Get exam results for a session
    Returns detailed score breakdown with question-by-question analysis
    """
    try:
        result = ScoringEngine.get_result_details(session_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting results: {str(e)}'}), 500


@result_bp.route('/results/<session_id>/score', methods=['GET'])
def get_score(session_id):
    """Get calculated score and grade for a session"""
    try:
        result = ScoringEngine.calculate_score(session_id)
        
        if result['success']:
            score_data = result['data']
            return jsonify({
                'success': True,
                'data': {
                    'session_id': session_id,
                    'score': score_data['score'],
                    'grade': score_data['grade'],
                    'correct_count': score_data['correct_count'],
                    'incorrect_count': score_data['incorrect_count'],
                    'skipped_count': score_data['skipped_count'],
                    'total_questions': score_data['total_questions'],
                    'pass': score_data['pass']
                },
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error calculating score: {str(e)}'}), 500


@result_bp.route('/results/<session_id>/analysis', methods=['GET'])
def get_result_analysis(session_id):
    """Get detailed analysis by difficulty level"""
    try:
        result = ScoringEngine.get_statistics_by_difficulty(session_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting analysis: {str(e)}'}), 500
