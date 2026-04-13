"""
Exam Routes: Exam session management
Integrated with ExamService
"""

from flask import Blueprint, jsonify, request
from ..services import ExamService, ValidationService
from ..utils.error_codes import error_response, success_response, ERR_MISSING_PARAM, ERR_QUIZ_NOT_FOUND, ERR_SESSION_NOT_FOUND, ERR_SESSION_EXPIRED, ERR_INTERNAL, ERR_INVALID_ANSWER

exam_bp = Blueprint('exam', __name__, url_prefix='/api')


@exam_bp.route('/exams', methods=['POST'])
def create_exam():
    """
    Create new exam
    Expected JSON:
        - quiz_id: ID of quiz to use
        - num_questions (optional): Number of random questions
        - duration_minutes (optional): Duration in minutes (default: 30)
    """
    try:
        data = request.get_json()
        
        if not data or 'quiz_id' not in data:
            response, status = error_response(ERR_MISSING_PARAM, 'quiz_id is required', 400)
            return jsonify(response), status
        
        quiz_id = data['quiz_id']
        num_questions = data.get('num_questions', None)
        duration_minutes = data.get('duration_minutes', 30)
        
        result = ExamService.create_session(quiz_id, num_questions, duration_minutes)
        
        if result['success']:
            exam = result['data']
            response, status = success_response(
                data={
                    'session_id': exam.session_id,
                    'quiz_id': exam.quiz_id,
                    'num_questions': exam.num_questions,
                    'exam_duration': exam.exam_duration,
                    'expires_at': exam.expires_at.isoformat(),
                    'status': exam.status
                },
                message=result['message'],
                status_code=201
            )
            return jsonify(response), status
        else:
            response, status = error_response(ERR_QUIZ_NOT_FOUND, result['message'], 400)
            return jsonify(response), status
    
    except Exception as e:
        response, status = error_response(ERR_INTERNAL, f'Error creating exam: {str(e)}', 500)
        return jsonify(response), status


@exam_bp.route('/exams/<session_id>', methods=['GET'])
def get_exam(session_id):
    """Get exam details"""
    try:
        result = ExamService.get_session(session_id)
        
        if result['success']:
            exam = result['data']
            response, status = success_response(
                data={
                    'session_id': exam.session_id,
                    'quiz_id': exam.quiz_id,
                    'num_questions': exam.num_questions,
                    'exam_duration': exam.exam_duration,
                    'created_at': exam.created_at.isoformat(),
                    'expires_at': exam.expires_at.isoformat(),
                    'status': exam.status
                },
                message=result['message']
            )
            return jsonify(response), status
        else:
            response, status = error_response(ERR_SESSION_NOT_FOUND, result['message'], 404)
            return jsonify(response), status
    
    except Exception as e:
        response, status = error_response(ERR_INTERNAL, f'Error getting exam: {str(e)}', 500)
        return jsonify(response), status


@exam_bp.route('/exams/<session_id>/status', methods=['GET'])
def get_exam_status(session_id):
    """Get current exam status and remaining time"""
    try:
        result = ExamService.get_session_status(session_id)
        
        if result['success']:
            response, status = success_response(data=result['data'], message=result['message'])
            return jsonify(response), status
        else:
            response, status = error_response(ERR_SESSION_NOT_FOUND, result['message'], 404)
            return jsonify(response), status
    
    except Exception as e:
        response, status = error_response(ERR_INTERNAL, f'Error getting exam status: {str(e)}', 500)
        return jsonify(response), status


@exam_bp.route('/exams/<session_id>/questions', methods=['GET'])
def get_exam_questions(session_id):
    """Get all questions for exam"""
    try:
        result = ExamService.get_session_questions(session_id)
        
        if result['success']:
            response, status = success_response(data=result['data'], message=result['message'])
            return jsonify(response), status
        else:
            response, status = error_response(ERR_SESSION_NOT_FOUND, result['message'], 404)
            return jsonify(response), status
    
    except Exception as e:
        response, status = error_response(ERR_INTERNAL, f'Error getting exam questions: {str(e)}', 500)
        return jsonify(response), status


