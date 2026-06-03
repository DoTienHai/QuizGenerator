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
    app = Flask(__name__)

    if config is None:
        config = get_config()
    app.config.from_object(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print(f"✓ Database initialized: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        print(f"✓ Tables created (quiz, question, exam_session, user_answer, exam_result)")

    app.register_blueprint(frontend_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(result_bp)

    return app


# Create app at module level so other modules and Gunicorn can import it
app = create_app()


if __name__ == '__main__':
    # Run development server only when script is executed directly
    # Not run when imported by other modules or Gunicorn
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
