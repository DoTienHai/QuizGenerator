"""
QuizGenerator - Flask Application
"""
import os
from flask import Flask
from config import get_config
from modules.models import db
from modules.routes.frontend import frontend_bp
from modules.routes.quiz import quiz_bp
from modules.routes.exam import exam_bp
from modules.routes.result import result_bp


def create_app(config=None):
    """Application factory function - initialize Flask app with all settings and database"""
    # Step 1: Create Flask app instance
    app = Flask(__name__)
    
    # Step 2: Load and apply configuration
    # Get config class (DevelopmentConfig, TestingConfig, or ProductionConfig)
    if config is None:
        config = get_config()
    
    # Flask reads all UPPERCASE keywords from config class and stores in app.config
    # Examples: DEBUG=True, SQLALCHEMY_DATABASE_URI='sqlite://...', SECRET_KEY='...'
    app.config.from_object(config)
    
    # Step 3: Initialize database with Flask app
    # db.init_app(app) = connect SQLAlchemy db instance to Flask app
    # This tells db where to find config (database URI, echo settings, etc.)
    # Without this: db doesn't know which app it belongs to
    # After this: db can use app.config['SQLALCHEMY_DATABASE_URI'] to connect
    db.init_app(app)
    
    # Step 4: Create all database tables
    # app.app_context() = Flask context (needed for database operations)
    # db.create_all() = execute CREATE TABLE for all models (Quiz, Question, ExamSession, ...)
    # This only creates tables if they don't exist (idempotent)
    with app.app_context():
        db.create_all()
        print(f"✓ Database initialized: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        print(f"✓ Tables created (quiz, question, exam_session, user_answer, exam_result)")
    
    # Step 5: Register blueprints (route handlers)
    # Blueprint = group of routes (like modules)
    # This connects all routes: /frontend, /api/quizzes, /api/sessions, /api/results
    app.register_blueprint(frontend_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(result_bp)
    
    # Step 6: Return configured app instance
    # Now app is ready to: handle requests, use database, serve routes
    return app


# ==================== Module-level app instance ====================
# Create app at MODULE LEVEL (not inside if __name__)
# Reason: Other modules, tests, and Gunicorn need to import this app
# Example: from app import app
app = create_app()


if __name__ == '__main__':
    # Run development server only when script is executed directly
    # Not run when imported by other modules or Gunicorn
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
