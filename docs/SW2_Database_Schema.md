# SW2: Database Schema Design - QuizGenerator

**Last Updated**: 2026-04-13  
**Version**: 1.1  
**Status**: Implementation Phase  
**Author**: AI Assistant

---

## Table of Contents

- [Database Overview](#database-overview)
- [Entity-Relationship Diagram](#entity-relationship-diagram)
- [Table Definitions](#table-definitions)
- [Relationships & Constraints](#relationships--constraints)
- [Indexes & Performance](#indexes--performance)
- [Data Integrity Rules](#data-integrity-rules)
- [Normalization](#normalization)
- [Query Patterns](#query-patterns)

---

## Database Overview

### Technology
**SQLite** - Local file-based database, no server required

### Scope
Single-user application, local file storage

### Database File
`quizgenerator.db` (stored in app root or data folder)

### Design Principles
- Third Normal Form (3NF) for data integrity
- Minimal redundancy
- Clear relationships
- Support for all FR requirements

---

## Entity-Relationship Diagram

```
┌─────────────┐
│    Quiz     │
├─────────────┤
│ quiz_id (PK)│
│ total_q     │
│ uploaded_at │
└──────┬──────┘
       │ 1:N
       │
       ↓
┌──────────────────┐
│   Question       │
├──────────────────┤
│question_id (PK)  │
│quiz_id (FK)      │
│question_text     │
│option_a          │
│option_b          │
│option_c          │
│option_d          │
│correct_answer    │
└──────┬───────────┘
       │
       │ 1:N
       ↓
┌─────────────────────────┐
│   ExamSession           │
├─────────────────────────┤
│session_id (PK)          │
│quiz_id (FK)             │
│num_questions            │
│exam_duration            │
│created_at               │
│status                   │
└──────┬──────────────────┘
       │ 1:N
       ├─────────────────┐
       │                 │
       ↓                 ↓
┌──────────────┐  ┌────────────────┐
│ UserAnswer   │  │  ExamResult    │
├──────────────┤  ├────────────────┤
│answer_id (PK)│  │result_id (PK)  │
│session_id(FK)│  │session_id(FK)  │
│question_id   │  │score           │
│user_answer   │  │status          │
│answered_at   │  │correct_count   │
└──────────────┘  │incorrect_count │
                  │skipped_count   │
                  │submitted_at    │
                  │time_spent_sec  │
                  └────────────────┘
```

---

## Table Definitions

### Table 1: Quiz

**Purpose**: Store quiz/question bank metadata

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `quiz_id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique quiz identifier |
| `total_questions` | INTEGER | NOT NULL, > 0 | Total questions in this quiz |
| `uploaded_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Upload date/time |
| `name` | TEXT | UNIQUE | Quiz name (optional, from file) |

**SQL**:
```sql
CREATE TABLE quiz (
  quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
  total_questions INTEGER NOT NULL CHECK(total_questions > 0),
  uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name TEXT UNIQUE,
  UNIQUE(quiz_id)
);
```

---

### Table 2: Question

**Purpose**: Store individual questions and options

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `question_id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique question identifier |
| `quiz_id` | INTEGER | NOT NULL, FK → Quiz | Reference to quiz |
| `question_text` | TEXT | NOT NULL, MAX 2000 | Question content |
| `option_a` | TEXT | NOT NULL, MAX 500 | Option A text |
| `option_b` | TEXT | NOT NULL, MAX 500 | Option B text |
| `option_c` | TEXT | NOT NULL, MAX 500 | Option C text |
| `option_d` | TEXT | NOT NULL, MAX 500 | Option D text |
| `correct_answer` | CHAR(1) | NOT NULL, IN ('A','B','C','D') | Correct option |
| `difficulty` | INTEGER | 1-5 (optional) | Difficulty level |

**SQL**:
```sql
CREATE TABLE question (
  question_id INTEGER PRIMARY KEY AUTOINCREMENT,
  quiz_id INTEGER NOT NULL,
  question_text TEXT NOT NULL CHECK(LENGTH(question_text) <= 2000),
  option_a TEXT NOT NULL CHECK(LENGTH(option_a) <= 500),
  option_b TEXT NOT NULL CHECK(LENGTH(option_b) <= 500),
  option_c TEXT NOT NULL CHECK(LENGTH(option_c) <= 500),
  option_d TEXT NOT NULL CHECK(LENGTH(option_d) <= 500),
  correct_answer CHAR(1) NOT NULL CHECK(correct_answer IN ('A','B','C','D')),
  difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 5),
  FOREIGN KEY(quiz_id) REFERENCES quiz(quiz_id) ON DELETE CASCADE
);

CREATE INDEX idx_question_quiz ON question(quiz_id);
```

---

### Table 3: ExamSession

**Purpose**: Track quiz taking sessions

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `session_id` | TEXT | PRIMARY KEY | Unique session identifier (UUID) |
| `quiz_id` | INTEGER | NOT NULL, FK | Reference to quiz |
| `num_questions` | INTEGER | NOT NULL, 1-total | Number of selected questions |
| `exam_duration` | INTEGER | NOT NULL, ≥ 1 | Duration in minutes |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Session start time |
| `expires_at` | TIMESTAMP | NOT NULL | Session expiration (24h later) |
| `status` | VARCHAR(10) | NOT NULL, DEFAULT 'active' | 'active', 'submitted', 'expired' |

**SQL**:
```sql
CREATE TABLE exam_session (
  session_id TEXT PRIMARY KEY,
  quiz_id INTEGER NOT NULL,
  num_questions INTEGER NOT NULL CHECK(num_questions >= 1),
  exam_duration INTEGER NOT NULL CHECK(exam_duration >= 1),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NOT NULL,
  status VARCHAR(10) NOT NULL DEFAULT 'active' 
    CHECK(status IN ('active', 'submitted', 'expired')),
  FOREIGN KEY(quiz_id) REFERENCES quiz(quiz_id) ON DELETE CASCADE
);

CREATE INDEX idx_session_quiz ON exam_session(quiz_id);
CREATE INDEX idx_session_status ON exam_session(status);
```

---

### Table 4: UserAnswer

**Purpose**: Store user's answers for each question in a session

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `answer_id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique answer identifier |
| `session_id` | TEXT | NOT NULL, FK | Reference to exam session |
| `question_id` | INTEGER | NOT NULL | Question being answered |
| `user_answer` | CHAR(1) | NOT NULL, IN ('A','B','C','D','NULL') | User's selected option |
| `is_correct` | BOOLEAN | COMPUTED (after submission) | Auto-computed: user_answer == correct_answer |
| `answered_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Timestamp of submission |

**SQL**:
```sql
CREATE TABLE user_answer (
  answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  question_id INTEGER NOT NULL,
  user_answer CHAR(1) CHECK(user_answer IN ('A','B','C','D',NULL)),
  is_correct BOOLEAN,
  answered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(session_id) REFERENCES exam_session(session_id) ON DELETE CASCADE,
  FOREIGN KEY(question_id) REFERENCES question(question_id) ON DELETE RESTRICT,
  UNIQUE(session_id, question_id)
);

CREATE INDEX idx_answer_session ON user_answer(session_id);
CREATE INDEX idx_answer_correct ON user_answer(is_correct);
```

---

### Table 5: ExamResult

**Purpose**: Store final exam results and score

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `result_id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique result identifier |
| `session_id` | TEXT | NOT NULL, UNIQUE, FK | Reference to exam session |
| `quiz_id` | INTEGER | NOT NULL, FK | Reference to quiz |
| `score` | FLOAT | 0-100 | Percentage score |
| `correct_count` | INTEGER | ≥ 0 | Count of correct answers |
| `incorrect_count` | INTEGER | ≥ 0 | Count of incorrect answers |
| `skipped_count` | INTEGER | ≥ 0 | Count of skipped questions |
| `status` | VARCHAR(10) | IN ('PASS','FAIL') | Pass/Fail status (≥80% for PASS) |
| `submitted_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Submission time |
| `time_spent_seconds` | INTEGER | Optional | Seconds spent on exam |

**SQL**:
```sql
CREATE TABLE exam_result (
  result_id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL UNIQUE,
  quiz_id INTEGER NOT NULL,
  score FLOAT CHECK(score BETWEEN 0 AND 100),
  correct_count INTEGER DEFAULT 0,
  incorrect_count INTEGER DEFAULT 0,
  skipped_count INTEGER DEFAULT 0,
  status VARCHAR(10) CHECK(status IN ('PASS','FAIL')),
  submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  time_spent_seconds INTEGER,
  FOREIGN KEY(session_id) REFERENCES exam_session(session_id) ON DELETE CASCADE,
  FOREIGN KEY(quiz_id) REFERENCES quiz(quiz_id) ON DELETE RESTRICT
);

CREATE INDEX idx_result_quiz ON exam_result(quiz_id);
CREATE INDEX idx_result_status ON exam_result(status);
CREATE INDEX idx_result_submitted ON exam_result(submitted_at);
```

---

## Relationships & Constraints

### Relationship: Quiz → Question (1:N)
- **Cardinality**: One quiz has many questions
- **Constraint**: Cascade delete (delete quiz → delete questions)
- **Foreign Key**: `question.quiz_id → quiz.quiz_id`

### Relationship: Quiz → ExamSession (1:N)
- **Cardinality**: One quiz can have many sessions
- **Constraint**: Cascade delete
- **Foreign Key**: `exam_session.quiz_id → quiz.quiz_id`

### Relationship: ExamSession → UserAnswer (1:N)
- **Cardinality**: One session has many answers
- **Constraint**: Cascade delete
- **Foreign Key**: `user_answer.session_id → exam_session.session_id`

### Relationship: ExamSession → ExamResult (1:1)
- **Cardinality**: One session produces one result
- **Constraint**: Cascade delete
- **Foreign Key**: `exam_result.session_id → exam_session.session_id`
- **Unique**: One result per session

### Data Integrity Rules

#### Rule 1: Score Calculation
```
score = (correct_answers / total_questions) * 100
CONSTRAINT: correct_answers + incorrect_answers + skipped_answers = total_questions
```

#### Rule 2: Pass/Fail Status
```
IF score >= 50.00 THEN status = 'PASS'
IF score < 50.00 THEN status = 'FAIL'
```

#### Rule 3: Session Timeout
```
IF (NOW() - sess.created_at) > 24 hours
  THEN session.status = 'expired'
  AND auto-submit if results not yet submitted
```

#### Rule 4: Answer Validation
```
user_answer MUST BE NULL (unanswered) OR ('A'|'B'|'C'|'D')
is_correct MUST BE (user_answer == question.correct_answer)
```

#### Rule 5: Question Count Consistency
```
CONSTRAINT: num_questions <= total_questions_in_quiz
CONSTRAINT: COUNT(user_answers) <= num_questions
```

---

## Indexes & Performance

### Index: question_quiz
```sql
CREATE INDEX idx_question_quiz ON question(quiz_id);
```
**Purpose**: Fast retrieval of questions for a quiz
**Usage**: `SELECT * FROM question WHERE quiz_id = ?`

### Index: session_quiz
```sql
CREATE INDEX idx_session_quiz ON exam_session(quiz_id);
```
**Purpose**: Find all sessions for a quiz
**Usage**: `SELECT * FROM exam_session WHERE quiz_id = ?`

### Index: session_status
```sql
CREATE INDEX idx_session_status ON exam_session(status);
```
**Purpose**: Find active/expired sessions for cleanup
**Usage**: `SELECT * FROM exam_session WHERE status = 'expired'`

### Index: answer_session
```sql
CREATE INDEX idx_answer_session ON user_answer(session_id);
```
**Purpose**: Retrieve all answers for a session
**Usage**: `SELECT * FROM user_answer WHERE session_id = ?`

### Index: answer_correct
```sql
CREATE INDEX idx_answer_correct ON user_answer(is_correct);
```
**Purpose**: Analyze correct vs incorrect answers
**Usage**: Used in score calculation

### Index: result_quiz
```sql
CREATE INDEX idx_result_quiz ON exam_result(quiz_id);
```
**Purpose**: Get all results for a quiz
**Usage**: Progress analysis

### Index: result_status
```sql
CREATE INDEX idx_result_status ON exam_result(status);
```
**Purpose**: Filter results by pass/fail
**Usage**: Statistics queries

### Index: result_submitted
```sql
CREATE INDEX idx_result_submitted ON exam_result(submitted_at);
```
**Purpose**: Time-based queries
**Usage**: History, timeline analysis

---

## Normalization

### 1st Normal Form (1NF)
✅ **All columns contain atomic values** (no lists/repeating groups)
- Questions split into separate rows
- Options stored as individual columns (A, B, C, D)
- No array/list fields in any column

### 2nd Normal Form (2NF)
✅ **Meets 1NF and all non-key attributes fully dependent on primary key**
- No partial dependencies
- Foreign keys properly established
- Each table represents one entity

### 3rd Normal Form (3NF)
✅ **Meets 2NF and no transitive dependencies**
- Score is computed (not stored redundantly)
- Status is derived (not redundant)
- Minimal denormalization for performance

---

## Query Patterns

### Query 1: Get All Questions for a Quiz
```sql
SELECT * FROM question WHERE quiz_id = ? ORDER BY question_id;
```

### Query 2: Create Exam Session
```sql
INSERT INTO exam_session (session_id, quiz_id, num_questions, exam_duration, expires_at)
VALUES (?, ?, ?, ?, datetime('now', '+24 hours'));
```

### Query 3: Get Questions for Current Session (Random Selection)
```sql
SELECT q.* FROM question q
WHERE q.quiz_id = ? 
ORDER BY RANDOM() 
LIMIT ?;
```

### Query 4: Store User Answer
```sql
INSERT INTO user_answer (session_id, question_id, user_answer)
VALUES (?, ?, ?);
```

### Query 5: Calculate Score
```sql
SELECT 
  COUNT(CASE WHEN q.correct_answer = ua.user_answer THEN 1 END) as correct_count,
  COUNT(CASE WHEN q.correct_answer != ua.user_answer OR ua.user_answer IS NULL THEN 1 END) as incorrect_count,
  COUNT(CASE WHEN ua.user_answer IS NULL THEN 1 END) as skipped_count
FROM user_answer ua
JOIN question q ON ua.question_id = q.question_id
WHERE ua.session_id = ?;
```

### Query 6: Store Exam Result
```sql
INSERT INTO exam_result (session_id, quiz_id, score, correct_count, incorrect_count, skipped_count, status, time_spent_seconds, submitted_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
```

### Query 7: Get Result for Display
```sql
SELECT * FROM exam_result WHERE session_id = ?;
```

---

## Data Types Reference

| Type | Usage | Example |
|------|-------|---------|
| INTEGER | IDs, Counts, Minutes | quiz_id=1, num_questions=20 |
| TEXT | Questions, Options | "What is 2+2?" |
| CHAR(1) | Single letter options | 'A', 'B', 'C', 'D' |
| DECIMAL(5,2) | Score percentage | 75.50 |
| TIMESTAMP | Dates & Times | 2026-03-15 10:30:00 |
| BOOLEAN | True/False | is_correct=TRUE |

---

## Database Initialization

### Create Database
```python
# In Flask app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizgenerator.db'
db = SQLAlchemy(app)
db.create_all()  # Creates all tables
```

### Insert Sample Data
```sql
-- Insert sample quiz
INSERT INTO quiz (total_questions, name) 
VALUES (50, 'Sample Quiz 1');

-- Insert sample question
INSERT INTO question (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer)
VALUES (1, 'What is 2+2?', '3', '4', '5', '6', 'B');
```

---

## References

- See `docs/SW1_Requirement_Analysis.md` for data specifications (FR-7)
- See `docs/SW2_System_Architecture.md` for architecture context
- See `docs/SW2_API_Design.md` for API data contracts
