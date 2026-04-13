# SW2: System Architecture Design - QuizGenerator

**Last Updated**: 2026-04-13  
**Version**: 1.2  
**Status**: Implementation (Session→Exam Refactor, QuizStats Added)

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [High-Level Architecture](#high-level-architecture)
- [Component Diagram](#component-diagram)
- [Layered Architecture](#layered-architecture)
- [Module Breakdown](#module-breakdown)
- [Data Flow](#data-flow)
- [Technology Stack Integration](#technology-stack-integration)
- [Deployment Architecture](#deployment-architecture)

---

## Architecture Overview

### Architecture Style
**Layered (N-Tier) Architecture** with client-server model

### Design Pattern
Model-View-Controller (MVC) adapted for Flask

### Key Principles
- Separation of Concerns (each layer has distinct responsibility)
- Single Responsibility Principle
- DRY (Don't Repeat Yourself)
- Modularity and maintainability

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│           Presentation Layer                     │
│  (HTML/CSS/JavaScript Frontend)                 │
└─────────────────┬───────────────────────────────┘
                  │ HTTP/AJAX
                  ↓
┌─────────────────────────────────────────────────┐
│        Application Layer (Flask)                 │
│  - Routes & Controllers                          │
│  - Request/Response handling                     │
│  - Session management                           │
└──────┬──────────────────────────────┬────────────┘
       │                              │
       ↓                              ↓
┌──────────────────┐        ┌─────────────────────┐
│  Business Layer  │        │   Data Layer        │
│  - Quiz Service  │        │  - Database Access  │
│  - Exam Service  │        │  - File Operations  │
│  - Score Engine  │        │  - Data Validation  │
└──────┬───────────┘        └─────────┬───────────┘
       │                              │
       └──────────────┬───────────────┘
                      ↓
        ┌─────────────────────────────┐
        │   Database Layer (SQLite)   │
        │   File Storage (Local FS)   │
        └─────────────────────────────┘
```

---

## Component Diagram

### Core Components

```
QuizGenerator Application
├── Frontend Layer
│   ├── Upload Page (upload.html) - Default landing page
│   ├── Quiz List Page (list-quizzes.html) - Table view of all quizzes
│   ├── Exam Page (exam.html / exam-do route)
│   ├── Quiz Stats Page (quiz-stats.html) - Statistics and results
│   └── Results Page (results.html) - Detailed answer review
│
├── Application Layer (Flask)
│   ├── app.py (Main Flask app)
│   ├── Routes
│   │   ├── GET / → Upload page
│   │   ├── POST /api/quizzes → Upload quiz (Excel)
│   │   ├── GET /list-quizzes → Quiz list page
│   │   ├── GET /exam-do → Exam page (prepare & take)
│   │   ├── GET /quiz-stats → Statistics & results
│   │   ├── GET /results → Detailed answer review
│   │   └── API Routes (see SW2_API_Design.md)
│   └── Utilities
│       ├── File handler
│       └── Session manager
│
├── Business Logic Layer
│   ├── QuizService
│   │   ├── parse_excel()
│   │   ├── store_quiz()
│   │   └── create_session()
│   ├── ExamService
│   │   ├── get_questions()
│   │   ├── shuffle_options()
│   │   └── submit_answers()
│   └── ScoringEngine
│       ├── calculate_score()
│       └── determine_status()
│
├── Data Layer (models.py)
│   ├── Quiz (model)
│   ├── Question (model)
│   ├── ExamSession (model)
│   ├── UserAnswer (model)
│   └── ExamResult (model)
│
└── Database Layer
    └── SQLite Database
        ├── quiz table
        ├── question table
        ├── exam_session table
        ├── user_answer table
        └── exam_result table
```

---

## Layered Architecture

### Layer 1: Presentation Layer
**Responsibility**: UI and user interaction

**Components**:
- HTML Templates (Jinja2)
- CSS Styling (Static folder)
- JavaScript (Client-side logic)
- Form validation
- Timer display
- Results visualization

**Interfaces**:
- HTTP requests to Flask routes
- Form submissions
- AJAX calls for dynamic updates

---

### Layer 2: Application Layer (Flask)
**Responsibility**: Request handling, routing, session management

**Components**:
- `app.py`: Flask app initialization
- Routes (endpoints):
  - `GET /` → Upload page (main landing)
  - `POST /api/quizzes` → Handle Excel file upload (API)
  - `GET /list-quizzes` → Quiz listing page
  - `GET /exam` → Exam page
  - `GET /results` → Results page
- Middleware:
  - Error handling
  - Request validation
  - CORS (if needed)

**Key Functions**:
- Route mapping
- Request parsing
- Response formatting
- HTTP status codes

---

### Layer 3: Business Logic Layer
**Responsibility**: Core application logic

**Services**:

#### 3.1 QuizService
```
Methods:
- parse_excel(file_path) → list of questions
- validate_questions(questions) → bool, error messages
- store_quiz(questions) → quiz_id
- get_quiz(quiz_id) → quiz object
- list_quizzes() → list of quizzes
```

#### 3.2 ExamService
```
Methods:
- create_session(quiz_id, num_questions, duration) → session_id, questions
- get_session(session_id) → session object
- select_random_questions(quiz_id, num) → list of question objects
- shuffle_options(question) → shuffled question
- submit_answers(session_id, answers) → bool
- get_answers(session_id) → all user answers
- timeout_session(session_id) → force submit
```

#### 3.3 ScoringEngine
```
Methods:
- calculate_score(session_id) → score (decimal)
- count_correct(session_id) → int
- determine_status(score) → 'PASS' or 'FAIL'
- generate_result(session_id) → result object
```

---

### Layer 4: Data Layer
**Responsibility**: Data access and persistence

**Database Access Methods**:
- Create (INSERT)
- Read (SELECT)
- Update (UPDATE)
- Delete (DELETE)

**Models** (SQLAlchemy ORM):
- Quiz
- Question
- ExamSession
- UserAnswer
- ExamResult

**File Operations**:
- Upload Excel file handling
- File validation
- Temporary file management

---

### Layer 5: Database Layer
**Responsibility**: Data persistence

**Technology**: SQLite (local file)

**Schema**:
- 5 main tables (see SW2_Database_Schema.md)
- Relationships and foreign keys
- Indexes for performance

---

## Module Breakdown

### Module 1: Core Application (app.py)
```python
Structure:
- Flask app initialization
- Configuration loading
- Blueprint registration
- Error handlers
- Context processors
```

### Module 2: Routes (routes.py or multiple blueprint files)
```python
Structure:
- /upload router
- /config router
- /exam router
- /results router
- Error handlers
```

### Module 3: Models (models.py)
```python
Structure:
- Database models
- Relationships
- Methods for ORM
```

### Module 4: Services (services/)
```
services/
├── quiz_service.py
├── exam_service.py
└── scoring_engine.py
```

### Module 5: Utilities (utils/)
```
utils/
├── file_handler.py
├── validators.py
├── session_manager.py
└── decorators.py
```

### Module 6: Templates (templates/)
```
templates/
├── base.html
├── index.html
├── upload.html
├── config.html
├── exam.html
└── results.html
```

### Module 7: Static Files (static/)
```
static/
├── css/
│   └── style.css
├── js/
│   ├── timer.js
│   ├── validation.js
│   └── exam.js
└── images/
```

---

## Data Flow

### Flow 1: Quiz Upload & Storage
```
1. User selects Excel file
2. Frontend sends multipart/form-data POST to /upload
3. Flask receives file → FileHandler validates
4. QuizService.parse_excel() extracts data
5. Validation checks (required columns, correct answer format)
6. Store in database via models
7. Return quiz_id to frontend
8. Display success message
```

### Flow 2: Quiz Configuration & Session Creation
```
1. User selects quiz, enters num_questions, duration
2. Frontend sends POST to /config with parameters
3. Flask validates inputs (1 ≤ num ≤ total, duration ≥ 1)
4. ExamService.create_session() generates session_id
5. ExamService.select_random_questions() picks N questions
6. ExamService.shuffle_options() for each question
7. Store session in database
8. Return session with questions to frontend
9. Display exam interface
```

### Flow 3: Answer Submission & Scoring
```
1. User submits answers (all at once or per question)
2. Frontend sends POST /submit with {session_id, answers}
3. Flask stores answers in user_answer table
4. Request session timeout check
5. ScoringEngine.calculate_score() computes result
6. ScoringEngine.determine_status() assigns PASS/FAIL
7. Store result in exam_result table
8. Return results to frontend
9. Display results page
```

### Flow 4: Timer Auto-Submission
```
1. Timer reaches 0:00 on frontend
2. Frontend sends POST /submit?auto=true
3. Flask marks session as auto-submitted
4. ScoringEngine treats unanswered as incorrect
5. Calculate score and display results
```

---

## Technology Stack Integration

### Backend Integration
```
Flask Application
├── Receives HTTP requests from Frontend
├── Routes to appropriate controllers
├── Calls business logic services
├── Uses ORM to access database
├── Returns JSON/HTML responses
└── Manages sessions and state
```

### Database Integration
```
SQLAlchemy ORM
├── Models define table structure
├── Methods provide CRUD operations
├── Relationships model foreign keys
├── Query builder for complex searches
└── Transaction management
```

### File Storage Integration
```
Local Filesystem
├── Accepts uploaded Excel files
├── Validates file format
├── Parses content
├── Stores metadata in database
└── Optional: Archive old files
```

### Frontend Integration
```
HTML/CSS/JavaScript
├── Form submission to Flask routes
├── Timer management (setTimeout)
├── AJAX for dynamic updates
├── Event handling for user actions
└── Results display and formatting
```

---

## Deployment Architecture

### Development Environment
```
Local Machine
├── Flask App (localhost:5000)
├── SQLite Database (local file)
├── File uploads (temp folder)
└── Browser (Chrome/Firefox)
```

### Production Environment
```
Server/Cloud
├── Flask App (WSGI server like Gunicorn)
├── SQLite Database (persistent storage)
├── File uploads (secure folder)
├── Reverse proxy (Nginx)
├── SSL/TLS encryption
└── Backup strategy
```

---

## Quality Attributes

### Performance
- Page load: < 2 seconds
- Score calculation: < 1 second
- Database queries optimized with indexes

### Reliability
- Error handling at all layers
- Data persistence validation
- Session recovery capability
- Graceful degradation

### Security
- Input validation at frontend and backend
- SQL injection prevention (ORM)
- CSRF protection (Flask-WTF)
- File upload validation
- Secure file storage

### Maintainability
- Clear separation of concerns
- Consistent naming conventions
- Code comments and docstrings
- Modular design for easy updates

### Scalability
- Currently designed for single user
- Stateless routes (can scale if needed)
- Database can handle growth
- File storage can expand

---

## Architecture Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| Layered Architecture | Clear separation of concerns, easy to test and maintain |
| Flask Framework | Lightweight, flexible, good for MVP |
| SQLite Database | No server setup needed, suitable for local app |
| MVC Pattern | Familiar pattern, reduces complexity |
| ORM (SQLAlchemy) | Type safety, prevents SQL injection, reduces boilerplate |
| Local File Storage | Simplicity, no cloud dependencies for MVP |
| Client-side Timer | Responsive UX, less server load |

---

## References

- See `docs/SW1_Requirement_Analysis.md` for functional requirements
- See `docs/SW2_Database_Schema.md` for database design
- See `docs/SW2_API_Design.md` for API endpoints
