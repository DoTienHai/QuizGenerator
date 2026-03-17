"""
ScoringEngine: Score calculation and analysis logic
Handles score computation, grading, and statistics
"""

from datetime import datetime
from ..models import db, ExamSession, UserAnswer, Question, ExamResult


class ScoringEngine:
    """Engine for calculating scores and generating result statistics"""

    @staticmethod
    def calculate_score(session_id):
        """
        Calculate score for a completed exam session
        Args: session_id (str) - Session UUID
        Returns:
            dict - {
                'success': bool,
                'data': {
                    'score': float (0-100),
                    'grade': str (A-F),
                    'correct_count': int,
                    'incorrect_count': int,
                    'skipped_count': int,
                    'total_questions': int,
                    'pass': bool
                },
                'message': str
            }
        """
        try:
            session = ExamSession.query.get(session_id)
            if not session:
                return {
                    'success': False,
                    'data': None,
                    'message': f"Session {session_id} not found"
                }
            
            # Get all answers for this session
            answers = UserAnswer.query.filter_by(session_id=session_id).all()
            
            if not answers:
                return {
                    'success': False,
                    'data': None,
                    'message': f"No answers found for session {session_id}"
                }
            
            # Count correct, incorrect, and skipped
            correct_count = sum(1 for a in answers if a.is_correct is True)
            incorrect_count = sum(1 for a in answers if a.is_correct is False)
            skipped_count = sum(1 for a in answers if a.is_correct is None)
            
            total_questions = len(answers)
            
            # Calculate percentage score
            score = (correct_count / total_questions * 100) if total_questions > 0 else 0
            
            # Determine grade
            grade = ScoringEngine._get_grade(score)
            
            # Pass/Fail (70% threshold)
            pass_threshold = 70
            is_pass = score >= pass_threshold
            
            result = {
                'score': round(score, 2),
                'grade': grade,
                'correct_count': correct_count,
                'incorrect_count': incorrect_count,
                'skipped_count': skipped_count,
                'total_questions': total_questions,
                'pass': is_pass,
                'pass_threshold': pass_threshold
            }
            
            return {
                'success': True,
                'data': result,
                'message': f"Score calculated: {score:.2f}% ({grade})"
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f"Error calculating score: {str(e)}"
            }

    @staticmethod
    def _get_grade(score):
        """
        Convert numeric score to letter grade
        Args: score (float) - Score percentage (0-100)
        Returns: str - Letter grade (A, B, C, D, F)
        
        Grading scale:
        A: 90-100
        B: 80-89
        C: 70-79
        D: 60-69
        F: 0-59
        """
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

    @staticmethod
    def get_result_details(session_id):
        """
        Get detailed result breakdown with question-by-question analysis
        Args: session_id (str) - Session UUID
        Returns:
            dict - {
                'success': bool,
                'data': {
                    'score': float,
                    'grade': str,
                    'answers': [
                        {
                            'question_id': int,
                            'question_text': str,
                            'user_answer': str,
                            'correct_answer': str,
                            'is_correct': bool,
                            'difficulty': int
                        },
                        ...
                    ]
                },
                'message': str
            }
        """
        try:
            session = ExamSession.query.get(session_id)
            if not session:
                return {'success': False, 'data': None, 'message': f"Session not found"}
            
            # Get score
            score_result = ScoringEngine.calculate_score(session_id)
            if not score_result['success']:
                return score_result
            
            score_info = score_result['data']
            
            # Get detailed answers
            answers = UserAnswer.query.filter_by(session_id=session_id).all()
            
            detailed_answers = []
            for answer in answers:
                question = Question.query.get(answer.question_id)
                if question:
                    detailed_answers.append({
                        'question_id': question.question_id,
                        'question_text': question.question_text,
                        'option_a': question.option_a,
                        'option_b': question.option_b,
                        'option_c': question.option_c,
                        'option_d': question.option_d,
                        'user_answer': answer.user_answer,
                        'correct_answer': question.correct_answer,
                        'is_correct': answer.is_correct,
                        'difficulty': question.difficulty,
                        'answered_at': answer.answered_at.isoformat() if answer.answered_at else None
                    })
            
            result = {
                'session_id': session_id,
                'quiz_id': session.quiz_id,
                'score': score_info['score'],
                'grade': score_info['grade'],
                'correct_count': score_info['correct_count'],
                'incorrect_count': score_info['incorrect_count'],
                'skipped_count': score_info['skipped_count'],
                'total_questions': score_info['total_questions'],
                'pass': score_info['pass'],
                'submitted_at': ExamResult.query.filter_by(session_id=session_id).first().submitted_at.isoformat() if ExamResult.query.filter_by(session_id=session_id).first() else None,
                'answers': detailed_answers
            }
            
            return {
                'success': True,
                'data': result,
                'message': f"Result details retrieved"
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f"Error retrieving result details: {str(e)}"
            }

    @staticmethod
    def get_statistics_by_difficulty(session_id):
        """
        Get score breakdown by question difficulty
        Args: session_id (str) - Session UUID
        Returns:
            dict - {
                'success': bool,
                'data': {
                    'difficulty_1': {'correct': int, 'incorrect': int, 'skipped': int},
                    'difficulty_2': {...},
                    ...
                },
                'message': str
            }
        """
        try:
            answers = UserAnswer.query.filter_by(session_id=session_id).all()
            
            stats = {}
            for difficulty_level in range(1, 6):
                stats[f'difficulty_{difficulty_level}'] = {
                    'correct': 0,
                    'incorrect': 0,
                    'skipped': 0,
                    'total': 0
                }
            
            for answer in answers:
                question = Question.query.get(answer.question_id)
                if question:
                    difficulty_key = f'difficulty_{question.difficulty}'
                    stats[difficulty_key]['total'] += 1
                    
                    if answer.is_correct is True:
                        stats[difficulty_key]['correct'] += 1
                    elif answer.is_correct is False:
                        stats[difficulty_key]['incorrect'] += 1
                    else:
                        stats[difficulty_key]['skipped'] += 1
            
            # Remove empty difficulty levels
            stats = {k: v for k, v in stats.items() if v['total'] > 0}
            
            return {
                'success': True,
                'data': stats,
                'message': f"Statistics by difficulty retrieved"
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f"Error calculating statistics: {str(e)}"
            }

    @staticmethod
    def compare_scores(session_ids):
        """
        Compare scores across multiple sessions
        Args: session_ids (list) - List of session UUIDs
        Returns:
            dict - {
                'success': bool,
                'data': [
                    {'session_id': str, 'score': float, 'grade': str, 'passed': bool},
                    ...
                ],
                'message': str
            }
        """
        try:
            comparison = []
            
            for session_id in session_ids:
                result = ScoringEngine.calculate_score(session_id)
                if result['success']:
                    comparison.append({
                        'session_id': session_id,
                        'score': result['data']['score'],
                        'grade': result['data']['grade'],
                        'passed': result['data']['pass']
                    })
            
            return {
                'success': True,
                'data': comparison,
                'message': f"Score comparison retrieved for {len(comparison)} sessions"
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f"Error comparing scores: {str(e)}"
            }
