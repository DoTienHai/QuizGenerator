"""
Quiz Routes: CRUD operations for quizzes
Integrated with QuizService and ExcelImportService
"""

from flask import Blueprint, jsonify, request
from ..services import QuizService, ExcelImportService, ValidationService

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api')


@quiz_bp.route('/quizzes', methods=['POST'])
def upload_quiz():
    """
    Upload Excel file with questions (create quiz)
    Expected form data:
        - file: Excel file (.xlsx)
        - quiz_name: Name for the quiz
    """
    try:
        # Check if file and quiz_name provided
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        if not request.form.get('quiz_name'):
            return jsonify({'success': False, 'message': 'Quiz name is required'}), 400
        
        file = request.files['file']
        quiz_name = request.form.get('quiz_name').strip()
        
        # Validate file type
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'success': False, 'message': 'Only Excel files (.xlsx, .xls) are accepted'}), 400
        
        # Read file content
        file_content = file.read()
        
        # Initialize ExcelImportService with file
        service = ExcelImportService(file_content)
        
        # Validate file structure
        if not service.validate():
            return jsonify({'success': False, 'message': service.error_message}), 400
        
        # Parse Excel file
        parse_result = service.parse(quiz_name)
        if not parse_result['success']:
            return jsonify({'success': False, 'message': parse_result['message']}), 400
        
        # Import as quiz
        result = service.import_as_quiz(quiz_name)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': {
                    'quiz_id': result['data'].quiz_id,
                    'name': result['data'].name,
                    'total_questions': result['data'].total_questions
                },
                'message': result['message']
            }), 201
        else:
            return jsonify({'success': False, 'message': result['message']}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error uploading quiz: {str(e)}'}), 500


@quiz_bp.route('/quizzes', methods=['GET'])
def list_quizzes():
    """Get paginated list of all quizzes"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        result = QuizService.list_quizzes(page=page, per_page=per_page)
        
        return jsonify({
            'success': result['success'],
            'data': [
                {
                    'quiz_id': q.quiz_id,
                    'name': q.name,
                    'total_questions': q.total_questions,
                    'uploaded_at': q.uploaded_at.isoformat()
                }
                for q in result['data']
            ],
            'pagination': result['pagination'],
            'message': result['message']
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error listing quizzes: {str(e)}'}), 500


@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get quiz by ID with all questions"""
    try:
        result = QuizService.get_quiz(quiz_id)
        
        if result['success']:
            quiz_details = QuizService.get_quiz_details(quiz_id)
            return jsonify({
                'success': True,
                'data': quiz_details,
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting quiz: {str(e)}'}), 500


@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    """Delete quiz and all associated data"""
    try:
        result = QuizService.delete_quiz(quiz_id)
        
        if result['success']:
            return jsonify({'success': True, 'message': result['message']}), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error deleting quiz: {str(e)}'}), 500


@quiz_bp.route('/quizzes/<int:quiz_id>/statistics', methods=['GET'])
def get_quiz_statistics(quiz_id):
    """Get statistics for a quiz (attempts, pass rate, avg score)"""
    try:
        result = QuizService.get_quiz_statistics(quiz_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting statistics: {str(e)}'}), 500


@quiz_bp.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
def get_quiz_questions(quiz_id):
    """Get all questions for a quiz with pagination"""
    try:
        from ..services import QuestionService
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        result = QuestionService.get_quiz_questions(quiz_id, page=page, per_page=per_page)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': [
                    {
                        'question_id': q.question_id,
                        'question_text': q.question_text,
                        'option_a': q.option_a,
                        'option_b': q.option_b,
                        'option_c': q.option_c,
                        'option_d': q.option_d,
                        'correct_answer': q.correct_answer,
                        'difficulty': q.difficulty
                    }
                    for q in result['data']
                ],
                'pagination': result['pagination'],
                'message': result['message']
            }), 200
        else:
            return jsonify({'success': False, 'message': result['message']}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting questions: {str(e)}'}), 500


@quiz_bp.route('/templates/quiz', methods=['GET'])
def get_quiz_template():
    """Download Excel template for quiz creation"""
    try:
        template = ExcelImportService.get_import_template()
        
        if template:
            return template.getvalue(), 200, {
                'Content-Disposition': 'attachment; filename=quiz_template.xlsx',
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }
        else:
            return jsonify({'success': False, 'message': 'Error generating template'}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error downloading template: {str(e)}'}), 500
