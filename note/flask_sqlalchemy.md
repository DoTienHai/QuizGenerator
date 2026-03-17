# Flask-SQLAlchemy: Hiểu Rõ ORM & Database

**Ngày tạo**: 2026-03-17  
**Mục đích**: Giải thích Flask-SQLAlchemy, SQLAlchemy ORM, và cách dùng trong QuizGenerator

---

## Mục Lục
- [SQLAlchemy là gì?](#sqlalchemy-là-gì)
- [Flask-SQLAlchemy là gì?](#flask-sqlalchemy-là-gì)
- [ORM (Object-Relational Mapping)](#orm-object-relational-mapping)
- [Raw SQL vs ORM](#raw-sql-vs-orm)
- [Architecture & Flow](#architecture--flow)
- [Key Concepts](#key-concepts)
- [Cách Dùng Flask-SQLAlchemy](#cách-dùng-flask-sqlalchemy)
- [Database Session](#database-session)
- [Queries & Filtering](#queries--filtering)
- [Relationships](#relationships)
- [Flask-SQLAlchemy Configuration Keys](#flask-sqlalchemy-configuration-keys)
- [Best Practices](#best-practices)

---

## SQLAlchemy là gì?

### Định Nghĩa

**SQLAlchemy** = ORM (Object-Relational Mapping) Library cho Python

Tạm dịch: Công cụ giúp viết Python objects thay vì SQL strings, tự động convert giữa Python ↔ Database

---

### Ví Dụ: SQLAlchemy vs Raw SQL

#### ❌ Raw SQL (Khó)
```python
import sqlite3

conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Insert - phải viết SQL string
cursor.execute(
    "INSERT INTO quiz (name, total_questions) VALUES (?, ?)",
    ('My Quiz', 50)
)
conn.commit()

# Query - trả về tuple, phải biết index
cursor.execute("SELECT * FROM quiz WHERE quiz_id = ?", (1,))
row = cursor.fetchone()
quiz_id = row[0]
name = row[1]
```

#### ✅ SQLAlchemy (Dễ)
```python
from sqlalchemy.orm import sessionmaker
from models import Quiz

# Insert - Python object
quiz = Quiz(name='My Quiz', total_questions=50)
session.add(quiz)
session.commit()

# Query - trả về object
quiz = session.query(Quiz).filter_by(quiz_id=1).first()
print(quiz.name)  # Direct attribute access
```

---

### Ưu & Nhược Điểm

#### ✅ Ưu Điểm
- Type Safety: Column(Integer), Column(String) validation
- Relationships: Tự động join via foreign keys
- Readability: Python objects dễ hiểu
- Portability: Dễ switch databases
- Security: SQL injection protection

#### ❌ Nhược Điểm
- Performance overhead cho complex queries
- Learning curve (cần hiểu ORM)
- Magic behaviors (khó debug)

---

## Flask-SQLAlchemy là gì?

### Định Nghĩa

**Flask-SQLAlchemy** = Extension kết hợp SQLAlchemy ORM với Flask

```
Flask Framework (web routing)
           ↓
Flask-SQLAlchemy (bridge)
           ↓
SQLAlchemy ORM (models, sessions)
           ↓
Database Driver (sqlite3, psycopg2)
           ↓
Actual Database (.db file)
```

---

### Tại Sao Cần Flask-SQLAlchemy?

**Không Flask-SQLAlchemy:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///quiz.db')
Session = sessionmaker(bind=engine)
session = Session()
# Phải manual setup, manual close
```

**Với Flask-SQLAlchemy:**
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # ← One line!
# Automatic session management, app context handling
```

---

## ORM (Object-Relational Mapping)

### Concept

ORM = Bridge between Python Objects & Database Tables

```
Python Class          Database Table
─────────────────────────────────────
Quiz                  quiz
  ├─ quiz_id          ├─ quiz_id INT PRIMARY KEY
  ├─ name             ├─ name VARCHAR(255)
  └─ total_questions  └─ total_questions INTEGER

Automatic Conversion:
  quiz.name (String) → "name" TEXT column
  quiz.quiz_id (Integer) → "quiz_id" INT column
```

---

### Mapping Example

#### Python Class → Database Table

```python
class Quiz(db.Model):
    __tablename__ = 'quiz'
    
    quiz_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    total_questions = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

# ↓ Automatically Creates

CREATE TABLE quiz (
  quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) UNIQUE,
  total_questions INTEGER NOT NULL,
  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Raw SQL vs ORM

### Comparison

| Operation | Raw SQL | ORM |
|-----------|---------|-----|
| **INSERT** | `cursor.execute("INSERT ...")` | `db.session.add(object)` |
| **SELECT** | `cursor.execute("SELECT ...")` | `Model.query.get(id)` |
| **UPDATE** | `cursor.execute("UPDATE ...")` | `object.field = value; db.session.commit()` |
| **DELETE** | `cursor.execute("DELETE ...")` | `db.session.delete(object)` |
| **JOIN** | Hand-written SQL | Auto via `relationship()` |

---

## Architecture & Flow

### How Flask-SQLAlchemy Works

```
1. DEFINE MODEL
   ├─ class Quiz(db.Model):
   │   ├─ quiz_id = db.Column(db.Integer, primary_key=True)
   │   └─ name = db.Column(db.String(255))
   └─ SQLAlchemy introspects schema

2. INITIALIZE APP
   ├─ app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
   ├─ db.init_app(app)
   └─ Connects Flask to database

3. CREATE TABLES
   ├─ with app.app_context():
   │   └─ db.create_all()
   └─ Executes: CREATE TABLE quiz (...)

4. USE IN ROUTES
   ├─ quiz = Quiz(name='Test', total_questions=10)
   ├─ db.session.add(quiz)
   ├─ db.session.commit()
   └─ Executes: INSERT INTO quiz ...

5. QUERY DATA
   ├─ quiz = Quiz.query.get(1)
   ├─ for q in quiz.questions:
   └─ Auto-executes complex JOINs
```

---

## Key Concepts

### 1. db = SQLAlchemy()

Global instance - used to define all models

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Provides:
db.Model              # Base class for models
db.Column             # Define table columns
db.Integer, String    # Data types
db.ForeignKey         # Foreign key reference
db.relationship       # One-to-many, many-to-one
db.session            # Database session (add, commit)
db.create_all()       # Create all tables
```

---

### 2. db.Column (Table Columns)

Syntax: `db.Column(DataType, constraints, options)`

Examples:
```python
# Primary Key
quiz_id = db.Column(db.Integer, primary_key=True)

# String with length limit
name = db.Column(db.String(255), unique=True)

# Required field (NOT NULL)
total_questions = db.Column(db.Integer, nullable=False)

# With default value
created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

Data Types:
- `db.Integer` → INTEGER
- `db.String(255)` → VARCHAR(255)
- `db.Text` → TEXT (unlimited)
- `db.Boolean` → BOOLEAN
- `db.DateTime` → TIMESTAMP
- `db.Float` → FLOAT

---

### 3. db.ForeignKey (Relationships)

Link between tables

```python
class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey('quiz.quiz_id', ondelete='CASCADE'),
        nullable=False
    )
    # If quiz deleted → auto-delete questions
```

---

### 4. db.relationship (Python Navigation)

Define how to access related objects

```python
class Quiz(db.Model):
    questions = db.relationship(
        'Question',
        back_populates='quiz',
        cascade='all, delete-orphan'
    )

class Question(db.Model):
    quiz = db.relationship('Quiz', back_populates='questions')

# Usage:
quiz = Quiz.query.get(1)
for question in quiz.questions:  # ← Auto join!
    print(question.question_text)
```

---

### 5. db.session (Database Session)

Transaction management - add, commit, rollback

```python
# ADD (stage for insert)
quiz = Quiz(name='Test', total_questions=10)
db.session.add(quiz)

# COMMIT (execute INSERT)
db.session.commit()

# ROLLBACK (undo changes)
try:
    db.session.commit()
except:
    db.session.rollback()

# DELETE
db.session.delete(quiz)
db.session.commit()
```

---

## Cách Dùng Flask-SQLAlchemy

### Step 1: Install

```bash
pip install Flask-SQLAlchemy
```

---

### Step 2: Create models Package

**modules/models/__init__.py:**
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # ← Global instance
```

---

### Step 3: Define Models (Separate Files)

**modules/models/quiz.py:**
```python
from modules.models import db
from datetime import datetime

class Quiz(db.Model):
    __tablename__ = 'quiz'
    
    quiz_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    total_questions = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    questions = db.relationship('Question', back_populates='quiz')
```

**modules/models/question.py:**
```python
from modules.models import db

class Question(db.Model):
    __tablename__ = 'question'
    
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey('quiz.quiz_id', ondelete='CASCADE'),
        nullable=False
    )
    question_text = db.Column(db.String(2000), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)
    
    quiz = db.relationship('Quiz', back_populates='questions')
```

---

### Step 4: Setup in Flask App

**app.py:**
```python
from flask import Flask
from config import DevelopmentConfig
from modules.models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize db with app
db.init_app(app)

# Create tables on startup
with app.app_context():
    db.create_all()

# Register blueprints
from modules.routes.quiz import quiz_bp
app.register_blueprint(quiz_bp)

if __name__ == '__main__':
    app.run()
```

**config.py:**
```python
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_generator.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Log SQL queries
```

---

### Step 5: Use in Routes

**modules/routes/quiz.py:**
```python
from flask import Blueprint, request, jsonify
from modules.models.quiz import Quiz
from modules.models import db

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api')

@quiz_bp.route('/quizzes', methods=['POST'])
def create_quiz():
    data = request.get_json()
    
    quiz = Quiz(
        name=data['name'],
        total_questions=data['total_questions']
    )
    
    db.session.add(quiz)
    db.session.commit()
    
    return {'quiz_id': quiz.quiz_id}, 201

@quiz_bp.route('/quizzes/<int:quiz_id>')
def get_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    
    if not quiz:
        return {'error': 'Not found'}, 404
    
    return {
        'quiz_id': quiz.quiz_id,
        'name': quiz.name,
        'questions_count': len(quiz.questions)
    }
```

---

## Database Session

### What is Session?

Session = Connection + Transaction context

```
Session mở (connection tạo)
  ↓
Execute queries
  ↓
db.session.commit() ← Save changes
  ↓
Session đóng (connection đóng)
```

---

### Flask Auto-manages Session

In Flask-SQLAlchemy:
```python
@app.route('/api/quizzes')
def list_quizzes():
    # Session automatically opened
    quizzes = Quiz.query.all()
    return {...}
    # Session automatically closed after request
```

---

## Queries & Filtering

### Basic Queries

```python
# Get all
all_quizzes = Quiz.query.all()

# Get by primary key
quiz = Quiz.query.get(1)

# Get first matching
quiz = Quiz.query.filter_by(name='Test').first()

# Get all matching
quizzes = Quiz.query.filter_by(name='Test').all()

# Filter with condition
quizzes = Quiz.query.filter(Quiz.total_questions > 50).all()

# Like (text search)
quizzes = Quiz.query.filter(Quiz.name.like('%Python%')).all()

# Order by
quizzes = Quiz.query.order_by(Quiz.uploaded_at.desc()).all()

# Pagination
quizzes = Quiz.query.limit(10).offset(0).all()

# Count
count = Quiz.query.count()
```

---

## Relationships

### One-to-Many (Quiz → Questions)

```python
class Quiz(db.Model):
    questions = db.relationship('Question', back_populates='quiz')

class Question(db.Model):
    quiz = db.relationship('Quiz', back_populates='questions')

# Usage:
quiz = Quiz.query.get(1)
for question in quiz.questions:  # ← Auto join
    print(question.question_text)
```

---

### One-to-One (ExamSession → ExamResult)

```python
class ExamSession(db.Model):
    exam_result = db.relationship(
        'ExamResult',
        back_populates='session',
        uselist=False  # ← One-to-one!
    )

class ExamResult(db.Model):
    session = db.relationship('ExamSession', back_populates='exam_result')

# Usage:
session = ExamSession.query.get('uuid-123')
score = session.exam_result.score  # ← Single object
```

---

## Best Practices

### 1. Always Set Constraints

```python
# ✅ GOOD
name = db.Column(db.String(255), unique=True, nullable=False)

# ❌ BAD
name = db.Column(db.String)
```

---

### 2. Use Bidirectional Relationships

```python
# ✅ GOOD
class Quiz(db.Model):
    questions = db.relationship('Question', back_populates='quiz')

class Question(db.Model):
    quiz = db.relationship('Quiz', back_populates='questions')

# ❌ BAD
class Quiz(db.Model):
    questions = db.relationship('Question')
    # Can't access question.quiz
```

---

### 3. Check for None

```python
# ✅ GOOD
quiz = Quiz.query.get(1)
if quiz:
    print(quiz.name)

# ❌ BAD
quiz = Quiz.query.get(999)
print(quiz.name)  # ← Crash if None!
```

---

### 4. Error Handling

```python
# ✅ GOOD
try:
    db.session.commit()
except Exception as e:
    db.session.rollback()
    print(f'Error: {e}')

# ❌ BAD
db.session.commit()  # ← Might fail silently
```

---

## Flask-SQLAlchemy Configuration Keys

### Where do Config Keys Come From?

All configuration keywords in `config.py` are **standard keys from Flask and Flask-SQLAlchemy**, not custom made:

| Keyword | Source | Purpose |
|---------|--------|---------|
| **SQLALCHEMY_TRACK_MODIFICATIONS** | Flask-SQLAlchemy | Disable ORM object change tracking |
| **SQLALCHEMY_RECORD_QUERIES** | Flask-SQLAlchemy | Record all SQL queries for debugging |
| **SQLALCHEMY_DATABASE_URI** | Flask-SQLAlchemy | Database connection string |
| **SQLALCHEMY_ECHO** | Flask-SQLAlchemy | Print SQL queries to console |
| **PERMANENT_SESSION_LIFETIME** | Flask | Session timeout duration |
| **SESSION_COOKIE_SECURE** | Flask/Werkzeug | HTTPS-only cookies |
| **SESSION_COOKIE_HTTPONLY** | Flask/Werkzeug | Prevent JavaScript access to cookies |
| **SESSION_COOKIE_SAMESITE** | Flask/Werkzeug | CSRF protection |
| **MAX_CONTENT_LENGTH** | Werkzeug | Max file upload size |
| **DEBUG** | Flask | Debug mode (auto-reload) |
| **SECRET_KEY** | Flask | Session encryption key |

---

### How Flask Reads Config Keys

```python
# config.py
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_generator.db'
    SQLALCHEMY_ECHO = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SECRET_KEY = 'dev-key'

# app.py
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)  # ← Flask reads all keys

# Flask automatically recognizes standard keys and applies them
# Non-standard keys are ignored (don't create custom ones here)
```

---

### How to Find & Read Config Keys

#### **Option 1: Official Documentation** (Recommended)
- Flask: https://flask.palletsprojects.com/config/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- Werkzeug: https://werkzeug.palletsprojects.com/

#### **Option 2: VS Code Auto-complete**
```python
# In app.py, type: app.config['S
# IDE shows all available keys starting with 'S':
# - SECRET_KEY
# - SESSION_COOKIE_SECURE
# - SQLALCHEMY_DATABASE_URI
# - SQLALCHEMY_ECHO
```

#### **Option 3: Print All Loaded Config**
```python
# Run in Python shell:
python -c "from app import app; print(dict(app.config))"

# Output:
# DEBUG: True
# TESTING: False
# SQLALCHEMY_DATABASE_URI: sqlite:///quiz_generator.db
# SQLALCHEMY_ECHO: True
# ...
```

#### **Option 4: Check Source Code**
- Flask source: https://github.com/pallets/flask/blob/main/src/flask/config.py
- Flask-SQLAlchemy: https://github.com/pallets-eco/flask-sqlalchemy

---

### Important Rules

```python
# ✅ CORRECT: Use standard Flask/Flask-SQLAlchemy keys
SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_generator.db'
SECRET_KEY = 'my-key'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# ❌ WRONG: Don't create custom config keys in Config class
CUSTOM_API_KEY = 'xyz'  # ← Flask ignores these!
MY_SETTING = 'abc'      # ← Flask ignores these!

# ✅ IF YOU NEED CUSTOM SETTINGS: Store separately
CUSTOM_SETTINGS = {
    'api_key': 'xyz',
    'email_sender': 'noreply@quiz.com'
}
```

---

## Summary

**Config Keys:**
- All keys are **standard from Flask/Flask-SQLAlchemy/Werkzeug**
- Flask automatically recognizes them and applies
- Custom keys are ignored
- Always check official docs for available keys
- Use IDE auto-complete or documentation to discover keys

**For QuizGenerator:**
- `SQLALCHEMY_DATABASE_URI` = SQLite file path
- `SQLALCHEMY_ECHO` = Show SQL queries for debugging
- `SECRET_KEY` = Session encryption (random string)
- `MAX_CONTENT_LENGTH` = File upload limit (16 MB)
- `DEBUG` = Auto-reload during development

---

## Summary

```
SQLAlchemy = ORM Library
  ↓
Flask-SQLAlchemy = Flask integration
  ↓
Define Models (Quiz, Question, etc.)
  ↓
Map to Database Tables (CREATE TABLE)
  ↓
Use in Routes (CRUD operations)
```

**Key Points:**
- ✅ ORM = Python objects ↔ Database rows (automatic)
- ✅ Flask-SQLAlchemy = SQLAlchemy + Flask integration
- ✅ db.Model = Base class for all models
- ✅ db.session = Transaction management
- ✅ db.relationship = Auto-join via FK
- ✅ Queries = Model.query.filter().all()

**For QuizGenerator:**
- 5 models: Quiz, Question, ExamSession, UserAnswer, ExamResult
- UUID for session_id (security)
- Relationships connect models (1:N, 1:1)
- db.session.add() + commit() = INSERT/UPDATE
