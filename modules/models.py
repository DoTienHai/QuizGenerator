"""
Database Models for QuizGenerator
All 5 models in one file (suitable for MVP with 5 tables)
"""

import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Global database instance
db = SQLAlchemy()


# ===== Table 1: Quiz =====
class Quiz(db.Model):
    """Store quiz/question bank metadata"""
    __tablename__ = 'quiz'

    quiz_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    total_questions = db.Column(
        db.Integer,
        db.CheckConstraint('total_questions > 0'),
        nullable=False
    )
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    questions = db.relationship(
        'Question',
        back_populates='quiz',
        cascade='all, delete-orphan',
        lazy='joined'
    )
    sessions = db.relationship(
        'ExamSession',
        back_populates='quiz',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<Quiz {self.quiz_id}: {self.name}>'


# ===== Table 2: Question =====
class Question(db.Model):
    """Store individual questions and options"""
    __tablename__ = 'question'

    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey('quiz.quiz_id', ondelete='CASCADE'),
        nullable=False
    )
    question_text = db.Column(
        db.String(2000),
        db.CheckConstraint('LENGTH(question_text) <= 2000'),
        nullable=False
    )
    option_a = db.Column(
        db.String(500),
        db.CheckConstraint('LENGTH(option_a) <= 500'),
        nullable=False
    )
    option_b = db.Column(
        db.String(500),
        db.CheckConstraint('LENGTH(option_b) <= 500'),
        nullable=False
    )
    option_c = db.Column(
        db.String(500),
        db.CheckConstraint('LENGTH(option_c) <= 500'),
        nullable=False
    )
    option_d = db.Column(
        db.String(500),
        db.CheckConstraint('LENGTH(option_d) <= 500'),
        nullable=False
    )
    correct_answer = db.Column(
        db.String(1),
        db.CheckConstraint("correct_answer IN ('A','B','C','D')"),
        nullable=False
    )
    difficulty = db.Column(
        db.Integer,
        db.CheckConstraint('difficulty BETWEEN 1 AND 5')
    )

    # Relationships
    quiz = db.relationship('Quiz', back_populates='questions')
    user_answers = db.relationship(
        'UserAnswer',
        back_populates='question',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    # Indexes for better query performance
    __table_args__ = (
        db.Index('idx_question_quiz', 'quiz_id'),
    )

    def __repr__(self):
        return f'<Question {self.question_id}: Quiz {self.quiz_id}>'


# ===== Table 3: ExamSession =====
class ExamSession(db.Model):
    """Track quiz taking sessions with UUID for security"""
    __tablename__ = 'exam_session'

    session_id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey('quiz.quiz_id', ondelete='CASCADE'),
        nullable=False
    )
    num_questions = db.Column(
        db.Integer,
        db.CheckConstraint('num_questions >= 1'),
        nullable=False
    )
    exam_duration = db.Column(
        db.Integer,
        db.CheckConstraint('exam_duration >= 1'),
        nullable=False
    )  # in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.String(10),
        db.CheckConstraint("status IN ('active', 'submitted', 'expired')"),
        default='active',
        nullable=False
    )

    # Relationships
    quiz = db.relationship('Quiz', back_populates='sessions')
    user_answers = db.relationship(
        'UserAnswer',
        back_populates='session',
        cascade='all, delete-orphan',
        lazy='joined'
    )
    exam_result = db.relationship(
        'ExamResult',
        back_populates='session',
        uselist=False,
        cascade='all, delete-orphan',
        lazy='joined'
    )

    # Indexes for better query performance
    __table_args__ = (
        db.Index('idx_session_quiz', 'quiz_id'),
        db.Index('idx_session_status', 'status'),
    )

    def __repr__(self):
        return f'<ExamSession {self.session_id}: Quiz {self.quiz_id}>'


# ===== Table 4: UserAnswer =====
class UserAnswer(db.Model):
    """Store user's answers for each question in a session"""
    __tablename__ = 'user_answer'

    answer_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.String(36),
        db.ForeignKey('exam_session.session_id', ondelete='CASCADE'),
        nullable=False
    )
    question_id = db.Column(
        db.Integer,
        db.ForeignKey('question.question_id', ondelete='RESTRICT'),
        nullable=False
    )
    user_answer = db.Column(
        db.String(1),
        db.CheckConstraint("user_answer IN ('A','B','C','D',NULL)")
    )
    is_correct = db.Column(db.Boolean)  # Computed after submission
    answered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    session = db.relationship('ExamSession', back_populates='user_answers')
    question = db.relationship('Question', back_populates='user_answers')

    # Unique constraint: one answer per question per session
    # Indexes for better query performance
    __table_args__ = (
        db.UniqueConstraint('session_id', 'question_id', name='uq_session_question'),
        db.Index('idx_answer_session', 'session_id'),
        db.Index('idx_answer_correct', 'is_correct'),
    )

    def __repr__(self):
        return f'<UserAnswer {self.answer_id}: Session {self.session_id}>'


# ===== Table 5: ExamResult =====
class ExamResult(db.Model):
    """Store final exam results and score"""
    __tablename__ = 'exam_result'

    result_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.String(36),
        db.ForeignKey('exam_session.session_id', ondelete='CASCADE'),
        unique=True,
        nullable=False
    )
    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey('quiz.quiz_id'),
        nullable=False
    )
    score = db.Column(
        db.Float,
        db.CheckConstraint('score BETWEEN 0 AND 100')
    )  # Percentage
    correct_count = db.Column(db.Integer, default=0)
    incorrect_count = db.Column(db.Integer, default=0)
    skipped_count = db.Column(db.Integer, default=0)
    status = db.Column(
        db.String(10),
        db.CheckConstraint("status IN ('PASS', 'FAIL')")
    )  # Pass if score >= 80
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    time_spent_seconds = db.Column(db.Integer)

    # Relationships
    session = db.relationship('ExamSession', back_populates='exam_result')
    quiz = db.relationship('Quiz')

    def __repr__(self):
        return f'<ExamResult {self.result_id}: Session {self.session_id}>'
