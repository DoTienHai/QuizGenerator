"""
ValidationService: Centralized validation logic
Used by other services for data validation and business rule enforcement
"""

import re
from datetime import datetime
from ..models import db, Quiz, Question, ExamSession, UserAnswer


class ValidationService:
    """Validation service for quiz-related business rules"""

    @staticmethod
    def validate_quiz_name(name):
        """
        Validate quiz name format
        Args: name (str) - Quiz name to validate
        Returns: tuple (is_valid, error_message)
        """
        if not name or not isinstance(name, str):
            return False, "Quiz name is required and must be a string"
        
        if len(name.strip()) == 0:
            return False, "Quiz name cannot be empty or whitespace only"
        
        if len(name) > 255:
            return False, "Quiz name must not exceed 255 characters"
        
        # Check if name already exists
        existing = Quiz.query.filter_by(name=name.strip()).first()
        if existing:
            return False, f"Quiz name '{name}' already exists"
        
        return True, None

    @staticmethod
    def validate_question_format(question_data):
        """
        Validate question data format
        Args: question_data (dict) - Question with text, options, correct_answer
        Returns: tuple (is_valid, error_message)
        """
        required_fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
        
        # Check all required fields
        missing_fields = [field for field in required_fields if field not in question_data]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # Validate question text
        question_text = question_data.get('question_text', '').strip()
        if not question_text or len(question_text) == 0:
            return False, "Question text cannot be empty"
        if len(question_text) > 2000:
            return False, "Question text must not exceed 2000 characters"
        
        # Validate options
        for option_key in ['option_a', 'option_b', 'option_c', 'option_d']:
            option_text = question_data.get(option_key, '').strip()
            if not option_text or len(option_text) == 0:
                return False, f"{option_key.upper()} cannot be empty"
            if len(option_text) > 500:
                return False, f"{option_key.upper()} must not exceed 500 characters"
        
        # Validate correct answer
        correct_answer = str(question_data.get('correct_answer', '')).upper()
        if correct_answer not in ['A', 'B', 'C', 'D']:
            return False, "Correct answer must be A, B, C, or D"
        
        # Validate difficulty if present
        if 'difficulty' in question_data:
            try:
                difficulty = int(question_data['difficulty'])
                if difficulty < 1 or difficulty > 5:
                    return False, "Difficulty must be between 1 and 5"
            except (ValueError, TypeError):
                return False, "Difficulty must be a valid integer"
        
        return True, None

    @staticmethod
    def validate_options_list(options):
        """
        Validate options list (from Excel)
        Args: options (list) - List of 4 options
        Returns: tuple (is_valid, error_message)
        """
        if not isinstance(options, list):
            return False, "Options must be a list"
        
        if len(options) != 4:
            return False, "Must have exactly 4 options"
        
        for i, option in enumerate(options, 1):
            if not isinstance(option, str) or len(option.strip()) == 0:
                return False, f"Option {i} cannot be empty"
            if len(option) > 500:
                return False, f"Option {i} exceeds 500 character limit"
        
        return True, None

    @staticmethod
    def validate_quiz_exists(quiz_id):
        """
        Check if quiz exists
        Args: quiz_id (int) - Quiz ID
        Returns: tuple (exists, quiz_obj, error_message)
        """
        if not quiz_id or not isinstance(quiz_id, int):
            return False, None, "Quiz ID must be a valid integer"
        
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return False, None, f"Quiz {quiz_id} not found"
        
        return True, quiz, None

    @staticmethod
    def validate_session_exists(session_id):
        """
        Check if exam session exists
        Args: session_id (str) - Session UUID
        Returns: tuple (exists, session_obj, error_message)
        """
        if not session_id or not isinstance(session_id, str):
            return False, None, "Session ID must be a valid string"
        
        session = ExamSession.query.get(session_id)
        if not session:
            return False, None, f"Session {session_id} not found"
        
        return True, session, None

    @staticmethod
    def validate_session_active(session):
        """
        Check if session is active and not expired
        Args: session (ExamSession) - Session object
        Returns: tuple (is_active, error_message)
        """
        if session.status == 'expired':
            return False, f"Session {session.session_id} has expired"
        
        if session.status == 'submitted':
            return False, f"Session {session.session_id} has already been submitted"
        
        if session.status != 'active':
            return False, f"Session {session.session_id} is not active (status: {session.status})"
        
        # Check if session has exceeded time limit
        now = datetime.utcnow()
        if now > session.expires_at:
            return False, f"Session {session.session_id} has expired"
        
        return True, None

    @staticmethod
    def validate_answer_format(answer_data):
        """
        Validate answer submission format
        Args: answer_data (dict) - Answer with question_id and user_answer
        Returns: tuple (is_valid, error_message)
        """
        required_fields = ['question_id', 'user_answer']
        
        missing_fields = [field for field in required_fields if field not in answer_data]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # Validate question_id
        try:
            question_id = int(answer_data['question_id'])
            if question_id <= 0:
                return False, "Question ID must be positive"
        except (ValueError, TypeError):
            return False, "Question ID must be a valid integer"
        
        # Validate user_answer
        user_answer = str(answer_data.get('user_answer', '')).upper()
        if user_answer and user_answer not in ['A', 'B', 'C', 'D']:
            return False, "User answer must be A, B, C, D, or empty (skip)"
        
        return True, None

    @staticmethod
    def validate_question_exists(question_id):
        """
        Check if question exists
        Args: question_id (int) - Question ID
        Returns: tuple (exists, question_obj, error_message)
        """
        if not question_id or not isinstance(question_id, int):
            return False, None, "Question ID must be a valid integer"
        
        question = Question.query.get(question_id)
        if not question:
            return False, None, f"Question {question_id} not found"
        
        return True, question, None

    @staticmethod
    def validate_session_has_questions(session):
        """
        Verify session has questions available
        Args: session (ExamSession) - Session object
        Returns: tuple (has_questions, error_message)
        """
        if not session.user_answers or len(session.user_answers) == 0:
            return False, "Session has no questions available"
        
        return True, None

    @staticmethod
    def validate_min_questions(total_questions, min_required=5):
        """
        Validate minimum number of questions
        Args: total_questions (int) - Total question count
               min_required (int) - Minimum required (default: 5)
        Returns: tuple (is_valid, error_message)
        """
        if not isinstance(total_questions, int) or total_questions <= 0:
            return False, "Total questions must be a positive integer"
        
        if total_questions < min_required:
            return False, f"At least {min_required} questions are required"
        
        return True, None
