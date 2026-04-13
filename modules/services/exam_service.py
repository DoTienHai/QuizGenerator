"""
ExamService: Exam session management business logic
Handles session creation, answer submission, auto-submit, and status tracking
"""

import random
from datetime import datetime, timedelta
from ..models import db, ExamSession, Question, UserAnswer, ExamResult, Quiz
from .validation_service import ValidationService


class ExamService:
    """Service for managing exam sessions and submissions"""

    @staticmethod
    def create_session(quiz_id, num_questions=None, duration_minutes=30):
        """
        Create a new exam session
        Args:
            quiz_id (int) - Quiz ID to use for session
            num_questions (int, optional) - Number of random questions. If None, use all
            duration_minutes (int) - Duration in minutes (default: 30)
        Returns:
            dict - {'success': bool, 'data': session_obj or None, 'message': str}
        """
        # Validate quiz exists
        is_valid, quiz, error_msg = ValidationService.validate_quiz_exists(quiz_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        # Determine number of questions
        if num_questions is None:
            num_questions = quiz.total_questions
        elif num_questions > quiz.total_questions:
            return {
                'success': False,
                'data': None,
                'message': f"Cannot request {num_questions} questions when only {quiz.total_questions} available"
            }
        elif num_questions < 1:
            return {
                'success': False,
                'data': None,
                'message': "Must have at least 1 question in session"
            }
        
        # Validate duration
        if duration_minutes < 1:
            return {
                'success': False,
                'data': None,
                'message': "Duration must be at least 1 minute"
            }
        
        try:
            # Create exam session
            now = datetime.utcnow()
            session = ExamSession(
                quiz_id=quiz_id,
                num_questions=num_questions,
                exam_duration=duration_minutes,
                created_at=now,
                expires_at=now + timedelta(minutes=duration_minutes),
                status='active'
            )
            
            # Get random questions
            questions = Question.query.filter_by(quiz_id=quiz_id).all()
            selected_questions = random.sample(questions, min(num_questions, len(questions)))
            
            # Create user_answer records (for tracking)
            # Each answer will be filled as user responds
            for question in selected_questions:
                user_answer = UserAnswer(
                    session_id=session.session_id,
                    question_id=question.question_id,
                    user_answer=None,  # Not answered yet
                    is_correct=None,   # Unknown until submission
                    answered_at=None
                )
                session.user_answers.append(user_answer)
            
            db.session.add(session)
            db.session.commit()
            
            return {
                'success': True,
                'data': session,
                'message': f"Exam session created with {num_questions} questions, expires at {session.expires_at}"
            }
        
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'data': None, 'message': f"Error creating exam session: {str(e)}"}

    @staticmethod
    def get_session(session_id):
        """
        Get exam session details
        Args: session_id (str) - Session UUID
        Returns: dict - {'success': bool, 'data': session_obj or None, 'message': str}
        """
        is_valid, session, error_msg = ValidationService.validate_session_exists(session_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        return {
            'success': True,
            'data': session,
            'message': f"Session {session_id} retrieved"
        }

    @staticmethod
    def get_session_status(session_id):
        """
        Get current session status and remaining time
        Args: session_id (str) - Session UUID
        Returns: dict - Detailed status information
        """
        is_valid, session, error_msg = ValidationService.validate_session_exists(session_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        now = datetime.utcnow()
        time_remaining = session.expires_at - now
        
        # Count answered questions
        answered = sum(1 for ua in session.user_answers if ua.user_answer is not None)
        skipped = len(session.user_answers) - answered
        
        status_info = {
            'session_id': session.session_id,
            'quiz_id': session.quiz_id,
            'status': session.status,
            'total_questions': session.num_questions,
            'answered_count': answered,
            'skipped_count': skipped,
            'duration_minutes': session.exam_duration,
            'created_at': session.created_at.isoformat(),
            'expires_at': session.expires_at.isoformat(),
            'time_remaining_seconds': int(time_remaining.total_seconds()),
            'is_expired': time_remaining.total_seconds() <= 0
        }
        
        return {
            'success': True,
            'data': status_info,
            'message': f"Session status retrieved"
        }

    @staticmethod
    def submit_answer(session_id, question_id, user_answer):
        """
        Submit a single answer
        Args:
            session_id (str) - Session UUID
            question_id (int) - Question ID
            user_answer (str) - User's answer (A, B, C, D, or empty for skip)
        Returns:
            dict - {'success': bool, 'message': str}
        """
        # Validate session
        is_valid, session, error_msg = ValidationService.validate_session_exists(session_id)
        if not is_valid:
            return {'success': False, 'message': error_msg}
        
        # Validate session is active
        is_active, error_msg = ValidationService.validate_session_active(session)
        if not is_active:
            return {'success': False, 'message': error_msg}
        
        # Validate question
        is_valid, question, error_msg = ValidationService.validate_question_exists(question_id)
        if not is_valid:
            return {'success': False, 'message': error_msg}
        
        # Validate answer format
        is_valid, error_msg = ValidationService.validate_answer_format({
            'question_id': question_id,
            'user_answer': user_answer
        })
        if not is_valid:
            return {'success': False, 'message': error_msg}
        
        try:
            # Find or create user answer record
            answer_record = UserAnswer.query.filter_by(
                session_id=session_id,
                question_id=question_id
            ).first()
            
            if answer_record:
                answer_record.user_answer = user_answer.upper() if user_answer else None
                answer_record.answered_at = datetime.utcnow()
                # Mark answer as correct or incorrect
                if user_answer:
                    answer_record.is_correct = (user_answer.upper() == question.correct_answer)
            else:
                # Should not happen, but create if missing
                answer_record = UserAnswer(
                    session_id=session_id,
                    question_id=question_id,
                    user_answer=user_answer.upper() if user_answer else None,
                    is_correct=(user_answer.upper() == question.correct_answer) if user_answer else None,
                    answered_at=datetime.utcnow()
                )
                db.session.add(answer_record)
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f"Answer for question {question_id} recorded"
            }
        
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f"Error submitting answer: {str(e)}"}

    @staticmethod
    def submit_exam(session_id, answers=None):
        """
        Submit exam (final submission)
        Args: 
            session_id (str) - Session UUID
            answers (dict) - User answers {question_id: user_answer, ...}
        Returns: dict - {'success': bool, 'data': result_obj or None, 'message': str}
        """
        # Validate session
        is_valid, session, error_msg = ValidationService.validate_session_exists(session_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        # Validate session is active
        is_active, error_msg = ValidationService.validate_session_active(session)
        if not is_active:
            return {'success': False, 'data': None, 'message': error_msg}
        
        try:
            # Update user answers with provided answers and check correctness
            if answers and isinstance(answers, dict):
                for question_id_str, answer in answers.items():
                    try:
                        question_id = int(question_id_str)
                        # Find and update the UserAnswer record
                        user_answer_record = UserAnswer.query.filter_by(
                            session_id=session_id,
                            question_id=question_id
                        ).first()
                        
                        if user_answer_record:
                            user_answer_record.user_answer = answer if answer else None
                            user_answer_record.answered_at = datetime.utcnow()
                            
                            # Determine if answer is correct
                            if answer:  # Only mark correct/incorrect if answer provided
                                question = Question.query.get(question_id)
                                if question:
                                    # Compare user answer with correct answer
                                    user_answer_record.is_correct = (answer.upper() == question.correct_answer.upper())
                            else:  # No answer = skipped
                                user_answer_record.is_correct = None
                                
                    except (ValueError, TypeError):
                        pass  # Skip invalid question IDs
            
            # Update session status
            session.status = 'submitted'
            
            # Calculate results
            from .scoring_engine import ScoringEngine
            result_data = ScoringEngine.calculate_score(session_id)
            
            if not result_data['success']:
                db.session.rollback()
                return {
                    'success': False,
                    'data': None,
                    'message': f"Error calculating score: {result_data['message']}"
                }
            
            # Calculate time spent in seconds
            time_spent_seconds = None
            if session.created_at:
                time_diff = datetime.utcnow() - session.created_at
                time_spent_seconds = int(time_diff.total_seconds())  # Total seconds
            
            # Create ExamResult record
            exam_result = ExamResult(
                session_id=session_id,
                quiz_id=session.quiz_id,
                score=result_data['data']['score'],
                correct_count=result_data['data']['correct_count'],
                incorrect_count=result_data['data']['incorrect_count'],
                skipped_count=result_data['data']['skipped_count'],
                status='PASS' if result_data['data']['score'] >= 80 else 'FAIL',
                submitted_at=datetime.utcnow(),
                time_spent_seconds=time_spent_seconds
            )
            
            db.session.add(exam_result)
            db.session.commit()
            
            return {
                'success': True,
                'data': exam_result,
                'message': f"Exam submitted successfully. Score: {result_data['data']['score']}"
            }
        
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'data': None, 'message': f"Error submitting exam: {str(e)}"}

    @staticmethod
    def auto_submit(session_id):
        """
        Auto-submit when time expires
        Args: session_id (str) - Session UUID
        Returns: dict - {'success': bool, 'message': str}
        """
        # Validate session
        is_valid, session, error_msg = ValidationService.validate_session_exists(session_id)
        if not is_valid:
            return {'success': False, 'message': error_msg}
        
        try:
            # Mark session as expired
            session.status = 'expired'
            
            # Calculate and save results
            from .scoring_engine import ScoringEngine
            result_data = ScoringEngine.calculate_score(session_id)
            
            if result_data['success']:
                exam_result = ExamResult(
                    session_id=session_id,
                    score=result_data['data']['score'],
                    correct_count=result_data['data']['correct_count'],
                    incorrect_count=result_data['data']['incorrect_count'],
                    skipped_count=result_data['data']['skipped_count'],
                    status='auto_submitted',
                    submitted_at=datetime.utcnow()
                )
                db.session.add(exam_result)
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f"Session {session_id} auto-submitted due to time expiration"
            }
        
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f"Error auto-submitting: {str(e)}"}

    @staticmethod
    def get_session_questions(session_id):
        """
        Get all questions for a session (for display during exam)
        Args: session_id (str) - Session UUID
        Returns: dict - {'success': bool, 'data': questions_list or None, 'message': str}
        """
        is_valid, session, error_msg = ValidationService.validate_session_exists(session_id)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        try:
            # Get questions from user_answers (maintains order)
            questions = []
            for user_answer in session.user_answers:
                question = Question.query.get(user_answer.question_id)
                if question:
                    questions.append({
                        'question_id': question.question_id,
                        'question_text': question.question_text,
                        'option_a': question.option_a,
                        'option_b': question.option_b,
                        'option_c': question.option_c,
                        'option_d': question.option_d,
                        'difficulty': question.difficulty,
                        'answered': user_answer.user_answer is not None
                    })
            
            return {
                'success': True,
                'data': questions,
                'message': f"Retrieved {len(questions)} questions for session"
            }
        
        except Exception as e:
            return {'success': False, 'data': None, 'message': f"Error retrieving questions: {str(e)}"}
