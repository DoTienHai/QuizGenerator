from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    """Homepage - Main landing page"""
    return render_template('index.html')

@frontend_bp.route('/upload')
def upload():
    """Quiz upload page"""
    return render_template('upload.html')

@frontend_bp.route('/list-quizzes')
def list_quizzes_page():
    """List all quizzes page"""
    return render_template('list-quizzes.html')

@frontend_bp.route('/exam')
def exam():
    """Exam page - Take exam"""
    return render_template('exam.html')

@frontend_bp.route('/results')
def results():
    """Results page - View exam results"""
    return render_template('results.html')
