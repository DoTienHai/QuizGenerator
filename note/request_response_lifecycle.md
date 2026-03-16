# Request & Response: Life Cycle trong API

**Ngày tạo**: 2026-03-15  
**Mục đích**: Giải thích chi tiết Request-Response flow khi frontend gửi request đến backend API

---

## Mục Lục
- [Cách Hoạt Động](#1-cach-hoat-dong-request--be-xu-ly--response)
- [Ví Dụ GET](#2-vi-du-chi-tiet-get-apiquizzes1)
- [Ví Dụ POST](#3-vi-du-chi-tiet-post-apisessions)
- [Response Types](#4-response-types-cac-truong-hop-khac-nhau)
- [Tóm Tắt](#5-tom-tat-be-xu-ly-gi-truoc-khi-return-response)

---

## 1. Cách Hoạt Động: Request → BE Xử Lý → Response

### Flow Đơn Giản (3 bước)

```
┌─────────────────┐                    ┌──────────────────┐                    ┌─────────────────┐
│   Frontend      │                    │    Backend       │                    │   Frontend      │
│   (Browser)     │                    │    (Flask)       │                    │   (Browser)     │
└────────┬────────┘                    └────────┬─────────┘                    └────────┬────────┘
         │                                      │                                       │
         │ 1. SEND REQUEST                      │                                       │
         ├─────────────────────────────────────→│                                       │
         │                                      │                                       │
         │                            2. PROCESS LOGIC                                 │
         │                                      │                                       │
         │ 3. RETURN RESPONSE                   │                                       │
         │←─────────────────────────────────────┼───────────────────────────────────────┤
         │                                      │                                       │
```

### Flow Chi Tiết (7 bước)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  1. FRONTEND GỬI REQUEST                                                 │
│  ────────────────────────────                                            │
│  Ví dụ: GET /api/quizzes/1                                               │
│  Headers: { "Content-Type": "application/json" }                         │
│  Body: (không có cho GET)                                                │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │
                           ↓
┌──────────────────────────────────────────────────────────────────────────┐
│  2. BACKEND NHẬN REQUEST                                                 │
│  ──────────────────────                                                  │
│  Flask parse request:                                                    │
│  - URL: /api/quizzes/1 → quiz_id = 1                                     │
│  - Method: GET                                                           │
│  - Headers                                                               │
│  - Body (nếu có)                                                         │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │
                           ↓
┌──────────────────────────────────────────────────────────────────────────┐
│  3. VALIDATE INPUT (Optional but recommended)                            │
│  ──────────────────                                                      │
│  Kiểm tra:                                                               │
│  - quiz_id có hợp lệ không? (phải là số > 0)                             │
│  - Có missing required fields không?                                     │
│  - Data type có đúng không?                                              │
│                                                                          │
│  Nếu sai → Return error response luôn, không xử lý logic                │
│  Ví dụ: GET /api/quizzes/abc → Lỗi 400 Bad Request                      │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │
                           ↓ (Input hợp lệ)
┌──────────────────────────────────────────────────────────────────────────┐
│  4. XỬ LÝ LOGIC (Business Logic)                                         │
│  ─────────────                                                           │
│  Thực hiện công việc chính:                                              │
│  - Query database: tìm quiz với id=1                                     │
│  - Tính toán                                                             │
│  - Xử lý file                                                            │
│  - Gọi services bên ngoài                                                │
│                                                                          │
│  Ví dụ:                                                                  │
│    quiz = Quiz.query.get(1)                                              │
│    if not quiz:                                                          │
│        return error response (404 Not Found)                             │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │
                           ↓ (Xử lý xong)
┌──────────────────────────────────────────────────────────────────────────┐
│  5. TẠO RESPONSE OBJECT                                                  │
│  ─────────────────                                                       │
│  Chuẩn bị dữ liệu gửi về:                                                │
│  - Status code: 200, 201, 400, 404, 500, etc                             │
│  - Headers: { "Content-Type": "application/json" }                       │
│  - Body: JSON data hoặc error message                                    │
│                                                                          │
│  Ví dụ:                                                                  │
│    Status: 200 OK                                                        │
│    Headers: { "Content-Type": "application/json" }                       │
│    Body: {                                                               │
│      "quiz_id": 1,                                                       │
│      "total_questions": 50,                                              │
│      "name": "Sample Quiz"                                               │
│    }                                                                     │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │
                           ↓
┌──────────────────────────────────────────────────────────────────────────┐
│  6. GỬI RESPONSE VỀ FRONTEND                                             │
│  ──────────────────────────                                              │
│  HTTP Response gửi về với:                                               │
│  - Status code (200, 400, 404, etc)                                      │
│  - Response headers                                                      │
│  - Response body (JSON)                                                  │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │
                           ↓
┌──────────────────────────────────────────────────────────────────────────┐
│  7. FRONTEND NHẬN & XỬ LÝ RESPONSE                                       │
│  ──────────────────────────────                                          │
│  JavaScript code:                                                        │
│  - Kiểm tra status code                                                  │
│  - Parse JSON response                                                   │
│  - Update DOM / hiển thị dữ liệu                                          │
│  - Hoặc hiển thị error message nếu fail                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Ví Dụ Chi Tiết: GET /api/quizzes/1

### REQUEST (Frontend → Backend)

```
HTTP GET /api/quizzes/1

Headers:
  - Host: localhost:5000
  - Content-Type: application/json
  - Accept: application/json

Body: (không có cho GET)
```

### BACKEND PROCESSING

#### Bước 1: Nhận & Parse Request
```python
@app.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    # Flask tự động parse:
    # - quiz_id = 1 (từ URL)
    # - method = GET
```

#### Bước 2: Validate Input
```python
    # Validate: quiz_id phải > 0 (Flask đã validate type)
    if quiz_id < 1:
        return jsonify({'error': 'Invalid quiz_id'}), 400
```

#### Bước 3: Xử Lý Logic
```python
    # Query database
    quiz = Quiz.query.get(quiz_id)
    
    # Kiểm tra tìm thấy không
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # Có dữ liệu → tiếp tục
```

#### Bước 4: Tạo Response
```python
    # Tạo response data
    response_data = {
        'quiz_id': quiz.quiz_id,
        'total_questions': quiz.total_questions,
        'name': quiz.name,
        'uploaded_at': quiz.uploaded_at.isoformat()
    }
    
    return jsonify(response_data), 200
```

### RESPONSE (Backend → Frontend)

```
HTTP/1.1 200 OK

Headers:
  - Content-Type: application/json
  - Content-Length: 120

Body:
{
  "quiz_id": 1,
  "total_questions": 50,
  "name": "Sample Quiz",
  "uploaded_at": "2026-03-15T10:30:00Z"
}
```

### FRONTEND PROCESSING

```javascript
// JavaScript code xử lý response
fetch('/api/quizzes/1')
  .then(response => {
    // Step 1: Kiểm tra status code
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    // Step 2: Parse JSON
    return response.json();
  })
  .then(data => {
    // Step 3: Xử lý dữ liệu
    console.log(data);  // {quiz_id: 1, total_questions: 50, ...}
    
    // Step 4: Update DOM
    document.getElementById('quiz-name').textContent = data.name;
    document.getElementById('quiz-count').textContent = `${data.total_questions} questions`;
  })
  .catch(error => {
    // Step 5: Xử lý error
    console.error('Error:', error);
    alert('Failed to load quiz');
  });
```

---

## 3. Ví Dụ Chi Tiết: POST /api/sessions

### REQUEST (Frontend → Backend)

```
HTTP POST /api/sessions

Headers:
  - Host: localhost:5000
  - Content-Type: application/json

Body:
{
  "quiz_id": 1,
  "num_questions": 20,
  "exam_duration": 60
}
```

### BACKEND PROCESSING

```python
@app.route('/api/sessions', methods=['POST'])
def create_session():
    # ---- STEP 1: PARSE REQUEST ----
    data = request.get_json()  # {quiz_id: 1, num_questions: 20, duration: 60}
    
    # ---- STEP 2: VALIDATE INPUT ----
    if 'quiz_id' not in data:
        return jsonify({'error': 'Missing quiz_id'}), 400
    
    quiz_id = data.get('quiz_id')
    num_questions = data.get('num_questions', 10)  # Default 10
    exam_duration = data.get('exam_duration')
    
    if not isinstance(num_questions, int) or num_questions < 1:
        return jsonify({'error': 'Invalid num_questions'}), 400
    
    if not isinstance(exam_duration, int) or exam_duration < 1:
        return jsonify({'error': 'Invalid exam_duration'}), 400
    
    # ---- STEP 3: BUSINESS LOGIC ----
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    if num_questions > quiz.total_questions:
        return jsonify({
            'error': f'Cannot select {num_questions} questions (only {quiz.total_questions} available)'
        }), 400
    
    # Tạo phiên thi mới trong database
    from datetime import datetime, timedelta
    expires_at = datetime.utcnow() + timedelta(minutes=exam_duration)
    
    session = ExamSession(
        quiz_id=quiz_id,
        num_questions=num_questions,
        exam_duration=exam_duration,
        expires_at=expires_at,
        status='ACTIVE'
    )
    db.session.add(session)
    db.session.commit()
    
    # Chọn random questions
    questions = ExamService.get_random_questions(quiz_id, num_questions)
    
    # ---- STEP 4: TẠỌ RESPONSE ----
    response_data = {
        'session_id': session.session_id,
        'quiz_id': quiz_id,
        'num_questions': num_questions,
        'exam_duration': exam_duration,
        'created_at': session.created_at.isoformat(),
        'expires_at': session.expires_at.isoformat(),
        'status': 'ACTIVE',
        'questions': [q.to_dict() for q in questions]
    }
    
    return jsonify(response_data), 201
```

### RESPONSE (Backend → Frontend)

```
HTTP/1.1 201 Created

Headers:
  - Content-Type: application/json

Body:
{
  "session_id": 123,
  "quiz_id": 1,
  "num_questions": 20,
  "exam_duration": 60,
  "created_at": "2026-03-15T10:30:00Z",
  "expires_at": "2026-03-15T11:30:00Z",
  "status": "ACTIVE",
  "questions": [
    {
      "question_id": 1,
      "question_text": "What is 2+2?",
      "options": {
        "A": "3",
        "B": "4",
        "C": "5",
        "D": "6"
      }
    },
    ...
  ]
}
```

### FRONTEND PROCESSING

```javascript
async function startExam() {
  const requestData = {
    quiz_id: 1,
    num_questions: 20,
    exam_duration: 60
  };
  
  try {
    // Gửi request
    const response = await fetch('/api/sessions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestData)
    });
    
    // Kiểm tra status
    if (!response.ok) {
      const error = await response.json();
      alert(`Error: ${error.error}`);
      return;
    }
    
    // Parse response
    const data = await response.json();
    
    // Lưu session_id
    sessionStorage.setItem('session_id', data.session_id);
    
    // Hiển thị câu hỏi
    displayQuestions(data.questions);
    
    // Bắt đầu timer
    startTimer(data.exam_duration * 60);  // Convert to seconds
    
  } catch (error) {
    console.error('Error:', error);
  }
}
```

---

## 4. Response Types (Các Trường Hợp Khác Nhau)

### Success Response (2xx)

```
Status 200 OK
{
  "status": "success",
  "data": {...}
}

Status 201 Created
{
  "status": "success",
  "data": {...}
}

Status 204 No Content
(Không có body - dùng cho DELETE)
```

### Client Error Response (4xx)

```
Status 400 Bad Request
{
  "status": "error",
  "error": {
    "code": "INVALID_INPUT",
    "message": "num_questions must be > 0",
    "field": "num_questions"
  }
}

Status 404 Not Found
{
  "status": "error",
  "error": {
    "code": "QUIZ_NOT_FOUND",
    "message": "Quiz with ID 999 not found"
  }
}

Status 405 Method Not Allowed
{
  "status": "error",
  "error": {
    "message": "Method GET not allowed for this endpoint"
  }
}
```

### Server Error Response (5xx)

```
Status 500 Internal Server Error
{
  "status": "error",
  "error": {
    "message": "An unexpected error occurred"
  }
}
```

---

## 5. Tóm Tắt: BE Xử Lý Gì Trước Khi Return Response?

**ĐÚng, BE luôn thực hiện các bước sau**:

1. **📨 Nhận request** - Parse URL, headers, body
2. **✅ Validate input** - Kiểm tra dữ liệu hợp lệ hay không
3. **💾 Query database** - Tìm/tạo/cập nhật dữ liệu
4. **🔄 Xử lý logic** - Tính toán, transform dữ liệu
5. **⚠️ Error handling** - Nếu có lỗi → return error response
6. **📦 Tạo response** - Format dữ liệu thành JSON
7. **📤 Return response** - Gửi (status code, headers, body) về FE

**Ví dụ actual flow**:

```python
@app.route('/api/sessions', methods=['POST'])
def create_session():
    # 1. Nhận request
    data = request.get_json()
    
    # 2. Validate input
    if 'quiz_id' not in data:
        return {'error': 'Missing quiz_id'}, 400  # Return ngay, không tiếp tục
    
    # 3-4. Query & xử lý logic
    quiz = Quiz.query.get(data['quiz_id'])
    if not quiz:
        return {'error': 'Quiz not found'}, 404  # Return ngay, không tiếp tục
    
    session = ExamSession.create(...)  # Tạo session trong DB
    
    # 5-7. Tạo và return response
    return {
        'session_id': session.id,
        'status': 'ACTIVE'
    }, 201
```

**KEY POINT**: 
- ✅ Nếu bất kỳ bước nào **FAIL** → Dừng ngay, return error response
- ✅ Nếu tất cả bước **OK** → Return success response với dữ liệu