@exam_bp.route('/exams/<session_id>/answers', methods=['POST'])
def submit_answer(session_id):
    """
    Submit answer during exam
    Expected JSON:
        - question_id: ID of the question
        - user_answer: User's answer (A, B, C, D, or empty for skip)
    """
    try:
        data = request.get_json()
        
        if not data or 'question_id' not in data:
            response, status = error_response(ERR_MISSING_PARAM, 'question_id is required', 400)
            return jsonify(response), status
        
        question_id = data['question_id']
        user_answer = data.get('user_answer', '')
        
        result = ExamService.submit_answer(session_id, question_id, user_answer)
        
        if result['success']:
            response, status = success_response(message=result['message'])
            return jsonify(response), status
        else:
            response, status = error_response(ERR_INVALID_ANSWER, result['message'], 400)
            return jsonify(response), status
    
    except Exception as e:
        response, status = error_response(ERR_INTERNAL, f'Error submitting exam answer: {str(e)}', 500)
        return jsonify(response), status


@exam_bp.route('/exams/<session_id>/submit', methods=['POST'])
def submit_exam(session_id):
    """Submit exam (final submission)"""
    try:
        # Get answers from request body
        data = request.get_json()
        answers = data.get('answers', {}) if data else {}
        
        # Process answers and submit exam
        result = ExamService.submit_exam(session_id, answers)
        
        if result['success']:
            exam_result = result['data']
            response, status = success_response(
                data={
                    'session_id': exam_result.session_id,
                    'score': exam_result.score,
                    'correct_count': exam_result.correct_count,
                    'incorrect_count': exam_result.incorrect_count,
                    'skipped_count': exam_result.skipped_count,
                    'status': exam_result.status,
                    'submitted_at': exam_result.submitted_at.isoformat()
                },
                message=result['message']
            )
            return jsonify(response), status
        else:
            response, status = error_response(ERR_SESSION_EXPIRED, result['message'], 400)
            return jsonify(response), status
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error submitting exam: {str(e)}'}), 500


@exam_bp.route('/exams/<session_id>/auto-submit', methods=['POST'])
def auto_submit(session_id):
    """Auto-submit exam when time expires"""
    try:
        result = ExamService.auto_submit(session_id)
        
        if result['success']:
            response, status = success_response(message=result['message'])
            return jsonify(response), status
        else:
            response, status = error_response(ERR_SESSION_EXPIRED, result['message'], 400)
            return jsonify(response), status
    
    except Exception as e:
        response, status = error_response(ERR_INTERNAL, f'Error auto-submitting: {str(e)}', 500)
        return jsonify(response), status


@exam_bp.route('/exams/<session_id>/answers-detail', methods=['GET'])
def get_exam_answers_detail(session_id):
    """Get exam answers with question details for result review"""
    try:
        from ..models import ExamSession, UserAnswer, Question, ExamResult
        from ..models import db
        
        # Get exam session
        session = ExamService.get_session(session_id)
        if not session['success']:
            response, status = error_response(ERR_SESSION_NOT_FOUND, session['message'], 404)
            return jsonify(response), status
        
        exam_session = session['data']
        
        # Get user answers with question details
        answers = db.session.query(UserAnswer, Question).join(
            Question, UserAnswer.question_id == Question.question_id
        ).filter(
            UserAnswer.session_id == session_id
        ).all()
        
        # Get exam result for scoring
        exam_result = ExamResult.query.filter_by(session_id=session_id).first()
        
        answers_list = []
        for user_answer, question in answers:
            is_correct = user_answer.user_answer == question.correct_answer
            
            answers_list.append({
                'question_id': question.question_id,
                'question_text': question.question_text,
                'option_a': question.option_a,
                'option_b': question.option_b,
                'option_c': question.option_c,
                'option_d': question.option_d,
                'correct_answer': question.correct_answer,
                'user_answer': user_answer.user_answer or '',
                'is_correct': is_correct,
                'difficulty': question.difficulty
            })
        
        response, status = success_response(
            data={
                'session_id': session_id,
                'quiz_id': exam_session.quiz_id,
                'score': exam_result.score if exam_result else 0,
                'status': exam_result.status if exam_result else 'PENDING',
                'submitted_at': exam_result.submitted_at.isoformat() if exam_result else None,
                'answers': answers_list
            },
            message='Exam answers retrieved successfully'
        )
        return jsonify(response), status
    
    except Exception as e:
        response, status = error_response(ERR_INTERNAL, f'Error getting answers: {str(e)}', 500)
        return jsonify(response), status
