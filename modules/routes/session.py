"""
Session Routes: Exam session management
Integrated with ExamService
"""

from flask import Blueprint, jsonify, request
from ..services import ExamService, ValidationService

session_bp = Blueprint('session', __name__, url_prefix='/api')


@session_bp.route('/sessions', methods=['POST'])
def create_session():
    """
    Create new exam session
    Expected JSON:
        - quiz_id: ID of quiz to use
        - num_questions (optional): Number of random questions
        - duration_minutes (optional): Duration in minutes (default: 30)
    """
    try:
        data = request.get_json()
        
        if not data or 'quiz_id' not in data:
            return jsonify({'success': False, 'message': 'quiz_id is required'}), 400
        
        quiz_id = data['quiz_id']
        num_questions = data.get('num_questions', None)
        duration_minutes = data.get('duration_minutes', 30)
        
        result = ExamService.create_session(quiz_id, num_questions, duration_minutes)
        
        if result['success']:
            session = result['data']
            return jsonify({
                'success': True,
                'data': {
                    'session_id': session.session_id,
                    'quiz_id': session.quiz_id,
                    'num_questions': session.num_questions,
                    'exam_duration': session.exam_duration,
                    'expires_at': session.expires_at.isoformat(),
                    'status': session.status
                },
                'message': result['message']
            }), 201
        else:
            return jsonify({'success': False, 'message': result['message']}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error creating session: {str(e)}'}), 500


@session_bp.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get exam session details"""
    try:
        result = ExamService.get_session(session_id)
        
        if result['success']:
            session = result['data']
            return jsonify({
                'success': True,
                'data': {
                    'session_id': session.session_id,
                    'quiz_id': session.quiz_id,
                    'num_questions': session.num_questions,
                    'exam_duration': session.exam_duration,
                    'created_at': session.created_at.isoformat(),
                    'expires_at': session.expires_at.isoformat(),
                    'status': session.status
                },
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting session: {str(e)}'}), 500


@session_bp.route('/sessions/<session_id>/status', methods=['GET'])
def get_session_status(session_id):
    """Get current exam session status and remaining time"""
    try:
        result = ExamService.get_session_status(session_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting session status: {str(e)}'}), 500


@session_bp.route('/sessions/<session_id>/questions', methods=['GET'])
def get_session_questions(session_id):
    """Get all questions for a session (for exam display)"""
    try:
        result = ExamService.get_session_questions(session_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting questions: {str(e)}'}), 500


@session_bp.route('/sessions/<session_id>/answers', methods=['POST'])
def submit_answer(session_id):
    """
    Submit a single answer during exam
    Expected JSON:
        - question_id: ID of the question
        - user_answer: User's answer (A, B, C, D, or empty for skip)
    """
    try:
        data = request.get_json()
        
        if not data or 'question_id' not in data:
            return jsonify({'success': False, 'message': 'question_id is required'}), 400
        
        question_id = data['question_id']
        user_answer = data.get('user_answer', '')
        
        result = ExamService.submit_answer(session_id, question_id, user_answer)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error submitting answer: {str(e)}'}), 500


@session_bp.route('/sessions/<session_id>/submit', methods=['POST'])
def submit_exam(session_id):
    """Final exam submission and scoring"""
    try:
        result = ExamService.submit_exam(session_id)
        
        if result['success']:
            exam_result = result['data']
            return jsonify({
                'success': True,
                'data': {
                    'session_id': exam_result.session_id,
                    'score': exam_result.score,
                    'correct_count': exam_result.correct_count,
                    'incorrect_count': exam_result.incorrect_count,
                    'skipped_count': exam_result.skipped_count,
                    'status': exam_result.status,
                    'submitted_at': exam_result.submitted_at.isoformat()
                },
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error submitting exam: {str(e)}'}), 500


@session_bp.route('/sessions/<session_id>/auto-submit', methods=['POST'])
def auto_submit(session_id):
    """Auto-submit when time expires"""
    try:
        result = ExamService.auto_submit(session_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error auto-submitting: {str(e)}'}), 500
