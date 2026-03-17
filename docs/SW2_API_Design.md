# SW2: API Design and Contracts - QuizGenerator

**Last Updated**: 2026-03-15  
**Version**: 1.0  
**Status**: Design Phase  
**Author**: AI Assistant

---

## Table of Contents

- [API Overview](#api-overview)
- [API Endpoints](#api-endpoints)
- [Request/Response Formats](#requestresponse-formats)
- [Error Handling](#error-handling)
- [HTTP Status Codes](#http-status-codes)
- [Authentication & Authorization](#authentication--authorization)
- [Rate Limiting & Throttling](#rate-limiting--throttling)
- [API Versioning](#api-versioning)

---

## API Overview

### Architecture Style
**REST (Representational State Transfer)**

### Protocol
**HTTP/HTTPS**

### Response Format
**JSON** (primary), **HTML** (for pages)

### Base URL
```
Development: http://localhost:5000/api
Production: https://quizgenerator.example.com/api
```

### API Version
```
v1 (Current)
```

---

## API Endpoints

### 1. Quiz Management

#### 1.1 Upload Quiz (Excel File)

**Endpoint**: `POST /api/quizzes`

**Purpose**: Upload Excel file with questions (create new quiz)

**Request**:
```
POST /api/quizzes HTTP/1.1
Content-Type: multipart/form-data

Body:
{
  "file": <binary Excel file>
}
```

**Response (Success - 201)**:
```json
{
  "status": "success",
  "data": {
    "quiz_id": 1,
    "total_questions": 50,
    "uploaded_at": "2026-03-15T10:30:00Z",
    "message": "Quiz uploaded successfully"
  }
}
```

**Response (Error - 400)**:
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_FILE_FORMAT",
    "message": "Missing required column: Correct_Answer",
    "field": "file"
  }
}
```

**Validations**:
- File format: .xlsx or .xls
- File size: < 10 MB
- Required columns: Question, Option_A, Option_B, Option_C, Option_D, Correct_Answer
- Correct_Answer values: A/B/C/D only
- Question length: ≤ 2000 chars
- Option length: ≤ 500 chars each

---

#### 1.2 Get Quiz List

**Endpoint**: `GET /api/quizzes`

**Purpose**: List all uploaded quizzes

**Query Parameters**:
```
?limit=10        (default: 10, max: 100)
?offset=0        (default: 0, for pagination)
?sort=uploaded_at (default: uploaded_at DESC)
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "quizzes": [
      {
        "quiz_id": 1,
        "total_questions": 50,
        "uploaded_at": "2026-03-15T10:30:00Z",
        "name": "Sample Quiz 1"
      },
      {
        "quiz_id": 2,
        "total_questions": 75,
        "uploaded_at": "2026-03-14T15:45:00Z",
        "name": "Study Material 2"
      }
    ],
    "total_count": 2,
    "limit": 10,
    "offset": 0
  }
}
```

---

#### 1.3 Get Quiz Details

**Endpoint**: `GET /api/quizzes/{quiz_id}`

**Purpose**: Get details of specific quiz

**Path Parameters**:
```
quiz_id: Integer (required)
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "quiz_id": 1,
    "total_questions": 50,
    "uploaded_at": "2026-03-15T10:30:00Z",
    "name": "Sample Quiz 1",
    "questions_preview": [
      {
        "question_id": 1,
        "question_text": "What is 2+2?",
        "difficulty": 1
      }
    ]
  }
}
```

**Response (Error - 404)**:
```json
{
  "status": "error",
  "error": {
    "code": "QUIZ_NOT_FOUND",
    "message": "Quiz with ID 999 not found"
  }
}
```

---

### 2. Exam Session Management

#### 2.1 Create Exam Session

**Endpoint**: `POST /api/sessions`

**Purpose**: Create new exam session with configuration

**Request**:
```json
{
  "quiz_id": 1,
  "num_questions": 20,
  "exam_duration": 60
}
```

**Validations**:
- num_questions: 1 ≤ num ≤ total_questions_in_quiz
- exam_duration: ≥ 1 minute
- quiz_id: must exist

**Response (Success - 201)**:
```json
{
  "status": "success",
  "data": {
    "session_id": "abc-123-def-456",
    "quiz_id": 1,
    "num_questions": 20,
    "exam_duration": 60,
    "created_at": "2026-03-15T10:30:00Z",
    "expires_at": "2026-03-16T10:30:00Z",
    "status": "active",
    "questions": [
      {
        "question_id": 1,
        "question_text": "What is the capital of France?",
        "options": {
          "A": "Berlin",
          "B": "Paris",
          "C": "London",
          "D": "Madrid"
        },
        "position": 1
      },
      // ... more questions
    ]
  }
}
```

**Response (Error - 400)**:
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_CONFIG",
    "message": "Cannot select 70 questions (only 50 available)",
    "field": "num_questions"
  }
}
```

---

#### 2.2 Get Exam Session

**Endpoint**: `GET /api/sessions/{session_id}`

**Purpose**: Retrieve exam session data

**Path Parameters**:
```
session_id: String (UUID format, required)
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "session_id": "abc-123-def-456",
    "quiz_id": 1,
    "num_questions": 20,
    "exam_duration": 60,
    "created_at": "2026-03-15T10:30:00Z",
    "expires_at": "2026-03-16T10:30:00Z",
    "status": "active",
    "time_elapsed_seconds": 120,
    "questions": [
      {
        "question_id": 1,
        "question_text": "What is the capital of France?",
        "options": {
          "A": "Berlin",
          "B": "Paris",
          "C": "London",
          "D": "Madrid"
        }
      }
    ]
  }
}
```

**Response (Error - 404)**:
```json
{
  "status": "error",
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "Session not found or expired"
  }
}
```

---

#### 2.3 Check Session Status

**Endpoint**: `GET /api/sessions/{session_id}/status`

**Purpose**: Quick check if session is still active

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "session_id": "abc-123-def-456",
    "session_status": "active",
    "time_remaining_seconds": 1800
  }
}
```

---

### 3. Answer Submission

#### 3.1 Submit Single Answer

**Endpoint**: `POST /api/sessions/{session_id}/answers`

**Purpose**: Submit answer for one question

**Path Parameters**:
```
session_id: String (UUID format, required)
```

**Request**:
```json
{
  "question_id": 1,
  "user_answer": "B"
}
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "answer_id": 1,
    "session_id": "abc-123-def-456",
    "question_id": 1,
    "user_answer": "B",
    "answered_at": "2026-03-15T10:32:00Z",
    "message": "Answer recorded"
  }
}
```

**Response (Error - 400)**:
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_ANSWER",
    "message": "Invalid answer value. Must be A, B, C, or D"
  }
}
```

