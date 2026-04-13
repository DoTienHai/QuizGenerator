# SW1: Requirement Analysis - QuizGenerator

**Last Updated**: 2026-03-15  
**Version**: 2.0  
**Status**: Final  
**Author**: AI Assistant

## Overview

QuizGenerator is a web application that allows a user to create, configure, and take randomized quizzes from Excel-based question banks. The system automates quiz creation from Excel templates, randomizes question selection and options, and provides immediate scoring.

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Business Requirements](#business-requirements)
- [User Requirements & Personas](#user-requirements--personas)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [System Constraints](#system-constraints)
- [Acceptance Criteria](#acceptance-criteria)
- [Use Cases](#use-cases)
- [Data Input & Output Specification](#data-input--output-specification)
- [Glossary](#glossary)

---

## Executive Summary

### 1. Purpose
Automate quiz creation from Excel templates, randomize question selection and options, and provide automated scoring with detailed results analysis.

### 2. Target Users

**Primary User:**
- **Quiz Creator & Taker**: Single user who uploads Excel question banks, configures quiz parameters, and takes the randomized quizzes to test/practice

### 3. Problem Statement
Manual quiz/exam creation is time-consuming. User needs a tool that:
- Eliminates manual question formatting from Excel
- Ensures fairness through randomized question selection
- Provides instant scoring for self-testing/practice
- Supports different difficulty levels through configurable exam parameters

### 4. Business Goals

| Goal | Metric |
|------|--------|
| Reduce quiz creation time | 10 mins → 2 mins per quiz |
| Enable quick self-testing | Create randomized exam within 5 minutes |
| Improve self-assessment | Instant scoring for learning feedback |

### 5. Success Metrics

- **Adoption**: User finds app useful and uses regularly
- **Performance**: Quiz creation + first exam completion ≤ 10 minutes
- **Quality**: Score accuracy 100%, no calculation errors
- **Usability**: Clear UI, no confusion on usage flow

---

## Business Requirements

### BR-1: Quiz Creation Automation
The system must accept Excel files containing quiz questions, parse them automatically, and store them for immediate use.

### BR-2: Fair Assessment
All quizzes must ensure fairness through:
- Random question selection (no predetermined patterns)
- Random option shuffling (prevent answer key patterns)
- Consistent scoring algorithm

### BR-3: Immediate Feedback
User must receive score and results immediately upon quiz submission.

### BR-4: Data Persistence & Security
All quiz data, sessions, and results must be:
- Securely stored in database
- Protected from unauthorized access
- Compliant with education data privacy standards

### BR-5: Flexible Exam Configuration
User can configure quiz parameters (number of questions, time limit) independently for each exam attempt to test different difficulty levels.

### BR-6: Session Management
Quiz sessions must be tracked with:
- Automatic timeout after 24 hours for abandoned sessions
- Recovery capability if browser reloads during exam
- Clear session history

---

## User Requirements & Personas

### User Persona: Self-Study Learner

**Profile:**
- Alex, 28, preparing for professional certification exam
- Comfortable with technology
- Has a collection of practice questions from study materials
- Values self-paced learning and immediate feedback

**Goals:**
1. Convert personal question banks into randomized practice exams
2. Self-test with different difficulty levels to track progress
3. Get instant score and performance feedback
4. Practice without manual question shuffling

**Workflow:**
1. Prepare Excel file with practice questions
2. Upload file to system
3. System stores and organizes questions
4. Configure and take practice exam (select num_questions, duration)
5. View score and compare with previous attempts
6. Retake with different settings to practice weak areas

**Motivations:**
- Wants fair, randomized practice without pattern recognition
- Needs quick feedback loop for learning
- Values privacy (personal study tool)
- Prefers local/self-hosted solution

**Pain Points:**
- Manually shuffling questions is tedious
- Can't easily create different difficulty levels
- Manual scoring is error-prone
- Difficult to track progress across attempts

---

## Functional Requirements

### FR-1: Excel File Upload
**Description**: User can upload Excel files containing practice questions

**Specifications**:
- **File Format**: `.xlsx`, `.xls`
- **Maximum Size**: 10 MB
- **Required Columns**: 
  - `Question` (text)
  - `Option_A`, `Option_B`, `Option_C`, `Option_D` (text)
  - `Correct_Answer` (A/B/C/D)
- **Processing**: Automatic parsing and validation
- **Error Handling**: Detailed error messages for missing/invalid data
- **Output**: Quiz ID assigned, questions stored in database

**Acceptance Criteria:**
- Valid Excel file (all required columns) → Success message, questions stored
- Missing required column → Error: "Missing column: [name]"
- Invalid correct answer → Error: "Question X: Invalid correct answer value"
- File > 10 MB → Error: "File size exceeds 10 MB limit"

### FR-2: Quiz Configuration
**Description**: User configures exam parameters before taking exam

**Parameters**:

#### 2.1 Number of Questions (`num_questions`)
- **Type**: Integer
- **Range**: 1 to total available questions
- **Validation**: `1 ≤ num_questions ≤ total_questions_in_file`
- **UI**: Dropdown with available options or numeric input
- **Feedback**: "You have X questions available"

#### 2.2 Exam Duration (`exam_duration`)
- **Type**: Integer (minutes)
- **Range**: ≥ 1 minute
- **Validation**: `exam_duration ≥ 1`
- **UI**: Numeric input field
- **Feedback**: "Time limit: X minutes"

**Processing**:
- Validate parameters
- Create quiz session with unique session ID
- Select random questions
- Shuffle options for each question
- Display quiz to user

### FR-3: Random Question Selection
**Description**: Select N random questions from uploaded bank

**Algorithm**:
1. Retrieve all questions for quiz
2. Use random.sample() to select N unique questions
3. Store selected question IDs in session
4. Ensure no duplicates

**Acceptance Criteria**:
- Selected count = num_questions ✓
- All selected questions exist ✓
- Each question selected exactly once ✓
- Distribution is statistically random (no patterns) ✓

### FR-4: Option Shuffling
**Description**: Randomize answer option positions to prevent pattern recognition

**Algorithm**:
1. For each question, get options (A, B, C, D)
2. Record original correct answer
3. Shuffle option positions randomly
4. Track new position of correct answer
5. Store shuffled options and new correct answer mapping

**Rules**:
- Shuffle independently for each question
- Preserve correct answer logic (still matches original answer)
- Each quiz instance gets unique shuffle

**Acceptance Criteria**:
- Original correct answer still marked as correct after shuffle ✓
- Options appear in valid permutations ✓
- No two quiz instances have identical shuffle ✓

### FR-5: Exam Display
**Description**: Present exam interface to user

**Components**:
1. **Question Display**: One question at a time or all questions (configurable)
2. **Timer**: Countdown in MM:SS format, updates every second
3. **Progress Indicator**: "Question X of Y"
4. **Answer Options**: Four radio buttons (A, B, C, D with texts)
5. **Navigation**: Previous/Next buttons or immediate submission
6. **Warning**: Alert at 5 minutes remaining

**Acceptance Criteria**:
- Timer displays correctly and decrements every second ✓
- Warning appears at exactly 5 minutes remaining ✓
- All options are selectable ✓
- Auto-submit triggers at time = 0 ✓

### FR-6: Answer Submission
**Description**: Capture and store user answers

**Process**:
1. User selects an option for each question
2. Submit button clicked or time expires
3. Collect all answers: `{question_id: selected_option}`
4. Store in database with timestamp
5. Prevent resubmission

**Data Captured**:
```
{
  session_id: unique_session_id,
  question_id: id,
  user_answer: 'A'/'B'/'C'/'D',
  timestamp: submission_time
}
```

### FR-7: Automatic Scoring
**Description**: Calculate score immediately upon submission

**Algorithm**:
1. Compare each user answer with correct answer
2. Count correct responses
3. Calculate percentage: (correct_count / num_questions) × 100
4. Apply Pass/Fail rule: ≥ 50 = PASS, < 50 = FAIL

**Results Stored**:
```
{
  session_id: unique,
  total_questions: int,
  correct_answers: int,
  incorrect_answers: int,
  skipped_answers: int,
  score: decimal(5,2),  # 0.00 to 100.00
  status: 'PASS'/'FAIL',
  time_spent: seconds
}
```

**Acceptance Criteria**:
- Score accuracy 100% (verified by manual calculation) ✓
- Skipped questions counted as incorrect ✓
- Result calculated within 1 second ✓
- Result saved in database ✓

### FR-8: Results Display
**Description**: Show user their exam results immediately after submission

**Display Elements**:
1. **Score Summary**:
   - Total score (e.g., "75.00/100")
   - Pass/Fail status (≥ 50 = PASS, < 50 = FAIL)
   - Percentage (e.g., "15 out of 20 correct")

2. **Statistics**:
   - Correct answers: count
   - Incorrect answers: count  
   - Skipped questions: count
   - Time spent vs. time allotted

3. **Question Breakdown** (optional, future enhancement):
   - Each question with user's answer, correct answer, status

**Acceptance Criteria**:
- Score displays immediately after submission ✓
- Pass/Fail status matches rule (score ≥ 50) ✓
- All statistics sum to total questions ✓

---

## Non-Functional Requirements

### NFR-1: Performance
- **Quiz Load Time**: ≤ 2 seconds
- **Score Calculation**: ≤ 1 second
- **Page Response Time**: ≤ 1 second for user interactions

### NFR-2: Reliability
- **Data Persistence**: Once submitted, results are permanently saved
- **Error Recovery**: Graceful error messages if something fails
- **Session Recovery**: Page reload restores in-progress exam (within 24 hours)

### NFR-3: Security
- **Data Protection**: Results stored securely (encrypted if on cloud)
- **Input Validation**: All Excel file inputs sanitized
- **File Storage**: Excel files stored in secure location

### NFR-4: Usability
- **UI Simplicity**: Clear, intuitive interface for single user
- **Timer Display**: Easy to read countdown in MM:SS format
- **Error Messages**: Clear, actionable error messages
- **Mobile Compatibility**: Works on desktop and tablet browsers

---

## System Constraints

### Technical Constraints
- **Framework**: Python Flask
- **Database**: SQLite (local file) or PostgreSQL
- **Frontend**: HTML/CSS/JavaScript
- **File Storage**: Local filesystem

### Business Constraints
- **Phase 1 Scope**: Single user, local file storage, no authentication
- **Access Model**: Local web app or self-hosted
- **Cost**: Minimal infrastructure
- **Timeline**: MVP in 2-3 weeks

### Data Constraints
- **Excel File Max Size**: 10 MB
- **Max Questions Per Quiz**: Limited by Excel file and memory
- **Session Timeout**: 24 hours
- **Score Precision**: 2 decimal places (0.00 to 100.00)

### User Constraints
- **Browser Support**: Chrome, Firefox, Safari, Edge (latest 2 versions)
- **Device Support**: Desktop, tablet (iOS/Android)
- **Accessibility**: Support for screen readers and keyboard navigation

---

## Acceptance Criteria

### AC-1: Excel Upload Feature
**Given**: User opens upload page  
**When**: Selects valid Excel file with all required columns and clicks "Upload"  
**Then**: System shows success message, assigns quiz ID, stores questions in database

**Given**: User uploads file with missing required column  
**When**: Clicks "Upload"  
**Then**: System shows error message "Missing required column: [ColumnName]" and does NOT store data

---

### AC-2: Quiz Configuration
**Given**: User is on configuration page with 50 available questions  
**When**: Selects "20" for num_questions and "45" for exam_duration  
**Then**: System creates quiz session and displays first question with timer showing 45:00

**Given**: User selects "70" when only 50 questions available  
**When**: Clicks "Start Quiz"  
**Then**: System shows error "Cannot select 70 questions (only 50 available)"

---

### AC-3: Option Shuffling
**Given**: Original correct answer is "Option B"  
**When**: User starts quiz twice with same Excel file  
**Then**: Options are shuffled differently in each attempt, correct answer still marked correctly

---

### AC-4: Automatic Scoring
**Given**: User answers 15 questions correctly out of 20 total  
**When**: Submits quiz  
**Then**: System displays "Score: 75.00/100" and "PASS" status immediately

**Given**: User answers 10 questions correctly and skips 5  
**When**: Submits quiz  
**Then**: Skipped questions counted as incorrect, score = (10/20)*100 = 50.00, Status = "PASS"

---

### AC-5: Timer & Auto-Submit
**Given**: Exam duration is 10 minutes  
**When**: Timer reaches 5 minutes remaining  
**Then**: Warning message appears: "5 minutes remaining!"

**When**: Timer reaches 0:00  
**Then**: Quiz automatically submits and shows results page

---

### AC-6: Results Display
**Given**: User completes quiz with 15 correct out of 20  
**When**: Quiz submits  
**Then**: Results page shows score (75.00/100), PASS status, and statistics (15 correct, 5 incorrect)

---

## Use Cases

### UC-1: Create Quiz from Excel File

**Actors**: User (Quiz Creator)

**Flow**:
1. User navigates to home/upload page
2. Selects Excel file with questions from their computer
3. System validates file format and required columns
4. System parses questions, options, and correct answers
5. System stores questions in database
6. System displays success message: "Quiz created! Total questions: 50"
7. System shows option to "Start New Exam" or upload another file

**Alternative**: File validation fails
- System displays error: "Missing required column: [ColumnName]" or "Invalid format"
- User corrects file and retries

**Postcondition**: Questions stored in database, ready for exam creation

---

### UC-2: Configure & Start Exam

**Actors**: User (Exam Taker)

**Flow**:
1. User clicks "Start New Exam" or selects quiz from list
2. System displays configuration page with:
   - "Number of Questions" input (default: 20, max: total available)
   - "Exam Duration (minutes)" input (default: 60)
3. User enters desired values (e.g., 30 questions, 90 minutes)
4. System validates inputs:
   - num_questions: 1 ≤ num ≤ total_available
   - duration: duration ≥ 1
5. System creates exam session:
   - Generates unique session ID
   - Randomly selects N questions
   - Shuffles options for each question
6. System displays first question with countdown timer
7. Timer starts (e.g., "90:00" for 90 minutes)

**Postcondition**: Exam session created, user sees first question with timer

---

### UC-3: Take Exam & Submit Answers

**Actors**: User (Exam Taker)

**Flow**:
1. User sees exam page with:
   - Question counter: "Question 1 of 30"
   - Timer: "90:00" (counting down)
   - Question text
   - Four answer options (A, B, C, D)
2. User selects an option by clicking radio button
3. User clicks "Next" button to see next question
4. System displays next question (repeat steps 2-3)
5. After all questions answered, user clicks "Submit Exam" OR
6. Timer reaches 0:00 → System auto-submits exam
7. System sends all answers to backend for scoring
8. System calculates score and displays results

**Alternative 1**: User doesn't answer all questions
- Unanswered (skipped) questions counted as incorrect
- Score calculated with skipped = 0 points

**Alternative 2**: Browser refresh during exam (Phase 2)
- User reopens browser and returns to exam URL
- Previous answers restored from localStorage
- Timer recalculates remaining time
- User can continue

**Postcondition**: Exam submitted, score calculated, results displayed

---

### UC-4: View Results

**Actors**: User (Exam Taker)

**Flow**:
1. After exam submission, user automatically shown results page
2. Results page displays:
   - Score summary: "Score: 75.00/100"
   - Pass/Fail status: "✓ PASS" (or "✗ FAIL")
   - Statistics: "24 correct, 6 incorrect, 0 skipped"
   - Time: "75 minutes 30 seconds out of 90 minutes"
3. User can:
   - Review results
   - Take another exam with different configuration
   - Upload new Excel file

**Postcondition**: User sees complete exam results and feedback

---

## Data Input & Output Specification

### Input Data

#### 1. Excel File Upload
```
Column Format:
- Question (required): text, max 2000 chars
- Option_A (required): text, max 500 chars
- Option_B (required): text, max 500 chars
- Option_C (required): text, max 500 chars
- Option_D (required): text, max 500 chars
- Correct_Answer (required): A/B/C/D only

Example Row:
Question: "What is the capital of France?"
Option_A: "London"
Option_B: "Paris"
Option_C: "Berlin"
Option_D: "Madrid"
Correct_Answer: "B"
```

#### 2. Quiz Configuration Input
```
num_questions: Integer, 1 to total_questions_in_file
exam_duration: Integer, >= 1 minute
```

#### 3. User Answers Input
```
{
  session_id: "abc-123-def",
  question_id: 1,
  selected_option: "A"  // or B, C, D
}
```

### Output Data

#### 1. Quiz Session Object (JSON)
```json
{
  "session_id": "abc-123-def",
  "quiz_id": "quiz-001",
  "num_questions": 20,
  "exam_duration": 60,
  "created_at": "2026-03-14T10:30:00Z",
  "status": "active",
  "selected_question_ids": [1, 5, 12, 8, ...]
}
```

#### 2. Question Object (with shuffled options)
```json
{
  "question_id": 1,
  "session_id": "abc-123-def",
  "question_text": "What is the capital of France?",
  "options": {
    "A": "Berlin",
    "B": "Paris",
    "C": "London",
    "D": "Madrid"
  },
  "correct_answer_position": "B"
}
```

#### 3. Score Result Object (JSON)
```json
{
  "session_id": "abc-123-def",
  "quiz_id": "quiz-001",
  "score": 75.00,
  "status": "PASS",
  "total_questions": 20,
  "correct_answers": 15,
  "incorrect_answers": 4,
  "skipped_answers": 1,
  "submitted_at": "2026-03-14T11:00:00Z",
  "time_spent_seconds": 1800,
  "time_allotted_minutes": 45
}
```

#### 4. Results Display (HTML/JSON)
```json
{
  "score_summary": {
    "score": 75.00,
    "out_of": 100.00,
    "status": "PASS",
    "percentage": "15/20"
  },
  "statistics": {
    "correct": 15,
    "incorrect": 4,
    "skipped": 1,
    "time_spent_seconds": 1800,
    "time_allotted_minutes": 45
  }
}
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **Question Bank** | Collection of questions from uploaded Excel file |
| **Quiz/Exam Session** | Single instance of taking an exam, has unique session_id with configuration and results |
| **Question** | Individual exam question with text and four options (A, B, C, D) |
| **Option Shuffling** | Randomizing the position of answer options within each question |
| **Auto-Submit** | Automatic exam submission when timer reaches 0:00 |
| **Pass/Fail** | Status determined by score: ≥ 50.00 = PASS, < 50.00 = FAIL |
| **Skipped Question** | Question user did not answer, counted as incorrect in scoring |
| **Correct Answer** | The option (A/B/C/D) marked as correct in the Excel file |

---

## References & Related Documents

- See `note/requirement_analysis_web_app.md` for methodology used in this analysis
- See `.github/copilot-instructions.md` for project governance rules