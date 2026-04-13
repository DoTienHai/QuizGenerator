# SW3: Error Handling & Error Codes - QuizGenerator

**Last Updated**: 2026-04-03  
**Version**: 1.0  
**Status**: Implementation  
**Author**: AI Assistant

---

## Table of Contents

- [Error Handling Overview](#error-handling-overview)
- [Error Code Reference](#error-code-reference)
- [Error Response Format](#error-response-format)
- [HTTP Status Codes Mapping](#http-status-codes-mapping)
- [Error Handling Implementation](#error-handling-implementation)
- [Testing Error Scenarios](#testing-error-scenarios)

---

## Error Handling Overview

### Response Format

All API endpoints follow a **standardized response format** for both success and error cases:

```json
{
  "success": true/false,
  "error_code": "ERROR_CODE or empty string",
  "message": "Human readable message",
  "data": {} or null
}
```

### Key Points

- **success**: Boolean indicating operation result
- **error_code**: Standard error code (empty string if no error)
- **message**: User-friendly error or success message
- **data**: Response payload (null if error)

---

## Error Code Reference

### Complete Error Code List (18 codes)

#### 1. File-Related Errors

| Error Code | HTTP Status | Description | Example |
|-----------|-------------|-------------|---------|
| `ERR_MISSING_FILE` | 400 | File not provided in request | User submits form without selecting file |
| `ERR_INVALID_FILE_TYPE` | 400 | File format not supported (.pdf, .txt instead of .xlsx) | User uploads wrong file type |

---

#### 2. Parameter Validation Errors

| Error Code | HTTP Status | Description | Example |
|-----------|-------------|-------------|---------|
| `ERR_MISSING_PARAM` | 400 | Required parameter not provided | `quiz_id` missing in session create request |
| `ERR_INVALID_PARAM` | 400 | Parameter value invalid (e.g., string instead of number) | `num_questions="abc"` instead of `20` |
| `ERR_VALIDATION_FAILED` | 400 | General data validation failure | Excel file structure invalid |

---

#### 3. Resource Not Found

| Error Code | HTTP Status | Description | Example |
|-----------|-------------|-------------|---------|
| `ERR_QUIZ_NOT_FOUND` | 404 | Quiz doesn't exist in database | User tries to take quiz that was deleted |
| `ERR_SESSION_NOT_FOUND` | 404 | Session doesn't exist or already expired | User tries to access old exam session |
| `ERR_QUESTION_NOT_FOUND` | 404 | Question doesn't exist in session | Invalid question_id in answer submission |

---

#### 4. Session-Related Errors

| Error Code | HTTP Status | Description | Example |
|-----------|-------------|-------------|---------|
| `ERR_SESSION_EXPIRED` | 410 | Session expired (> 24h or manually deleted) | User tries to submit after session expired |
| `ERR_SESSION_ALREADY_SUBMITTED` | 400 | Cannot modify already submitted session | User tries to change answer after submission |

---

#### 5. Answer Validation

| Error Code | HTTP Status | Description | Example |
|-----------|-------------|-------------|---------|
| `ERR_INVALID_ANSWER` | 400 | Answer format invalid (must be A/B/C/D or empty) | User sends `answer="E"` or `"Yes"` |

---

#### 6. Business Logic Errors

| Error Code | HTTP Status | Description | Example |
|-----------|-------------|-------------|---------|
| `ERR_IMPORT_FAILED` | 400 | Excel import process failed | Duplicate questions detected in Excel file |
| `ERR_DUPLICATE_QUIZ` | 400 | Quiz with same name already exists | User uploads same quiz twice |
| `ERR_CALCULATION_ERROR` | 500 | Score calculation failed | Database corruption in ExamResult |

---

#### 7. Access & Server Errors

| Error Code | HTTP Status | Description | Example |
|-----------|-------------|-------------|---------|
| `ERR_FORBIDDEN` | 403 | Access denied (reserved for future auth) | Currently not used, reserved for auth |
| `ERR_INTERNAL` | 500 | General internal server error | Unexpected exception in service layer |
| `ERR_SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable | Database connection failed |

---

#### 8. Success Code

| Error Code | HTTP Status | Description |
|-----------|-------------|-------------|
| `SUCCESS` | 200/201 | Operation completed successfully (error_code is empty string) |

---

## Error Response Format

### Error Response Structure

```json
{
  "success": false,
  "error_code": "ERR_INVALID_PARAM",
  "message": "Cannot select 70 questions (only 50 available in quiz)",
  "data": null
}
```

### Success Response Structure

```json
{
  "success": true,
  "error_code": "",
  "message": "Quiz created successfully",
  "data": {
    "quiz_id": 1,
    "total_questions": 50,
    "uploaded_at": "2026-04-03T10:30:00Z"
  }
}
```

---

## HTTP Status Codes Mapping

### Status Code Reference

| HTTP Status | Usage | Error Codes |
|-----------|-------|------------|
| **200 OK** | Successful GET request | `success: true`, error_code: "" |
| **201 Created** | Successful POST (creates resource) | `success: true`, error_code: "" |
| **400 Bad Request** | Client-side validation error | `ERR_MISSING_*`, `ERR_INVALID_*`, `ERR_*VALIDATION_FAILED` |
| **403 Forbidden** | Access denied | `ERR_FORBIDDEN` (reserved for future use) |
| **404 Not Found** | Resource not found | `ERR_*_NOT_FOUND` |
| **410 Gone** | Resource expired/deleted | `ERR_SESSION_EXPIRED` |
| **500 Internal Server Error** | Server error | `ERR_INTERNAL`, `ERR_CALCULATION_ERROR` |
| **503 Service Unavailable** | Service temporarily down | `ERR_SERVICE_UNAVAILABLE` |

---

## Error Handling Implementation

### Backend Implementation

#### Where Error Codes Are Defined

**File**: `modules/utils/error_codes.py`

```python
# Error Code Constants
ERR_MISSING_FILE = "ERR_MISSING_FILE"
ERR_MISSING_PARAM = "ERR_MISSING_PARAM"
ERR_INVALID_PARAM = "ERR_INVALID_PARAM"
ERR_INVALID_FILE_TYPE = "ERR_INVALID_FILE_TYPE"
ERR_QUIZ_NOT_FOUND = "ERR_QUIZ_NOT_FOUND"
ERR_SESSION_NOT_FOUND = "ERR_SESSION_NOT_FOUND"
ERR_QUESTION_NOT_FOUND = "ERR_QUESTION_NOT_FOUND"
ERR_SESSION_EXPIRED = "ERR_SESSION_EXPIRED"
ERR_SESSION_ALREADY_SUBMITTED = "ERR_SESSION_ALREADY_SUBMITTED"
ERR_INVALID_ANSWER = "ERR_INVALID_ANSWER"
ERR_VALIDATION_FAILED = "ERR_VALIDATION_FAILED"
ERR_IMPORT_FAILED = "ERR_IMPORT_FAILED"
ERR_DUPLICATE_QUIZ = "ERR_DUPLICATE_QUIZ"
ERR_CALCULATION_ERROR = "ERR_CALCULATION_ERROR"
ERR_INTERNAL = "ERR_INTERNAL"
ERR_FORBIDDEN = "ERR_FORBIDDEN"
ERR_SERVICE_UNAVAILABLE = "ERR_SERVICE_UNAVAILABLE"
SUCCESS = "SUCCESS"

# Helper Functions
def error_response(error_code, message, status_code=400):
    """Create standardized error response"""
    return {
        "success": False,
        "error_code": error_code,
        "message": message,
        "data": None
    }, status_code

def success_response(data=None, message="Operation successful", status_code=200):
    """Create standardized success response"""
    return {
        "success": True,
        "error_code": "",
        "message": message,
        "data": data
    }, status_code
```

#### Usage in Routes

**Example**: Session creation endpoint

```python
from ..utils.error_codes import error_response, success_response, ERR_MISSING_PARAM, ERR_QUIZ_NOT_FOUND

@session_bp.route('/sessions', methods=['POST'])
def create_session():
    try:
        data = request.get_json()
        
        # Validate required parameter
        if not data or 'quiz_id' not in data:
            response, status = error_response(
                ERR_MISSING_PARAM,
                'quiz_id is required',
                400
            )
            return jsonify(response), status
        
        # Process request
        result = ExamService.create_session(
            data['quiz_id'],
            data.get('num_questions'),
            data.get('duration_minutes', 30)
        )
        
        if result['success']:
            response, status = success_response(
                data=result['data'],
                message="Session created successfully",
                status_code=201
            )
            return jsonify(response), status
        else:
            response, status = error_response(
                ERR_QUIZ_NOT_FOUND,
                result['message'],
                400
            )
            return jsonify(response), status
            
    except Exception as e:
        response, status = error_response(
            ERR_INTERNAL,
            f'Error creating session: {str(e)}',
            500
        )
        return jsonify(response), status
```

### Frontend Error Handling

#### JavaScript Error Handling Pattern

```javascript
async function submitAnswer(sessionId, questionId, answer) {
    try {
        const response = await fetch(`/api/sessions/${sessionId}/answers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question_id: questionId,
                user_answer: answer
            })
        });
        
        const data = await response.json();
        
        // Check for errors
        if (!data.success) {
            // Handle specific error codes
            switch(data.error_code) {
                case 'ERR_SESSION_EXPIRED':
                    showMessage('❌ Session expired. Please take exam again.', 'error');
                    redirectToExam();
                    break;
                case 'ERR_INVALID_ANSWER':
                    showMessage(`❌ ${data.message}`, 'error');
                    break;
                case 'ERR_SESSION_NOT_FOUND':
                    showMessage('❌ Session not found', 'error');
                    break;
                default:
                    showMessage(`❌ Error: ${data.message}`, 'error');
            }
            return false;
        }
        
        // Success
        showMessage('✅ Answer saved', 'success');
        return true;
        
    } catch (error) {
        showMessage(`❌ Network error: ${error.message}`, 'error');
        return false;
    }
}
```

---

## Testing Error Scenarios

### Manual Testing Checklist

#### File Upload Errors

- [ ] Test `ERR_MISSING_FILE`: Submit form without file
- [ ] Test `ERR_INVALID_FILE_TYPE`: Upload .txt or .pdf file
- [ ] Test `ERR_IMPORT_FAILED`: Upload Excel with missing columns
- [ ] Test `ERR_DUPLICATE_QUIZ`: Upload same quiz twice

**Expected**: 400 status, appropriate error_code, clear message

#### Parameter Validation

- [ ] Test `ERR_MISSING_PARAM`: Create session without quiz_id
- [ ] Test `ERR_INVALID_PARAM`: Send num_questions="abc"
- [ ] Test `ERR_INVALID_ANSWER`: Submit answer "E" (valid only: A/B/C/D)

**Expected**: 400 status, error_code set, data=null

#### Resource Not Found

- [ ] Test `ERR_QUIZ_NOT_FOUND`: Take exam with quiz_id=999
- [ ] Test `ERR_SESSION_NOT_FOUND`: Get results for non-existent session
- [ ] Test `ERR_QUESTION_NOT_FOUND`: Submit answer for invalid question_id

**Expected**: 404 status, resource's error_code, data=null

#### Session Lifecycle

- [ ] Test `ERR_SESSION_EXPIRED`: Wait 24+ hours, try to submit
- [ ] Test `ERR_SESSION_ALREADY_SUBMITTED`: Submit exam twice

**Expected**: 410/400 status, session error code

#### Success Cases

- [ ] ✅ Create session → 201, success=true, data has session_id
- [ ] ✅ Submit answer → 200, success=true, data=null
- [ ] ✅ Get results → 200, success=true, data has scores

---

## Error Code Hierarchy

```
Errors
├── File Errors (ERR_MISSING_FILE, ERR_INVALID_FILE_TYPE)
├── Validation Errors (ERR_MISSING_PARAM, ERR_INVALID_PARAM, ERR_VALIDATION_FAILED)
├── Resource Not Found (ERR_*_NOT_FOUND)
├── Session Errors (ERR_SESSION_EXPIRED, ERR_SESSION_ALREADY_SUBMITTED)
├── Business Logic (ERR_IMPORT_FAILED, ERR_DUPLICATE_QUIZ, ERR_CALCULATION_ERROR)
├── Access Control (ERR_FORBIDDEN)
└── Server Errors (ERR_INTERNAL, ERR_SERVICE_UNAVAILABLE)
```

---

## Migration Guide (Old → New Format)

### Before (Old Format)
```json
{
  "status": "error",
  "error": {
    "code": "QUIZ_NOT_FOUND",
    "message": "Quiz not found"
  }
}
```

### After (New Format)
```json
{
  "success": false,
  "error_code": "ERR_QUIZ_NOT_FOUND",
  "message": "Quiz not found",
  "data": null
}
```

### Changes

| Field | Old | New |
|-------|-----|-----|
| Root structure | `status` field | `success` boolean |
| Error structure | Nested in `error` object | Flat `error_code` field |
| Error code prefix | No prefix | `ERR_` prefix |
| Always present | No | Yes (empty string if no error) |
| Data on error | Not included | Explicitly `null` |

---

## Related Files

- **Implementation**: [`modules/utils/error_codes.py`](../modules/utils/error_codes.py)
- **API Contract**: [`docs/SW2_API_Design.md`](SW2_API_Design.md)
- **Session Routes**: [`modules/routes/session.py`](../modules/routes/session.py)
- **Test File**: [`tests/test_routes_session.py`](../tests/test_routes_session.py)

---

## Future Enhancements

- [ ] Error logging and monitoring
- [ ] Error tracking dashboard
- [ ] Automatic error notification
- [ ] Error analytics
- [ ] Rate limiting errors
- [ ] Custom error pages for frontend