---

#### 3.2 Submit All Answers (Batch)

**Endpoint**: `POST /api/sessions/{session_id}/submit`

**Purpose**: Submit all answers and complete exam

**Path Parameters**:
```
session_id: String (UUID format, required)
```

**Request**:
```json
{
  "answers": [
    {
      "question_id": 1,
      "user_answer": "A"
    },
    {
      "question_id": 2,
      "user_answer": "B"
    },
    {
      "question_id": 3,
      "user_answer": null
    }
  ],
  "time_spent_seconds": 1800
}
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "result_id": 1,
    "session_id": "abc-123-def-456",
    "quiz_id": 1,
    "score": 75.00,
    "status": "PASS",
    "total_questions": 20,
    "correct_answers": 15,
    "incorrect_answers": 4,
    "skipped_answers": 1,
    "time_spent_minutes": 30,
    "time_allotted_minutes": 60,
    "submitted_at": "2026-03-15T11:00:00Z"
  }
}
```

**Response (Error - 400)**:
```json
{
  "status": "error",
  "error": {
    "code": "SESSION_EXPIRED",
    "message": "Exam session has expired"
  }
}
```

---

#### 3.3 Auto-Submit (Timer Expired)

**Endpoint**: `POST /api/sessions/{session_id}/auto-submit`

**Purpose**: Automatically submit when timer reaches 0:00

**Path Parameters**:
```
session_id: String (UUID format, required)
```

**Request**:
```json
{
  "time_spent_seconds": 3600
}
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "result_id": 1,
    "session_id": "abc-123-def-456",
    "score": 50.00,
    "status": "PASS",
    "message": "Exam auto-submitted due to time limit",
    "submitted_at": "2026-03-15T11:00:00Z"
  }
}
```

---

### 4. Results & Scoring

#### 4.1 Get Exam Results

**Endpoint**: `GET /api/results/{session_id}`

**Purpose**: Retrieve final exam results

**Path Parameters**:
```
session_id: String (UUID format, required)
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "result_id": 1,
    "session_id": "abc-123-def-456",
    "quiz_id": 1,
    "score": 75.00,
    "status": "PASS",
    "total_questions": 20,
    "correct_answers": 15,
    "incorrect_answers": 4,
    "skipped_answers": 1,
    "percentage": "75%",
    "time_spent_minutes": 30,
    "time_allotted_minutes": 60,
    "submitted_at": "2026-03-15T11:00:00Z",
    "question_breakdown": [
      {
        "question_id": 1,
        "question_text": "What is 2+2?",
        "user_answer": "B",
        "correct_answer": "B",
        "is_correct": true
      },
      {
        "question_id": 2,
        "question_text": "What is 3+3?",
        "user_answer": "A",
        "correct_answer": "B",
        "is_correct": false
      }
    ]
  }
}
```

---

#### 4.2 Get All Results for Quiz

**Endpoint**: `GET /api/quizzes/{quiz_id}/results`

**Purpose**: Retrieve all results for a quiz

