"""
QuestionService: Question management business logic
Handles question CRUD operations, search, and filtering
"""

from ..models import db, Question, Quiz
from .validation_service import ValidationService


class QuestionService:
    """Service for managing quiz questions"""

    @staticmethod
    def get_question(question_id):
        """
        Get a single question by ID (with correct answer hidden for exams)
        Args:
            question_id (int) - Question ID
            include_answer (bool) - Include correct answer in response
        Returns:
            dict - {'success': bool, 'data': question_obj or None, 'message': str}
        """
        is_valid, question, error_msg = ValidationService.validate_question_exists(question_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        return {
            'success': True,
            'data': question,
            'message': f"Question {question_id} retrieved"
        }

    @staticmethod
    def get_question_for_exam(question_id):
        """
        Get question for exam (without correct answer)
        Args: question_id (int) - Question ID
        Returns: dict - Question object without correct_answer field
        """
        is_valid, question, error_msg = ValidationService.validate_question_exists(question_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        # Return question without revealing correct answer
        question_data = {
            'question_id': question.question_id,
            'question_text': question.question_text,
            'option_a': question.option_a,
            'option_b': question.option_b,
            'option_c': question.option_c,
            'option_d': question.option_d,
            'difficulty': question.difficulty
        }
        
        return {
            'success': True,
            'data': question_data,
            'message': f"Question {question_id} retrieved for exam"
        }

    @staticmethod
    def get_quiz_questions(quiz_id, page=1, per_page=20):
        """
        Get paginated list of questions for a quiz
        Args:
            quiz_id (int) - Quiz ID
            page (int) - Page number (1-based)
            per_page (int) - Items per page
        Returns:
            dict - {'success': bool, 'data': questions_list, 'pagination': {...}, 'message': str}
        """
        is_valid, quiz, error_msg = ValidationService.validate_quiz_exists(quiz_id)
        if not is_valid:
            return {'success': False, 'data': None, 'pagination': {}, 'message': error_msg}
        
        try:
            paginated = Question.query.filter_by(quiz_id=quiz_id).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return {
                'success': True,
                'data': paginated.items,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': paginated.total,
                    'total_pages': paginated.pages
                },
                'message': f"Retrieved {len(paginated.items)} questions from quiz {quiz_id}"
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'pagination': {},
                'message': f"Error retrieving questions: {str(e)}"
            }

    @staticmethod
    def search_questions(quiz_id, keyword):
        """
        Search questions by keyword in question text
        Args:
            quiz_id (int) - Quiz ID
            keyword (str) - Search keyword
        Returns:
            dict - {'success': bool, 'data': matching_questions or None, 'message': str}
        """
        is_valid, quiz, error_msg = ValidationService.validate_quiz_exists(quiz_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        if not keyword or len(keyword.strip()) == 0:
            return {'success': False, 'data': None, 'message': "Search keyword cannot be empty"}
        
        try:
            search_term = f"%{keyword.strip()}%"
            questions = Question.query.filter(
                Question.quiz_id == quiz_id,
                Question.question_text.ilike(search_term)
            ).all()
            
            return {
                'success': True,
                'data': questions,
                'message': f"Found {len(questions)} questions matching '{keyword}'"
            }
        
        except Exception as e:
            return {'success': False, 'data': None, 'message': f"Error searching questions: {str(e)}"}

    @staticmethod
    def filter_by_difficulty(quiz_id, difficulty_level):
        """
        Get all questions of a specific difficulty level
        Args:
            quiz_id (int) - Quiz ID
            difficulty_level (int) - Difficulty (1-5)
        Returns:
            dict - {'success': bool, 'data': questions_list or None, 'message': str}
        """
        is_valid, quiz, error_msg = ValidationService.validate_quiz_exists(quiz_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        if not isinstance(difficulty_level, int) or difficulty_level < 1 or difficulty_level > 5:
            return {'success': False, 'data': None, 'message': "Difficulty must be between 1 and 5"}
        
        try:
            questions = Question.query.filter_by(
                quiz_id=quiz_id,
                difficulty=difficulty_level
            ).all()
            
            return {
                'success': True,
                'data': questions,
                'message': f"Found {len(questions)} questions with difficulty {difficulty_level}"
            }
        
        except Exception as e:
            return {'success': False, 'data': None, 'message': f"Error filtering questions: {str(e)}"}

    @staticmethod
    def update_question(question_id, updates):
        """
        Update question details
        Args:
            question_id (int) - Question ID
            updates (dict) - Fields to update (question_text, options, difficulty, etc.)
        Returns:
            dict - {'success': bool, 'message': str}
        """
        is_valid, question, error_msg = ValidationService.validate_question_exists(question_id)
        if not is_valid:
            return {'success': False, 'message': error_msg}
        
        try:
            # Update question text if provided
            if 'question_text' in updates:
                new_text = updates['question_text'].strip()
                if len(new_text) == 0:
                    return {'success': False, 'message': "Question text cannot be empty"}
                if len(new_text) > 2000:
                    return {'success': False, 'message': "Question text exceeds 2000 characters"}
                question.question_text = new_text
            
            # Update options if provided
            for option_key in ['option_a', 'option_b', 'option_c', 'option_d']:
                if option_key in updates:
                    new_option = updates[option_key].strip()
                    if len(new_option) == 0:
                        return {'success': False, 'message': f"{option_key.upper()} cannot be empty"}
                    if len(new_option) > 500:
                        return {'success': False, 'message': f"{option_key.upper()} exceeds 500 characters"}
                    setattr(question, option_key, new_option)
            
            # Update correct answer if provided
            if 'correct_answer' in updates:
                correct_answer = str(updates['correct_answer']).upper()
                if correct_answer not in ['A', 'B', 'C', 'D']:
                    return {'success': False, 'message': "Correct answer must be A, B, C, or D"}
                question.correct_answer = correct_answer
            
            # Update difficulty if provided
            if 'difficulty' in updates:
                try:
                    difficulty = int(updates['difficulty'])
                    if difficulty < 1 or difficulty > 5:
                        return {'success': False, 'message': "Difficulty must be between 1 and 5"}
                    question.difficulty = difficulty
                except (ValueError, TypeError):
                    return {'success': False, 'message': "Difficulty must be a valid integer"}
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f"Question {question_id} updated successfully"
            }
        
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f"Error updating question: {str(e)}"}

    @staticmethod
    def delete_question(question_id):
        """
        Delete a question
        Args: question_id (int) - Question ID
        Returns: dict - {'success': bool, 'message': str}
        """
        is_valid, question, error_msg = ValidationService.validate_question_exists(question_id)
        if not is_valid:
            return {'success': False, 'message': error_msg}
        
        try:
            db.session.delete(question)
            db.session.commit()
            
            return {
                'success': True,
                'message': f"Question {question_id} deleted successfully"
            }
        
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f"Error deleting question: {str(e)}"}

    @staticmethod
    def get_difficulty_distribution(quiz_id):
        """
        Get distribution of questions by difficulty level
        Args: quiz_id (int) - Quiz ID
        Returns:
            dict - {
                'success': bool,
                'data': {'level_1': count, 'level_2': count, ...},
                'message': str
            }
        """
        is_valid, quiz, error_msg = ValidationService.validate_quiz_exists(quiz_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        try:
            distribution = {}
            for level in range(1, 6):
                count = Question.query.filter_by(
                    quiz_id=quiz_id,
                    difficulty=level
                ).count()
                distribution[f'level_{level}'] = count
            
            return {
                'success': True,
                'data': distribution,
                'message': f"Difficulty distribution retrieved for quiz {quiz_id}"
            }
        
        except Exception as e:
            return {'success': False, 'data': None, 'message': f"Error getting distribution: {str(e)}"}
