"""
QuizGenerator - Flask Application
"""
from flask import Flask
from modules.routes.frontend import frontend_bp
from modules.routes.quiz import quiz_bp
from modules.routes.session import session_bp
from modules.routes.result import result_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(frontend_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(session_bp)
app.register_blueprint(result_bp)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
