"""
Result Routes: Exam results and scoring
Integrated with ScoringEngine
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import func, case
from ..services import ScoringEngine
from ..models import ExamResult, Quiz, ExamSession, db

result_bp = Blueprint('result', __name__, url_prefix='/api')


def _build_result_dict(exam_result, quiz, session):
    return {
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
    }


@result_bp.route('/results', methods=['GET'])
def list_results():
    """
    List completed exams with scores.
    - Paginated mode: ?quiz_id=X&page=N&per_page=10 → returns data + stats + pagination
    - Legacy mode: no page param → returns all results (backward compat for /exams page)
    """
    try:
        quiz_id = request.args.get('quiz_id', type=int)
        page = request.args.get('page', type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)

        base_query = db.session.query(ExamResult, Quiz, ExamSession).join(
            Quiz, ExamResult.quiz_id == Quiz.quiz_id
        ).join(
            ExamSession, ExamResult.session_id == ExamSession.session_id
        )
        if quiz_id:
            base_query = base_query.filter(ExamResult.quiz_id == quiz_id)
        base_query = base_query.order_by(ExamResult.submitted_at.desc())

        # Paginated mode: quiz_id + page both provided
        if page is not None and quiz_id is not None:
            agg = db.session.query(
                func.count(ExamResult.result_id).label('total'),
                func.avg(ExamResult.score).label('avg_score'),
                func.sum(case((ExamResult.status == 'PASS', 1), else_=0)).label('pass_count')
            ).filter(ExamResult.quiz_id == quiz_id).one()

            total = agg.total or 0
            avg_score = round(float(agg.avg_score or 0), 1)
            pass_count = int(agg.pass_count or 0)
            total_pages = max(1, (total + per_page - 1) // per_page)
            page = max(1, min(page, total_pages))
            offset = (page - 1) * per_page

            results = base_query.limit(per_page).offset(offset).all()
            exam_list = [_build_result_dict(er, q, s) for er, q, s in results]

            return jsonify({
                'success': True,
                'data': exam_list,
                'stats': {
                    'total_attempts': total,
                    'pass_count': pass_count,
                    'fail_count': total - pass_count,
                    'avg_score': avg_score
                },
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                }
            }), 200

        # Legacy mode: return all results (used by /exams page)
        results = base_query.all()
        exam_list = [_build_result_dict(er, q, s) for er, q, s in results]
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