**Query Parameters**:
```
?limit=10      (default: 10)
?offset=0      (default: 0)
?sort=submitted_at (default: submitted_at DESC)
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "quiz_id": 1,
    "results": [
      {
        "result_id": 1,
        "session_id": "abc-123-def-456",
        "score": 75.00,
        "status": "PASS",
        "submitted_at": "2026-03-15T11:00:00Z"
      },
      {
        "result_id": 2,
        "session_id": "def-456-ghi-789",
        "score": 45.00,
        "status": "FAIL",
        "submitted_at": "2026-03-14T15:30:00Z"
      }
    ],
    "total_count": 2,
    "average_score": 60.00,
    "pass_rate": 50.0
  }
}
```

---

#### 4.3 Get Quiz Statistics

**Endpoint**: `GET /api/quizzes/{quiz_id}/statistics`

**Purpose**: Summary statistics for a quiz

**Response (Success - 200)**:
```json
{
  "status": "success",
  "data": {
    "quiz_id": 1,
    "total_attempts": 5,
    "average_score": 68.00,
    "pass_rate": 80.0,
    "highest_score": 95.00,
    "lowest_score": 45.00,
    "average_time_spent": 35,
    "pass_count": 4,
    "fail_count": 1
  }
}
```

---

## Request/Response Formats

### Standard Success Response

```json
{
  "status": "success",
  "data": {
    // Response-specific data
  }
}
```

### Standard Error Response

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "field": "field_name (if applicable)",
    "details": {}  // Additional details (optional)
  }
}
```

### Request Headers

```
Content-Type: application/json
Accept: application/json
User-Agent: Client/1.0
```

### Response Headers

```
Content-Type: application/json
Cache-Control: no-cache, no-store, must-revalidate
X-Request-ID: unique-request-id
X-Response-Time: 125ms
```

---

## Error Handling

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_REQUEST | 400 | Malformed request |
| INVALID_FILE_FORMAT | 400 | File upload invalid format |
| INVALID_CONFIG | 400 | Quiz config invalid |
| INVALID_ANSWER | 400 | Answer format invalid |
| QUIZ_NOT_FOUND | 404 | Quiz doesn't exist |
| SESSION_NOT_FOUND | 404 | Session doesn't exist |
| SESSION_EXPIRED | 410 | Session expired (> 24h) |
| FORBIDDEN | 403 | Access denied |
| SERVER_ERROR | 500 | Internal server error |

### Error Response Example

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_CONFIG",
    "message": "Cannot select 70 questions (only 50 available)",
    "field": "num_questions",
    "details": {
      "max_available": 50,
      "requested": 70
    }
  },
  "timestamp": "2026-03-15T10:30:00Z"
}
```

---

## HTTP Status Codes

| Code | Usage |
|------|-------|
| **200 OK** | Successful GET, POST with data return |
| **201 Created** | Successfully POST that creates resource |
| **400 Bad Request** | Invalid request, validation error |
| **403 Forbidden** | Access denied |
| **404 Not Found** | Resource not found |
| **410 Gone** | Resource expired (session timeout) |
| **500 Internal Server Error** | Server error |
| **503 Service Unavailable** | Server temporarily unavailable |

---

## Authentication & Authorization

### Current Implementation
**None** - Single user app, no authentication required

### Future Considerations (Phase 2)
```
Authorization: Bearer <token>
```

---

## Rate Limiting & Throttling

### Current Implementation
**None** - Single user app

### Recommended for Phase 2
- **File uploads**: 1 per 5 seconds, max 10 MB
- **API calls**: 100 per minute
- **Score calculation**: 1 per submission

---

## API Versioning

### Version Strategy
**URL-based versioning**

```
Current: /api/v1/...
Future: /api/v2/... (if breaking changes needed)
```

### Backward Compatibility
- Version 1 maintained
- New versions don't break existing clients
- Client specifies version in URL

---

## Pagination

### Implementation
```
GET /api/quizzes?limit=10&offset=0
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "items": [...],
    "total_count": 50,
    "limit": 10,
    "offset": 0,
    "has_more": true
  }
}
```

---

## Data Validation Rules

### File Upload Validation
```
- Format: .xlsx OR .xls
- Size: < 10 MB
- Columns: All required columns present
- Data: Correct_Answer valid (A/B/C/D)
```

### Quiz Configuration Validation
```
- num_questions: 1 ≤ num ≤ total_available
- exam_duration: duration ≥ 1 minute
- quiz_id: Must exist in database
```

### Answer Validation
```
- user_answer: 'A' | 'B' | 'C' | 'D' | null
- question_id: Must exist in session
- session_id: Must be active (not expired)
```

---

## References

- See `docs/SW1_Requirement_Analysis.md` for functional specifications
- See `docs/SW2_Database_Schema.md` for data structures
- See `docs/SW2_System_Architecture.md` for system design
