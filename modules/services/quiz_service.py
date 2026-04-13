"""
QuizService: Quiz management business logic
Handles quiz CRUD operations, validation, and statistics
"""

from datetime import datetime
from ..models import db, Quiz, Question, ExamSession
from .validation_service import ValidationService


class QuizService:
    """Service for managing quiz-related operations"""

    @staticmethod
    def create_quiz(name, questions_data):
        """
        Create a new quiz with questions
        Args:
            name (str) - Quiz name
            questions_data (list) - List of question dictionaries
        Returns:
            dict - {'success': bool, 'data': quiz_obj or None, 'message': str}
        """
        # Validate quiz name
        is_valid, error_msg = ValidationService.validate_quiz_name(name)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        # Validate minimum questions
        is_valid, error_msg = ValidationService.validate_min_questions(len(questions_data))
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        try:
            # Create quiz instance
            quiz = Quiz(
                name=name.strip(),
                total_questions=len(questions_data),
                uploaded_at=datetime.utcnow()
            )
            
            # Validate and create questions
            for q_data in questions_data:
                is_valid, error_msg = ValidationService.validate_question_format(q_data)
                if not is_valid:
                    return {'success': False, 'data': None, 'message': f"Question validation error: {error_msg}"}
                
                question = Question(
                    quiz_id=quiz.quiz_id,  # Will be assigned after quiz insert
                    question_text=q_data['question_text'].strip(),
                    option_a=q_data['option_a'].strip(),
                    option_b=q_data['option_b'].strip(),
                    option_c=q_data['option_c'].strip(),
                    option_d=q_data['option_d'].strip(),
                    correct_answer=str(q_data['correct_answer']).upper(),
                    difficulty=int(q_data.get('difficulty', 3))
                )
                quiz.questions.append(question)
            
            # Save to database
            db.session.add(quiz)
            db.session.commit()
            
            return {
                'success': True,
                'data': quiz,
                'message': f"Quiz '{name}' created successfully with {len(questions_data)} questions"
            }
        
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'data': None, 'message': f"Error creating quiz: {str(e)}"}

    @staticmethod
    def get_quiz(quiz_id):
        """
        Get quiz by ID with all questions
        Args: quiz_id (int) - Quiz ID
        Returns: dict - {'success': bool, 'data': quiz_obj or None, 'message': str}
        """
        is_valid, quiz, error_msg = ValidationService.validate_quiz_exists(quiz_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        return {
            'success': True,
            'data': quiz,
            'message': f"Quiz {quiz_id} retrieved successfully"
        }

    @staticmethod
    def list_quizzes(page=1, per_page=20):
        """
        Get paginated list of all quizzes
        Args:
            page (int) - Page number (1-based)
            per_page (int) - Items per page
        Returns: dict - {'success': bool, 'data': quiz_list, 'pagination': {...}, 'message': str}
        """
        try:
            paginated = Quiz.query.paginate(page=page, per_page=per_page, error_out=False)
            
            return {
                'success': True,
                'data': paginated.items,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': paginated.total,
                    'total_pages': paginated.pages
                },
                'message': f"Retrieved {len(paginated.items)} quizzes from page {page}"
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'pagination': {},
                'message': f"Error listing quizzes: {str(e)}"
            }

    @staticmethod
    def delete_quiz(quiz_id):
        """
        Delete quiz and all associated data (cascade)
        Args: quiz_id (int) - Quiz ID
        Returns: dict - {'success': bool, 'message': str}
        """
        is_valid, quiz, error_msg = ValidationService.validate_quiz_exists(quiz_id)
        if not is_valid:
            return {'success': False, 'message': error_msg}
        
        try:
            db.session.delete(quiz)
            db.session.commit()
            
            return {
                'success': True,
                'message': f"Quiz {quiz_id} and all related data deleted successfully"
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f"Error deleting quiz: {str(e)}"}

    @staticmethod
    def get_quiz_statistics(quiz_id):
        """
        Get statistics for a quiz (attempts, pass rate, avg score, etc.)
        Args: quiz_id (int) - Quiz ID
        Returns: dict - {'success': bool, 'data': stats_dict or None, 'message': str}
        """
        is_valid, quiz, error_msg = ValidationService.validate_quiz_exists(quiz_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        try:
            from ..models import ExamResult
            
            # Get all results for this quiz
            results = ExamResult.query.join(
                ExamSession, ExamResult.session_id == ExamSession.session_id
            ).filter(
                ExamSession.quiz_id == quiz_id,
                ExamResult.status == 'completed'
            ).all()
            
            if not results:
                return {
                    'success': True,
                    'data': {
                        'quiz_id': quiz_id,
                        'quiz_name': quiz.name,
                        'total_attempts': 0,
                        'completed_attempts': 0,
                        'average_score': 0.0,
                        'highest_score': 0,
                        'lowest_score': 0,
                        'pass_count': 0,
                        'pass_rate': 0.0
                    },
                    'message': f"No completed attempts for quiz {quiz_id}"
                }
            
            scores = [r.score for r in results]
            pass_threshold = 80  # 80% to pass
            pass_count = sum(1 for s in scores if s >= pass_threshold)
            
            stats = {
                'quiz_id': quiz_id,
                'quiz_name': quiz.name,
                'total_attempts': len(results),
                'completed_attempts': len(results),
                'average_score': sum(scores) / len(scores),
                'highest_score': max(scores),
                'lowest_score': min(scores),
                'pass_count': pass_count,
                'pass_rate': (pass_count / len(results)) * 100 if results else 0
            }
            
            return {
                'success': True,
                'data': stats,
                'message': f"Statistics retrieved for quiz {quiz_id}"
            }
        
        except Exception as e:
            return {'success': False, 'data': None, 'message': f"Error retrieving statistics: {str(e)}"}

    @staticmethod
    def get_quiz_details(quiz_id):
        """
        Get detailed quiz information with all questions
        Args: quiz_id (int) - Quiz ID
        Returns: dict - Quiz with nested questions
        """
        is_valid, quiz, error_msg = ValidationService.validate_quiz_exists(quiz_id)
        if not is_valid:
            return None
        
        return {
            'quiz_id': quiz.quiz_id,
            'name': quiz.name,
            'total_questions': quiz.total_questions,
            'uploaded_at': quiz.uploaded_at.isoformat(),
            'questions': [
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
                for q in quiz.questions
            ]
        }

    @staticmethod
    def update_quiz_name(quiz_id, new_name):
        """
        Update quiz name
        Args:
            quiz_id (int) - Quiz ID
            new_name (str) - New quiz name
        Returns: dict - {'success': bool, 'message': str}
        """
        is_valid, quiz, error_msg = ValidationService.validate_quiz_exists(quiz_id)
        if not is_valid:
            return {'success': False, 'message': error_msg}
        
        # Validate new name
        is_valid, error_msg = ValidationService.validate_quiz_name(new_name)
        if not is_valid:
            return {'success': False, 'message': error_msg}
        
        try:
            quiz.name = new_name.strip()
            db.session.commit()
            
            return {
                'success': True,
                'message': f"Quiz name updated to '{new_name}'"
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f"Error updating quiz name: {str(e)}"}

if __name__ == '__main__':
    # Example usage
    quiz_service = QuizService()
    result = quiz_service.get_quiz(1)
    if result['success']:
        print(result['data'])
    else:
        print(result['message'])