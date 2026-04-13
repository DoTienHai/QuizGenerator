"""
Result Routes: Exam results and scoring
Integrated with ScoringEngine
"""

from flask import Blueprint, jsonify
from ..services import ScoringEngine
from ..models import ExamResult, Quiz, ExamSession, db

result_bp = Blueprint('result', __name__, url_prefix='/api')


@result_bp.route('/results', methods=['GET'])
def list_results():
    """
    List all completed exams with scores
    Returns summary of all exam results including parameters for retake
    """
    try:
        # Query all exam results with their related quiz and session info
        results = db.session.query(ExamResult, Quiz, ExamSession).join(
            Quiz, ExamResult.quiz_id == Quiz.quiz_id
        ).join(
            ExamSession, ExamResult.session_id == ExamSession.session_id
        ).order_by(ExamResult.submitted_at.desc()).all()
        
        exam_list = []
        for exam_result, quiz, session in results:
            exam_list.append({
                'session_id': exam_result.session_id,
                'quiz_id': exam_result.quiz_id,
                'quiz_name': quiz.name,
                'score': exam_result.score,
                'correct_count': exam_result.correct_count,
                'incorrect_count': exam_result.incorrect_count,
                'skipped_count': exam_result.skipped_count,
                'status': exam_result.status,
                'submitted_at': exam_result.submitted_at.isoformat(),
                'time_spent_seconds': exam_result.time_spent_seconds,
                'num_questions': session.num_questions,
                'exam_duration': session.exam_duration
            })
        
        return jsonify({
            'success': True,
            'data': exam_list,
            'message': 'Loaded completed exams'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error loading exam results: {str(e)}'}), 500


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
