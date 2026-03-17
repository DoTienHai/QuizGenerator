"""
Routes package for QuizGenerator API
Exports all route blueprints
"""

from .quiz import quiz_bp
from .session import session_bp
from .result import result_bp
from .frontend import frontend_bp

__all__ = [
    'quiz_bp',
    'session_bp',
    'result_bp',
    'frontend_bp',
]
