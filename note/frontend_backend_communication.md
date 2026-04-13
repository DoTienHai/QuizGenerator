---
date: 2026-04-03 15:00
summary: Cách truyền dữ liệu giữa Frontend (trình duyệt) và Backend (server) - HTTP methods, request/response, data formats
---

# Frontend - Backend Communication

## Mục Lục
- [HTTP Basics](#http-basics)
- [HTTP Methods](#http-methods)
- [Request & Response Format](#request--response-format)
- [Data Formats](#data-formats)
- [Browser Sessions & Cookies](#browser-sessions--cookies-identify-user)
- [Session vs Cookie - Deep Dive](#session-vs-cookie---deep-dive)
- [Session Lifecycle](#-session-lifecycle---qua-trình-từ-login-đến-hết-hạn)
- [Multi-Tab & Multi-Device Login](#-multi-tab--multi-device-login)
- [Device Fingerprinting & Backend Control](#-device-fingerprinting---thông-số-đặc-trưng-cho-máy)
- [Frontend Sending Data](#frontend-sending-data)
- [Backend Receiving Data](#backend-receiving-data)
- [QuizGenerator Examples](#quizgenerator-examples)
- [Common Patterns](#common-patterns)

---

## HTTP Basics

### Định Nghĩa
**HTTP** (HyperText Transfer Protocol) là cách FE và BE giao tiếp:

```
Frontend (Browser)                Backend (Server)
     |                                 |
     |------- HTTP Request ---->       |
     |        (Method, URL, Data)      |
     |                                 |
     |      HTTP Response <---------   |
     |      (Status, Headers, Body)    |
```

### Request Flow

```
1. Frontend (JS code)
   └─ Tạo request: fetch('/api/quizzes', {...})

2. Browser
   └─ Gửi qua Internet (HTTP protocol)

3. Backend Server (Flask, Node.js, etc.)
   └─ Nhận request, xử lý

4. Backend Server
   └─ Gửi response (JSON data, status code)

5. Browser
   └─ Nhận response

6. Frontend (JavaScript)
   └─ Parse JSON, update UI
```

---

## HTTP Methods

### CRUD Operations

**CRUD** = Create, Read, Update, Delete

| Method | Ý Nghĩa | Khi Dùng | Ví Dụ |
|--------|---------|---------|-------|
| **GET** | Lấy dữ liệu | Đọc dữ liệu từ server | `GET /api/quizzes` (lấy danh sách) |
| **POST** | Tạo dữ liệu | Tạo resource mới | `POST /api/quizzes` (tạo quiz) |
| **PUT** | Cập nhật toàn bộ | Cập nhật resource | `PUT /api/quizzes/1` (cập nhật quiz #1) |
| **DELETE** | Xóa dữ liệu | Xóa resource | `DELETE /api/quizzes/1` (xóa quiz #1) |
| **PATCH** | Cập nhật một phần | Cập nhật field nào đó | `PATCH /api/quizzes/1` (cập nhật tên) |

### Ví Dụ QuizGenerator

```javascript
// GET: Lấy danh sách quizzes
const quizzes = await fetch('/api/quizzes').then(r => r.json());

// POST: Tạo session mới
const session = await fetch('/api/sessions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ quiz_id: 1, num_questions: 20 })
}).then(r => r.json());

// PUT: Cập nhật exam result
const result = await fetch('/api/results/123', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: 'SUBMITTED', answers: [...] })
}).then(r => r.json());

// DELETE: Xóa quiz
await fetch('/api/quizzes/1', {
    method: 'DELETE'
});
```

---

## Request & Response Format

### HTTP Request Structure

```
POST /api/quizzes HTTP/1.1
Host: quizgenerator.com
Content-Type: application/json
Content-Length: 145

{
    "quiz_name": "Math Quiz",
    "num_questions": 20
}
```

**Phần tử:**
- **Method**: POST (cái hành động)
- **URL**: /api/quizzes (endpoint nào)
- **Headers**: Content-Type, Authorization, etc.
- **Body**: Dữ liệu gửi lên (JSON, FormData)

### HTTP Response Structure

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 256

{
    "success": true,
    "error_code": null,
    "message": "Quiz created successfully",
    "data": {
        "quiz_id": 15,
        "quiz_name": "Math Quiz",
        "num_questions": 20
    }
}
```

**Phần tử:**
- **Status Code**: 200 OK (thành công)
- **Headers**: Content-Type, etc.
- **Body**: Response data (JSON)

### HTTP Status Codes

| Code | Ý Nghĩa | Ví Dụ |
|------|---------|-------|
| **200 OK** | Success | Request thành công |
| **201 Created** | Resource tạo thành công | POST tạo quiz mới |
| **400 Bad Request** | Dữ liệu invalid | Missing field, format sai |
| **401 Unauthorized** | Chưa login/token invalid | Cần authenticate |
| **403 Forbidden** | Không có quyền | Không phải owner |
| **404 Not Found** | Resource không tồn tại | Quiz không tìm thấy |
| **500 Server Error** | Lỗi server | Database error, etc. |

---

## Backend Tạo Response (Response Creation)

### 🎯 Quy Tắc: Status Code + Headers + Body

**Backend PHẢI cung cấp 3 thành phần:**

```python
return {                    # ← 1. Body (JSON data)
    'success': True,
    'data': {...}
}, 201, {                   # ← 2. Status Code (BẮTBUỘC!)
    'Content-Type': 'application/json'  # ← 3. Headers
}
```

---

### ✅ Ví Dụ 1: POST - Tạo Quiz Mới

```python
from flask import Flask, request, jsonify

@app.route('/api/quizzes', methods=['POST'])
def create_quiz():
    """Tạo quiz mới"""
    
    # 1. Nhận dữ liệu từ request
    data = request.get_json()
    quiz_name = data.get('quiz_name')
    num_questions = data.get('num_questions')
    
    # 2. Validate dữ liệu
    if not quiz_name or not num_questions:
        return {
            'success': False,
            'error_code': 'INVALID_INPUT',
            'message': 'Missing required fields'
        }, 400  # ← Status code: 400 Bad Request
    
    # 3. Xử lý (tạo quiz, lưu DB, etc.)
    new_quiz = {
        'quiz_id': 15,
        'quiz_name': quiz_name,
        'num_questions': num_questions
    }
    
    # 4. Trả response thành công
    return {
        'success': True,
        'error_code': None,
        'message': 'Quiz created successfully',
        'data': new_quiz
    }, 201  # ← 201 Created
```

**Response:**
```json
HTTP/1.1 201 Created
Content-Type: application/json

{
    "success": true,
    "error_code": null,
    "message": "Quiz created successfully",
    "data": {
        "quiz_id": 15,
        "quiz_name": "Math Quiz",
        "num_questions": 20
    }
}
```

---

### ✅ Ví Dụ 2: GET - Lấy Danh Sách

```python
@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    """Lấy tất cả quizzes"""
    
    quizzes = [
        {'quiz_id': 1, 'quiz_name': 'Math', 'num_questions': 20},
        {'quiz_id': 2, 'quiz_name': 'English', 'num_questions': 15}
    ]
    
    return {
        'success': True,
        'error_code': None,
        'message': 'Quizzes retrieved',
        'data': quizzes
    }, 200  # ← 200 OK
```

---

### ✅ Ví Dụ 3: PUT - Cập Nhật Quiz

```python
@app.route('/api/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    """Cập nhật quiz"""
    
    data = request.get_json()
    
    # Check if exists
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return {
            'success': False,
            'error_code': 'NOT_FOUND',
            'message': 'Quiz not found'
        }, 404  # ← 404 Not Found
    
    # Update
    quiz.quiz_name = data.get('quiz_name', quiz.quiz_name)
    # db.session.commit()
    
    return {
        'success': True,
        'message': 'Quiz updated',
        'data': quiz.to_dict()
    }, 200  # ← 200 OK
```

---

### ✅ Ví Dụ 4: DELETE - Xóa Quiz

```python
@app.route('/api/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    """Xóa quiz"""
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return {
            'success': False,
            'error_code': 'NOT_FOUND',
            'message': 'Quiz not found'
        }, 404
    
    # db.session.delete(quiz)
    # db.session.commit()
    
    return {
        'success': True,
        'message': f'Quiz deleted',
        'data': {'quiz_id': quiz_id}
    }, 200  # ← 200 OK
```

---

### ❌ Ví Dụ 5: Error - Validation Failed

```python
@app.route('/api/quizzes', methods=['POST'])
def create_quiz_validated():
    """Tạo quiz với validation"""
    
    data = request.get_json()
    
    if not data.get('quiz_name'):
        return {
            'success': False,
            'error_code': 'MISSING_FIELD',
            'message': 'Field "quiz_name" is required'
        }, 400  # ← 400 Bad Request
    
    if not isinstance(data.get('num_questions'), int):
        return {
            'success': False,
            'error_code': 'INVALID_TYPE',
            'message': 'Field "num_questions" must be integer'
        }, 400
    
    # ... Create quiz ...
    return {'success': True, 'data': {...}}, 201
```

---

### ❌ Ví Dụ 6: Error - Chưa Login

```python
@app.route('/api/sessions', methods=['POST'])
def create_session():
    """Tạo exam session (cần login)"""
    
    user_id = session.get('user_id')
    if not user_id:
        return {
            'success': False,
            'error_code': 'UNAUTHORIZED',
            'message': 'Please login first'
        }, 401  # ← 401 Unauthorized
    
    # ... Create session ...
    return {'success': True, 'data': {...}}, 201
```

---

### ❌ Ví Dụ 7: Error - Không Có Quyền

```python
@app.route('/api/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz_checked(quiz_id):
    """Xóa quiz (check permission)"""
    
    user_id = session.get('user_id')
    if not user_id:
        return {'success': False, 'message': 'Not logged in'}, 401
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return {'success': False, 'message': 'Not found'}, 404
    
    # Check permission
    if quiz.owner_id != user_id:
        return {
            'success': False,
            'error_code': 'FORBIDDEN',
            'message': 'You cannot delete this quiz'
        }, 403  # ← 403 Forbidden
    
    # db.session.delete(quiz)
    return {'success': True, 'data': {'quiz_id': quiz_id}}, 200
```

---

### 📊 Tóm Tắt: Status Code Để Dùng

| Code | Khi Nào | Ví Dụ |
|------|---------|-------|
| **200 OK** | GET/PUT/DELETE OK | Update, delete thành công |
| **201 Created** | POST tạo resource | Tạo quiz, tạo session |
| **400 Bad Request** | Dữ liệu invalid | Missing field, type sai |
| **401 Unauthorized** | Chưa login | Cần authenticate |
| **403 Forbidden** | Login nhưng không quyền | Không phải owner |
| **404 Not Found** | Resource không tồn tại | Quiz không tìm |
| **500 Server Error** | Lỗi server | Exception, crash |

---

## Data Formats

### JSON (JavaScript Object Notation)

**Phổ biến nhất**, Lightweight, dễ parse:

```json
{
    "quiz_id": 1,
    "quiz_name": "Math Quiz",
    "questions": [
        {
            "id": 1,
            "text": "2+2=?",
            "options": ["3", "4", "5"],
            "correct": "B"
        }
    ]
}
```

**Frontend parse:**
```javascript
const data = await response.json();
console.log(data.quiz_name);  // "Math Quiz"
```

### FormData (cho file upload)

**Dùng khi upload file:**

```javascript
const formData = new FormData();
formData.append('quiz_name', 'My Quiz');
formData.append('file', fileInputElement.files[0]);

const response = await fetch('/api/quizzes', {
    method: 'POST',
    body: formData
    // Don't set Content-Type! Browser tự detect
});
```

**Backend nhận:**
```python
quiz_name = request.form.get('quiz_name')
file = request.files['file']
```

### URL-Encoded (Form)

**Cũ, dùng cho simple form:**

```javascript
// Frontend
await fetch('/api/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'username=user&password=pass123'
});
```

**Backend:**
```python
username = request.form.get('username')
password = request.form.get('password')
```

---

## Browser Sessions & Cookies (Identify User)

### ❓ Vấn Đề: Nhiều Users, Làm Sao BE Biết Gửi Data Cho Ai?

```javascript
// FE chỉ gửi URL đơn giản
const response = await fetch('/api/quizzes');

// 🤔 BE nhận request, nhưng:
// - Đến từ user nào?
// - Là admin hay user thường?
// - Nên gửi data của user nào về?
```

**Đáp Án: Browser tự động gửi Cookies!**

```
Browser                          Server
  |                                |
  | fetch('/api/quizzes')          |
  |------- Request + Cookies ----> |
  |                                |
  |  Cookie: session_id=abc123     |
  |  Cookie: user_id=42            |
  |                                |
  |      (Server dùng cookies)      |
  |      để identify user #42       |
  |                                |
  | <---- Response (data của #42)---
  |
```

### How Cookies Work

#### 1️⃣ User Đăng Nhập - Server Gửi Cookie

**Frontend HTML:**
```html
<form id="loginForm">
    <input id="username" type="text" placeholder="Username">
    <input id="password" type="password" placeholder="Password">
    <button type="submit">Login</button>
</form>
```

**Frontend JavaScript:**
```javascript
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        }),
        credentials: 'include'  // ⭐ Important: Allow cookies
    });
    
    const result = await response.json();
    if (result.success) {
        window.location.href = '/dashboard';
    }
});
```

**Backend Python (Flask):**
```python
from flask import session, jsonify

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Verify credentials
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return {'success': False, 'message': 'Invalid credentials'}, 401
    
    # ⭐ Save user_id in session/cookie
    session['user_id'] = user.id  # Browser gets cookie automatically
    
    return {'success': True, 'message': 'Logged in'}
```

**Browser tự động:**
1. Nhận response từ server
2. Server header: `Set-Cookie: session_id=xyz789; Path=/; HttpOnly`
3. Browser **tự động** lưu cookie
4. **Tất cả request sau đó** sẽ gửi cookie này

#### 2️⃣ User Gọi API - Browser Tự Gửi Cookie

**Frontend JavaScript:**
```javascript
// Browser tự động gửi cookies (do credentials: 'include')
const response = await fetch('/api/quizzes', {
    credentials: 'include'  // ⭐ Send cookies
});

// Thực tế, request gửi:
// GET /api/quizzes
// Cookie: session_id=xyz789
// (Browser tự thêm cookie!)
```

**Backend Python:**
```python
@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    # Server đọc cookie từ request
    user_id = session.get('user_id')  # Extract từ cookie
    
    if not user_id:
        return {'success': False, 'message': 'Not logged in'}, 401
    
    # ⭐ Now server knows: user #42 requested data
    quizzes = Quiz.query.filter_by(user_id=user_id).all()
    
    return {
        'success': True,
        'data': [q.to_dict() for q in quizzes]
    }
```

### Cookies vs SessionStorage

| Feature | Cookies | SessionStorage |
|---------|---------|---|
| **Lưu ở đâu** | Browser + Server | Browser only |
| **Server biết không** | ✅ Có (tự động gửi) | ❌ Không |
| **Expire** | Có thể set (1 ngày, 1 năm) | Khi close browser |
| **Dùng cho** | Authentication (login) | Temporary state (exam session) |
| **Security** | HttpOnly flag (không JS access) | JS có thể access, lộ dữ liệu |

**Ví dụ QuizGenerator:**

```javascript
// Đăng nhập: Backend gửi cookie session_id
// fetch('/api/login', ...) → Server set Cookie

// Sau đó, mỗi request:
// fetch('/api/quizzes') → Browser tự động thêm Cookie vào
// fetch('/api/sessions/123/questions') → Cookie gửi lại

// Ở client: lưu trạng thái exam trong SessionStorage
sessionStorage.setItem('sessionId', 123);  // Tạm thời
sessionStorage.setItem('currentQuestion', 1);  // Không cần BE biết
```

---

## Session vs Cookie - Deep Dive

### 🤔 Session là gì?

**Session** = Dữ liệu lưu trên **Server** để nhớ thông tin về user:

```
Server Memory/Database:
┌─────────────────────────────────────┐
│ Session Storage                      │
├─────────────────────────────────────┤
│ session_id=xyz789                    │
│  ├─ user_id: 42                      │
│  ├─ username: "john"                 │
│  ├─ login_time: 2026-04-03 15:30     │
│  ├─ ip_address: 192.168.1.100        │
│  └─ permissions: ["admin", "user"]   │
│                                       │
│ session_id=abc123                    │
│  ├─ user_id: 10                      │
│  ├─ username: "alice"                │
│  └─ ...                              │
└─────────────────────────────────────┘
```

**Ví dụ Python Flask:**
```python
from flask import session

@app.route('/api/login', methods=['POST'])
def login():
    user = User.query.filter_by(username='john').first()
    
    # ⭐ Create session on server
    session['user_id'] = user.id          # user_id: 42
    session['username'] = user.username   # username: "john"
    session['login_time'] = datetime.now()
    
    # Server automatically:
    # 1. Create session object with ID: xyz789
    # 2. Store session in memory/database
    # 3. Send cookie to browser: Set-Cookie: session_id=xyz789
```

### 🍪 Cookie là gì?

**Cookie** = Dữ liệu lưu trên **Browser**, được gửi lại server mỗi request:

```
Browser Storage:
┌─────────────────────────────────────┐
│ Cookies                              │
├─────────────────────────────────────┤
│ Name: session_id                     │
│ Value: xyz789                        │
│ Domain: quizgenerator.com            │
│ Path: /                              │
│ Expires: 2026-04-10 15:30 (7 days)  │
│ HttpOnly: true (JS không access)     │
│ Secure: true (chỉ HTTPS)             │
└─────────────────────────────────────┘
```

### ✅ Đúng! Cookie Được Backend Cấp

```
Backend:               Browser:               Server:
  ↓                      ↓                       ↓
BE tạo cookie      BE gửi cookie          BE cấp cookie
(Set-Cookie header)  qua HTTP Response     cho Browser
  
  ↓
Login thành công
response.set_cookie(
    'session_id',
    'xyz789',
    max_age=604800
)
  
  ↓
HTTP Response:
  Set-Cookie: session_id=xyz789; Max-Age=604800
  
  ↓
Browser nhận header Set-Cookie
→ Tự động lưu cookie vào storage
  
  ↓
Request tiếp theo:
Browser tự động gửi: Cookie: session_id=xyz789
  
  ↓
Backend nhận cookie
→ Dùng để identify user
```

**Ví Dụ:**

```python
# ⭐ Backend TẠO + GỬI Cookie

@app.route('/api/login', methods=['POST'])
def login():
    user = authenticate_user(username, password)
    
    # Backend tạo session
    session['user_id'] = user.id
    
    response = make_response({
        'success': True,
        'message': 'Logged in'
    })
    
    # ⭐ Backend GỬI cookie tới browser
    response.set_cookie(
        'session_id',      # Cookie name
        'xyz789',          # Cookie value (backend decide)
        max_age=604800,    # Backend decide expiry
        domain='.quiz.com', # Backend decide domain
        secure=True,       # Backend decide security
        httponly=True      # Backend decide access control
    )
    
    return response
    # Browser nhận response → Lưu cookie tự động
```

```javascript
// ⭐ Browser NHẬN + GỬI lại Cookie (không tạo)

// Developer không cần code gì để handling cookie
// Browser tự động xử lý:

// 1. Nhận: Set-Cookie header từ response
// 2. Lưu: Vào storage
// 3. Gửi lại: Tự động ở mỗi request

const response = await fetch('/api/quizzes', {
    credentials: 'include'  // Cho phép browser gửi cookies
});
// Behind the scenes:
// Browser tự động thêm: Cookie: session_id=xyz789
```

### 🔄 Quy Trình Chi Tiết:

```
Request #1: LOGIN
─────────────────
Browser                                    Backend
  |                                           |
  | POST /api/login                          |
  | Body: {username: john, pass: 123} ────> |
  |                                           |
  |                            ✓ Verify user |
  |                            ✓ Create session_id=xyz789 |
  |                            ✓ Store: session['user_id']=42 |
  |                           (⭐ Backend cấp)                |
  |                                           |
  | <─── Response ────────────────────────── |
  |      Set-Cookie: session_id=xyz789       |
  |      Max-Age: 604800 (7 days)           |
  |      Path: /                             |
  |      HttpOnly: true                      |
  |      (⭐ Backend gửi cookie)              |
  |                                           |
  | Browser tự động:                        |
  | 1. Nhận header Set-Cookie               |
  | 2. Lưu cookie vào storage               |
  | 3. Remember: session_id=xyz789          |
  | 4. Set timer: 7 ngày → xóa auto        |
  |                                           |


Request #2: GET QUIZZES (trong 7 ngày)
──────────────────────────────────────
Browser                                    Backend
  |                                           |
  | GET /api/quizzes                        |
  | Cookie: session_id=xyz789 (tự động) ──> |
  | (⭐ Browser tự động gửi lại)             |
  | ✅ Cookie vẫn có giá trị                |
  |                                           |
  |                            ✓ Nhận cookie |
  |                            ✓ Extract: session_id=xyz789 |
  |                            ✓ Lookup session → user_id=42 |
  |                            ✓ Get data của user #42 |
  |                                           |
  | <─── Response ────────────────────────── |
  |      {success: true, data: [...]} (của user #42) |
  |      🎉 KHÔNG CẦN USERNAME/PASSWORD!   |
  |                                           |


Request #3: GET QUIZZES (sau 7 ngày)
────────────────────────────────────
Browser                                    Backend
  |                                           |
  | GET /api/quizzes                        |
  | Cookie: [KHÔNG CÓ - đã hết hạn] ──────> |
  | (Browser xóa auto sau 7 ngày)            |
  | ❌ Cookie đã expired                     |
  |                                           |
  |                            ✓ Nhận request |
  |                            ✗ Không tìm thấy cookie |
  |                            ✗ session['user_id'] = None |
  |                                           |
  | <─── Response ────────────────────────── |
  |      {success: false, message: 'Not logged in', code: 401} |
  |      🔐 PHẢI LOGIN LẠI!                 |
  |                                           |


Request #4: LOGIN AGAIN
──────────────────────
Browser                                    Backend
  |                                           |
  | POST /api/login                          |
  | Body: {username: john, pass: 123} ────> |
  | (User phải nhập username + password)    |
  |                                           |
  |                            ✓ Verify user |
  |                            ✓ Create NEW session_id=abc999 |
  |                            ✓ Store: session['user_id']=42 |
  |                                           |
  | <─── Response ────────────────────────── |
  |      Set-Cookie: session_id=abc999       |
  |      Max-Age: 604800 (7 ngày mới)       |
  |                                           |
  | ✅ Cookie mới được tạo                  |
  | ✅ Reset timer 7 ngày                   |
  |                                           |


Request #5: GET QUIZZES (3 users khác nhau online cùng lúc)
──────────────────────────────────────────────────────────
User A:                                    Backend
  | GET /api/quizzes                        |
  | Cookie: session_id=aaa ───────────────> |
  |                            ✓ user_id=10 |
  | <─── quizzes của user #10 ──────────────
  |

User B:                                    Backend
  | GET /api/quizzes                        |
  | Cookie: session_id=bbb ───────────────> |
  |                            ✓ user_id=20 |
  | <─── quizzes của user #20 ──────────────
  |

User C:                                    Backend
  | GET /api/quizzes                        |
  | Cookie: session_id=ccc ───────────────> |
  |                            ✓ user_id=30 |
  | <─── quizzes của user #30 ──────────────
  |

⭐ Cùng URL, nhưng 3 users → 3 cookies khác → 3 datasets khác!
⭐ Mỗi user không cần nhập username/password mỗi request!
⭐ Cookie tự động xóa → phải login lại
```

### 📊 Tóm Tắt: Cookie Được Ai Cấp?

| Thành Phần | Được Ai Tạo? | Được Ai Gửi? | Lưu Ở Đâu? |
|-----------|-------------|-----------|-----------|
| **Cookie tạo lần đầu** | Backend | Backend (Set-Cookie header) | Browser Storage |
| **Cookie gửi lại** | ❌ Browser không tạo | Browser (tự động) | Từ Browser Storage |
| **Session** | Backend | Backend (store in memory/DB) | Server (không gửi cho browser) |

**= Session: Server-side storage**
**= Cookie: Browser-side storage (nhưng được Backend cấp dữ liệu)**

```python
# Backend:
session['user_id'] = 42           # ← Session (server-side)
response.set_cookie('session_id', 'xyz789')  # ← Cookie (cấp cho browser)

# Browser nhận:
# Cookie: session_id=xyz789  ← Lưu cookie
# (Không biết user_id=42, chỉ biết session_id)

# Request tiếp theo:
# Browser gửi: Cookie: session_id=xyz789
# Backend: Dùng session_id để lookup session → Lấy user_id=42
```

### 🔐 Session Lifecycle - Qua Trình Từ Login Đến Hết Hạn

**Tóm Tắt Của Bạn:**
```
Bước 1: Ban đầu
  └─ User chỉ có Username (chưa đăng nhập)
  └─ ❌ Không có Cookie

Bước 2: Đăng nhập (POST /api/login)
  └─ User gửi: username + password
  └─ Backend verify ✓
  └─ Backend TẠO: session_id + session['user_id']
  └─ Backend GỬI: Set-Cookie header
  └─ Browser LƯU: Cookie vào storage
  └─ ✅ Có Cookie (7 ngày)

Bước 3: Những request tiếp theo (7 ngày)
  └─ Browser TỰ ĐỘNG gửi: Cookie
  └─ Backend đọc: session['user_id'] từ session_id cookie
  └─ ✅ Mỗi request: KHÔNG cần username/password
  └─ Mọi hành động: Quiz, Session, Results - tất cả đều tự động!

Bước 4: Sau 7 ngày
  └─ Browser xóa cookie tự động (Max-Age hết)
  └─ ❌ Không còn Cookie
  └─ Backend: session['user_id'] = None
  └─ Tất cả API requests → return 401 Unauthorized

Bước 5: User muốn tiếp tục
  └─ PHẢI login lại: POST /api/login (username + password)
  └─ Backend tạo NEW session_id + NEW cookie
  └─ Reset timer 7 ngày
  └─ Process lặp lại from Bước 3
```

**Diagram Chi Tiết:**

```
Timeline:
──────────────────────────────────────────────────────────────

T=0s (Ban đầu)
│
├─ User mở app
├─ ❌ Không có cookie
├─ Backend: "Not logged in" → 401
└─ App yêu cầu: "Vui lòng đăng nhập"


T=0s (User nhập username + password)
│
├─ User click "Login"
├─ FE gửi: POST /api/login {username, password}
├─ Backend verify credentials ✓
├─ Backend tạo: session_id = "xyz789"
├─ Backend lưu: session['user_id'] = 42
├─ Backend gửi: Set-Cookie: session_id=xyz789; Max-Age=604800
├─ Browser nhận ✓
├─ Browser lưu cookie
├─ ✅ LOGGED IN
└─ Timer bắt đầu: 7 ngày countdown


T=5 minutes (Người dùng click "View All Quizzes")
│
├─ FE gửi: GET /api/quizzes
├─ Browser tự động: Cookie: session_id=xyz789
├─ Backend nhận cookie
├─ Backend lookup: session_id → user_id=42
├─ Backend: "This is user #42"
├─ Backend gửi: Quizzes của user #42
├─ ✅ SUCCESS (KHÔNG cần username/password!)
└─ Timer reset: 7 ngày countdown lại


T=1 hour (Người dùng upload quiz)
│
├─ FE gửi: POST /api/quizzes (FormData)
├─ Browser tự động: Cookie: session_id=xyz789
├─ Backend: "This is user #42"
├─ Backend tạo quiz với user_id=42
├─ ✅ SUCCESS
└─ Timer reset: 7 ngày countdown lại


T=6 days 23 hours 59 minutes (Sắp hết hạn)
│
├─ Cookie vẫn còn 1 phút
├─ Người dùng click "Create Exam"
├─ FE gửi: POST /api/sessions
├─ Browser tự động: Cookie: session_id=xyz789
├─ Backend: "This is user #42"
├─ ✅ SUCCESS (lần cuối cùng với cookie cũ)
└─ Timer: 1 phút countdown


T=7 days (COOKIE HẾT HẠN)
│
├─ Browser tự động XÓA cookie
├─ ❌ Cookie biến mất
├─ sessionStorage vẫn còn (nếu có)
└─ Nhưng session_id cookie = NULL


T=7 days + 1 minute (Người dùng click "View Results")
│
├─ FE gửi: GET /api/results
├─ Browser cố gửi: Cookie: [không tìm thấy]
├─ Request gửi: GET /api/results [NO COOKIE]
├─ Backend nhận request
├─ Backend: session.get('user_id') = None
├─ Backend: "Not logged in"
├─ Backend return: {success: false, code: 401, message: "Please login"}
├─ ❌ FORBIDDEN
├─ App yêu cầu: "Session expired, please login again"
└─ Người dùng PHẢI nhập username + password lại


T=7 days + 2 minutes (Login lại)
│
├─ User báo username + password
├─ FE gửi: POST /api/login {username, password}
├─ Backend verify ✓
├─ Backend tạo: NEW session_id = "abc999" (khác cũ)
├─ Backend lưu: NEW session['user_id'] = 42
├─ Backend gửi: Set-Cookie: session_id=abc999; Max-Age=604800
├─ Browser nhận ✓
├─ Browser lưu NEW cookie
├─ ✅ LOGGED IN AGAIN
└─ Timer bắt đầu: 7 ngày countdown (từ 0)


T=7 days + 3 minutes (Tiếp tục xài)
│
├─ FE gửi: GET /api/results
├─ Browser tự động: Cookie: session_id=abc999 (cookie mới!)
├─ Backend nhận
├─ Backend lookup: session_id=abc999 → user_id=42
├─ Backend: "This is user #42 (again)"
├─ Backend gửi: Results của user #42
├─ ✅ SUCCESS
└─ Timer reset: 7 ngày countdown lại
```

**🎯 Key Points:**

```
1️⃣ Ban đầu: ❌ Cookie
   → Backend: "Not logged in" → 401

2️⃣ Login: username + password
   → Backend tạo cookie
   → Browser lưu cookie

3️⃣ Trong thời hạn (7 ngày):
   → Browser tự động gửi cookie
   → ✅ Mỗi request KHÔNG cần username/password
   → Timer reset mỗi khi có request

4️⃣ Hết hạn:
   → Browser xóa cookie
   → Tất cả API → 401
   → PHẢI login lại

5️⃣ Login lại:
   → Backend tạo NEW cookie (khác cũ)
   → Process lặp lại
```

### 🔗 Cách Session & Cookie Kết Nối

```
Step 1: User Login
──────────────────
Browser                              Server
  |                                     |
  |-- POST /api/login --------->       |
  |  (username: john, pass: 123)       |
  |                                     |
  |  ✓ Verify credentials              |
  |  ✓ Create session object           |
  |    session_id = "xyz789"           |
  |    session['user_id'] = 42         |
  |    session['username'] = "john"    |
  |                                     |
  |<-- Response Header: ----------     |
  |    Set-Cookie: session_id=xyz789   |
  |    (+ Domain, Path, Expires, etc.) |
  |                                     |
  | Browser receives header            |
  | → Tự động lưu cookie vào storage   |
  | → Lưu name=session_id              |
  | → Lưu value=xyz789                 |


Step 2: Next Request (mỗi request sau)
──────────────────────────────────────
Browser                              Server
  |                                     |
  | GET /api/quizzes                    |
  |-- (tự động thêm cookie) ---->      |
  |  Cookie: session_id=xyz789         |
  |                                     |
  |  ✓ Server nhận cookie               |
  |  ✓ Extract session_id = "xyz789"   |
  |  ✓ Lookup session từ memory        |
  |  ✓ Get user_id = 42                |
  |  ✓ Biết đó là user john            |
  |  ✓ Return data của user #42        |
  |                                     |
  |<-- Response: quizzes của john ----  |
```

### 🌐 Multi-Tab & Multi-Device Login

**Câu hỏi:** Nếu cùng 1 user đăng nhập ở **2 tabs khác nhau** hoặc **2 máy khác nhau** thì sao?

#### Scenario 1️⃣: Cùng User → 2 Tabs Trên Cùng 1 Máy

```
Machine A (Chrome Browser):

  Tab 1                          Tab 2                     Server
    |                              |                          |
    |                              |                          |
    | POST /api/login              |                          |
    | (john / pass123) ──────────────────────────────────────> |
    |                              |                          |
    |                              |  ✓ Verify ✓ Create      |
    |                              |    session_id = "xyz789" |
    |                              |                          |
    | <──── Set-Cookie ────────────────────────────────────── |
    |       session_id=xyz789      |                          |
    | Browser lưu cookie           |                          |
    |                              |                          |
    | Browser Storage:             |                          |
    | ├─ session_id = "xyz789"     |                          |
    | └─ (SHARED giữa tabs)        |                          |
    |        ↓                      |                          |
    |        (Chrome cookie storage |                          |
    |         là global)           |                          |
    |        ↓                      |                          |
    |      Tab 2 cũng CÓ          |                          |
    |      session_id = "xyz789"   |                          |
    |                              |                          |
    | GET /api/quizzes             |                          |
    | Cookie: xyz789 ───────────────────────────────────────> |
    |                              | GET /api/results         |
    |                              | Cookie: xyz789 ────────> |
    |                              |                          |
    |                              |  ✓ Extract session_id    |
    |                              |  ✓ Lookup → user_id=42   |
    |                              |  ✓ Both requests = user#42
    |                              |                          |
    | <──── quizzes của john ──────────────────────────────── |
    |                              | <─ results của john ──── |
    |                              |                          |

⭐ KEY: Browser cookie SHARED giữa các tabs
⭐ Result: 2 tabs = CÙNG session_id = CÙNG user data
⭐ Backend sees: 1 session, chiều từ 2 tabs
⭐ Logout ở Tab 1 → Session xóa → Tab 2 cũng bị logout (cùng session)
```

#### Scenario 2️⃣: Cùng User → 2 Máy Khác Nhau

```
Machine A (Chrome)                 Machine B (Firefox)         Server
  |                                   |                           |
  |                                   |                           |
  | POST /api/login                   |                           |
  | (john / pass123) ──────────────────────────────────────────> |
  |                                   |                           |
  |                                   |  ✓ Verify ✓ Create       |
  |                                   |    session_id = "aaa111" |
  |                                   |                           |
  | <──── Set-Cookie ────────────────────────────────────────── |
  |       session_id=aaa111           |                           |
  | Browser A lưu cookie              |                           |
  |                                   |                           |
  | Browser A Storage:                |                           |
  | ├─ session_id = "aaa111"          |                           |
  | └─ (KHÁC Machine B)               |                           |
  |                                   |                           |
  |                                   | POST /api/login           |
  |                                   | (john / pass123) ────────> |
  |                                   |                           |
  |                                   |  ✓ Email/password verify  |
  |                                   |  ✓ Create NEW session     |
  |                                   |    session_id = "bbb222"  |
  |                                   |  (khác session cũ!)       |
  |                                   |                           |
  |                                   | <─ Set-Cookie ──────────  |
  |                                   |     session_id=bbb222     |
  |                                   | Browser B lưu cookie      |
  |                                   |                           |
  |                                   | Browser B Storage:        |
  |                                   | ├─ session_id = "bbb222"  |
  |                                   | └─ (KHÁC Machine A)       |
  |                                   |                           |
  | GET /api/quizzes                  |                           |
  | Cookie: aaa111 ────────────────────────────────────────────> |
  |                                   | GET /api/quizzes          |
  |                                   | Cookie: bbb222 ──────────> |
  |                                   |                           |
  |                        Backend Server Storage:                |
  |                        ┌─────────────────────────────────┐   |
  |                        │ Sessions:                       │   |
  |                        │ ├─ session['aaa111']            │   |
  |                        │ │  └─ user_id = 42 (john)      │   |
  |                        │ ├─ session['bbb222']            │   |
  |                        │ │  └─ user_id = 42 (john)      │   |
  |                        │ └─ (2 SESSIONS khác nhau!)     │   |
  |                        └─────────────────────────────────┘   |
  |                                   |                           |
  |  ✓ Lookup aaa111 → user_id=42     |                           |
  |  ✓ Server know: request từ user42 |  ✓ Lookup bbb222 → user_id=42 |
  |  ✓ Return quizzes của john        |  ✓ Server know: request từ user42
  |                                   |  ✓ Return quizzes của john |
  |                                   |                           |
  | <─── quizzes của john ────────────────────────────────────── |
  |                                   | <─ quizzes của john ───────
  |                                   |                           |

⭐ KEY: Browser cookies KHÔNG SHARED (khác máy)
⭐ Result: 2 machines = 2 SESSION IDs = 2 sessions trên server
⭐ Backend sees: 2 sessions (khác nhau) nhưng cùng user_id
⭐ Logout ở Machine A (xóa aaa111) → Machine B vẫn dùng bbb222 được!
```

#### 📊 So Sánh 2 Scenarios

| Yếu Tố | 2 Tabs (Cùng Máy) | 2 Máy Khác |
|--------|------------------|-----------|
| **Browser Storage** | ✅ SHARED (cùng Chrome) | ❌ KHÁC NHAU (khác device) |
| **Session IDs** | ✅ CÙNG 1 session_id | ❌ 2 session_ids khác |
| **Server Sessions** | ✅ 1 session entry | ❌ 2 session entries |
| **Request từ Tab 1** | → session_id=xyz789 | → session_id=aaa111 |
| **Request từ Tab 2** | → session_id=xyz789 (same) | N/A (khác máy) |
| **Logout ở Tab 1** | ❌ Tab 2 cũng logout | ✅ Machine 2 vẫn ok |
| **Backend View** | "1 user, 1 session, 2 tabs" | "1 user, 2 sessions, 2 devices" |

#### 🔴 Problem: Device Hijacking

```
Scenario: User bị hacker đánh cắp cookie

Machine A (Hacker):
  ├─ Hacker "steal" session_id = "aaa111" (từ user)
  ├─ Hacker set local cookie: session_id = "aaa111"
  └─ Hacker gửi requests như user → Backend accept!

Diagram:
─────────────────────────────────────────────

Legitimate User (Machine B)          Hacker (Machine A)
  |                                      |
  | GET /api/quizzes                     |
  | Cookie: aaa111 ──────────────────────> Backend
  |                                      |
  |                                      | GET /api/quizzes
  |                                      | Cookie: aaa111 (stolen!) ──> Backend
  |                                      |
  |                        Backend không biết
  |                        request từ hacker!
  |                        Cả 2 requests →
  |                        user_id = 42
  |
  | <──── OK ──────────────────────────────
  |                                      | <─ OK (lộ data!)

⚠️ Problem: Backend không distinguish được 2 requests
```

#### ✅ Solution: Add Device Fingerprinting

```python
# Backend:
# Khi login, save device info vào session

@app.route('/api/login', methods=['POST'])
def login():
    user = authenticate_user(username, password)
    
    # Save device info khi login
    session['user_id'] = user.id
    session['device_fingerprint'] = generate_fingerprint(request)
    # fingerprint = hash(User-Agent + IP Address + ...)
    
    return response

# Mỗi request sau, verify:

@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    user_id = session.get('user_id')
    saved_fingerprint = session.get('device_fingerprint')
    current_fingerprint = generate_fingerprint(request)
    
    if saved_fingerprint != current_fingerprint:
        # ⚠️ Device khác! Có thể là hacker
        # Option 1: Block request
        # Option 2: Ask 2FA (2-factor authentication)
        # Option 3: Log suspicious activity
        return {'success': False, 'message': 'Device mismatch'}, 403
    
    # OK, quizzes của user
```

#### 🎯 QuizGenerator Best Practice

```python
# Recommend:
# 1. Session timeout: 7 days là OK
# 2. Add device fingerprinting (optional)
# 3. Allow multiple devices per user (hầu hết apps làm thế)
# 4. Provide "logout all devices" feature
# 5. Log all login attempts + sessions

@app.route('/api/logout-all-devices', methods=['POST'])
def logout_all_devices():
    """Logout user from ALL devices"""
    user_id = session.get('user_id')
    
    # Delete ALL sessions for this user
    # pseudo code:
    # for session_id in all_sessions:
    #     if session[session_id]['user_id'] == user_id:
    #         delete session[session_id]
    
    # Current device:
    session.clear()
    response.delete_cookie('session_id')
    
    return {'success': True, 'message': 'Logged out from all devices'}
```

#### � HTTP Request Headers - Browser Tự Động Gửi Thông Tin Máy

**Câu hỏi của bạn:** "BE không thể biết được máy của FE, vậy cái gì đã lấy thông tin này để gửi cho BE?"

**Trả lời:** ⭐ **Browser tự động gửi thông tin về máy trong HTTP request headers, Frontend developer KHÔNG cần code gì cả!**

```
Frontend Developer Code:
───────────────────────

await fetch('/api/login', {
    method: 'POST',
    body: JSON.stringify({username, password})
    // ❌ KHÔNG gửi fingerprint, KHÔNG gửi máy info
})


Browser Tự Động Thêm Headers (Developer không cần làm):
──────────────────────────────────────────────────────

POST /api/login HTTP/1.1
Host: quizgenerator.com
Content-Type: application/json
Content-Length: 45

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0
  ↑ ⭐ Browser TỰ ĐỘNG gửi → Backend biết OS, Chrome version, bits
  
Accept-Language: vi-VN,vi;q=0.9,en;q=0.8
  ↑ ⭐ Browser TỰ ĐỘNG gửi → Backend biết ngôn ngữ user
  
Accept-Encoding: gzip, deflate, br
  ↑ ⭐ Browser TỰ ĐỘNG gửi → Backend biết compression support
  
X-Forwarded-For: 192.168.1.100
Connection: keep-alive
  ↑ ⭐ Server TỰ ĐỘNG capture → Backend biết IP address
  
Referer: https://quizgenerator.com/login


Backend Nhận Request:
────────────────────

@app.route('/api/login', methods=['POST'])
def login():
    # ✅ Backend CÓ ACCESS tất cả headers này:
    user_agent = request.headers.get('User-Agent')
    # → "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"
    
    language = request.headers.get('Accept-Language')
    # → "vi-VN,vi;q=0.9,en;q=0.8"
    
    ip_address = request.remote_addr
    # → "192.168.1.100"
    
    # Backend TỰ ĐỘNG generate fingerprint từ những header này!
    # ⭐ Frontend KHÔNG gửi, Backend TỰ LẤY!
```

**Diagram Chi Tiết - Cách Browser Gửi:**

```
User's Machine (Hardware):                    Browser (Software):
┌─────────────────────────────────┐          ┌──────────────────────────┐
│ OS: Windows 10 64-bit           │          │ Chrome Version 120.0     │
│ CPU: Intel 8-core               │          │ Language: Vietnamese     │
│ RAM: 16GB                       │          │ Screen: 1920x1080        │
│ IP: 192.168.1.100               │    ◄──── │ Cookies: [stored]        │
│ ISP: Viettel                    │          │ UserAgent: auto-detect   │
└─────────────────────────────────┘          └──────────────────────────┘
                                                         │
                                                         │ fetch('/api/login')
                                                         │ Developer code:
                                                         │ {username, password}
                                                         │
                                                         ▼
Browser Automatically Constructs Request Headers:
──────────────────────────────────────────────────

POST /api/login HTTP/1.1
Host: quizgenerator.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0
  └─ Auto-detect ✓

Accept-Language: vi-VN,vi;q=0.9
  └─ From OS/Browser settings ✓

Accept-Encoding: gzip, deflate
  └─ From Browser capabilities ✓

Cookie: session_id=xyz789
  └─ From Browser storage ✓

Content-Type: application/json
  └─ From fetch headers ✓

(IP Address: 192.168.1.100)
  └─ Auto-added by network layer ✓

⭐ ALL OF THIS is added AUTOMATICALLY by Browser
⭐ Frontend Developer KHÔNG CẦN CODE!
⭐ Backend receives these headers với mỗi request
```

**Ví dụ: Cùng Code, Khác Máy = Khác Headers:**

```
Machine A (Windows Chrome):
───────────────────────────
await fetch('/api/login', {...})
                ↓
POST /api/login
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0
IP: 192.168.1.100
Language: vi-VN

Machine B (Mac Firefox):
────────────────────────
await fetch('/api/login', {...})  # Exact same code!
                ↓
POST /api/login
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Firefox/121.0
IP: 203.0.113.50
Language: en-US

⭐ IDENTICAL Frontend code
❌ KHÁC Browser/OS → KHÁC User-Agent
❌ Khác Network/ISP → KHÁC IP Address
❌ Installed khác languages → KHÁC Accept-Language

Backend nhận 2 requests → Generate fingerprints:
- Machine A fingerprint: sha256("Windows|Chrome|192.168.1.100|vi-VN") = "abc123..."
- Machine B fingerprint: sha256("Mac|Firefox|203.0.113.50|en-US") = "xyz789..."

⭐ 2 Fingerprints KHÁC NHAU!
```

**Bảng: Thông Số Nào Được Browser Tự Động Gửi:**

| Thông Số | Browser Gửi? | Auto/Manual? | Ví Dụ | Backend Access? |
|---------|-----------|-----------|-------|---|
| **User-Agent** | ✅ CÓ | ✅ TỰ ĐỘNG | Mozilla/5.0 Windows Chrome | ✅ `request.headers.get('User-Agent')` |
| **IP Address** | ✅ CÓ | ✅ TỰ ĐỘNG | 192.168.1.100 | ✅ `request.remote_addr` |
| **Accept-Language** | ✅ CÓ | ✅ TỰ ĐỘNG | vi-VN,en-US | ✅ `request.headers.get('Accept-Language')` |
| **Accept-Encoding** | ✅ CÓ | ✅ TỰ ĐỘNG | gzip, deflate | ✅ `request.headers.get('Accept-Encoding')` |
| **Cookie** | ✅ CÓ | ✅ TỰ ĐỘNG | session_id=xyz789 | ✅ `session.get()` |
| **Referer** | ✅ CÓ | ✅ TỰ ĐỘNG | https://... | ✅ `request.headers.get('Referer')` |
| **Screen Size** | ❌ KHÔNG | N/A (JS only) | 1920x1080 | ❌ HTTP không gửi |
| **Device Memory** | ❌ KHÔNG | N/A (JS only) | 16GB | ❌ HTTP không gửi |

**Key Point:**
```
❌ WRONG: "Frontend gửi machine info cho Backend"
✅ RIGHT: "Browser tự động gửi headers, Backend đọc từ headers"

Backend không cần Frontend developer làm gì
Browser xử lý tất cả
```

---

#### 🖥️ Device Fingerprinting - Thông Số Đặc Trưng Cho Máy

**Câu hỏi:** Cookie còn phụ thuộc vào máy (device), vậy thông số nào đặc trưng cho máy?

**Trả lời:** Backend sử dụng những HTTP headers mà **Browser tự động gửi** để tạo "fingerprint" của device:

```python
# Backend code để tạo device fingerprint

def generate_device_fingerprint(request):
    """
    Tạo một unique identifier cho device
    Dùng để detect nếu request từ device khác
    
    ⭐ QUAN TRỌNG: 
      1. Frontend KHÔNG gửi fingerprint
      2. Browser TỰ ĐỘNG gửi headers (User-Agent, IP, Language)
      3. Backend EXTRACT từ headers
      4. Backend GENERATE fingerprint từ headers này
    """
    import hashlib
    
    # ✅ Backend EXTRACT từ request headers (Browser tự động gửi):
    fingerprint_data = {
        'user_agent': request.headers.get('User-Agent', ''),
        # Browser tự động gửi: "Mozilla/5.0 (Windows...) Chrome/120.0"
        
        'accept_language': request.headers.get('Accept-Language', ''),
        # Browser tự động gửi: "vi-VN,en-US"
        
        'accept_encoding': request.headers.get('Accept-Encoding', ''),
        # Browser tự động gửi: "gzip, deflate"
        
        'ip_address': request.remote_addr,
        # Server tự động capture: "192.168.1.100"
    }
    
    # Combine + Hash
    fingerprint_string = '|'.join(str(v) for v in fingerprint_data.values())
    fingerprint_hash = hashlib.sha256(fingerprint_string.encode()).hexdigest()
    
    return {
        'fingerprint': fingerprint_hash,  # "abc123def456..."
        'details': fingerprint_data
    }

# ❓ Ai gửi thông số này cho Backend?
# ✅ BROWSER (không phải Frontend developer)
# ✅ Browser tự động thêm headers vào request
```

**Flow Chi Tiết - Frontend KHÔNG gửi, Browser gửi:**

```
Step 1: Frontend gửi login request
═════════════════════════════════

Frontend Code (Developer viết):
──────────────────────────────
const response = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        username: 'john',
        password: 'pass123'
        // ❌ KHÔNG gửi fingerprint!
    })
});

⭐ Frontend Code: CHỈ gửi username + password


Step 2: Browser TỰ ĐỘNG thêm headers
═════════════════════════════════════

Browser (NOT controlled by Frontend code):
──────────────────────────────────────────

POST /api/login HTTP/1.1
Host: quizgenerator.com
Content-Type: application/json
Content-Length: 45

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0
├─ ⭐ Browser AUTO-DETECT OS + Browser version
├─ ⭐ Frontend code KHÔNG kiểm soát

Accept-Language: vi-VN,vi;q=0.9,en;q=0.8
├─ ⭐ Browser READ từ OS settings
├─ ⭐ Frontend code KHÔNG kiểm soát

Accept-Encoding: gzip, deflate, br
├─ ⭐ Browser AUTO-DETECT compression support
├─ ⭐ Frontend code KHÔNG kiểm soát

(Network Layer)
IP: 192.168.1.100
└─ ⭐ Server AUTO-CAPTURE từ socket
   └─ ⭐ Frontend code KHÔNG kiểm soát


Step 3: Backend EXTRACT từ headers
═════════════════════════════════

@app.route('/api/login', methods=['POST'])
def login():
    # Backend nhận HTTP request với headers
    # Headers này do Browser gửi, KHÔNG do Frontend code gửi!
    
    # ✅ Extract thông số từ headers:
    user_agent = request.headers.get('User-Agent')
    # → "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"
    
    language = request.headers.get('Accept-Language')
    # → "vi-VN,vi;q=0.9,en;q=0.8"
    
    ip_address = request.remote_addr
    # → "192.168.1.100"
    
    # ✅ Generate fingerprint từ các thông số này
    fingerprint = generate_device_fingerprint(request)
    # → fingerprint['fingerprint'] = "abc123def456789abcdef..."
    
    # ⭐ Fingerprint tạo xong → so sánh với DB, lưu DB
    return {'success': True, ...}
```

**Diagram: AI Gửi Thông Tin:**

```
┌──────────────────────────────────────────────────────┐
│ Frontend Developer Code (JavaScript)                  │
├──────────────────────────────────────────────────────┤
│ await fetch('/api/login', {                           │
│     body: JSON.stringify({username, password})       │
│ })                                                    │
│                                                       │
│ ❌ KHÔNG gửi: User-Agent, IP, Language, etc.        │
│ Frontend developer KHÔNG CODE những thứ này          │
└──────────────────────────────────────────────────────┘
                      ↓
                      │
             (HTTP Request được tạo)
                      │
                      ↓
┌──────────────────────────────────────────────────────┐
│ Browser (Chrome, Firefox, Safari, Edge)               │
├──────────────────────────────────────────────────────┤
│ ⭐ TỰ ĐỘNG THÊM HEADERS (Developer KHÔNG Code)       │
│                                                       │
│ User-Agent: [Detect OS + Browser version]            │
│   ← Browser tự biết nó chạy trên Windows 10          │
│   ← Browser tự biết version Chrome 120               │
│                                                       │
│ Accept-Language: [Read từ OS Setting]                │
│   ← Browser tự đọc setting "Vietnamese"              │
│   ← Frontend KHÔNG can thiệp                         │
│                                                       │
│ Accept-Encoding: [Auto-detect capabilities]          │
│   ← Browser tự biết nó support gzip hay không        │
│                                                       │
│ (IP Address)                                         │
│   ← Network layer tự capture từ socket               │
│   ← Backend, Browser, Frontend đều KHÔNG kiểm soát  │
└──────────────────────────────────────────────────────┘
                      ↓
                      │
                 "POST /api/login
                  User-Agent: Mozilla/5.0 Windows Chrome
                  Accept-Language: vi-VN
                  Accept-Encoding: gzip
                  (IP: 192.168.1.100)"
                      │
                      ↓
┌──────────────────────────────────────────────────────┐
│ Backend (Python Flask)                               │
├──────────────────────────────────────────────────────┤
│ request.headers.get('User-Agent')                    │
│   ← ✅ GET từ HTTP headers                          │
│   ← ✅ Headers do Browser gửi                       │
│                                                       │
│ request.headers.get('Accept-Language')               │
│   ← ✅ GET từ HTTP headers                          │
│   ← ✅ Headers do Browser gửi                       │
│                                                       │
│ request.remote_addr                                  │
│   ← ✅ GET IP address                              │
│   ← ✅ Từ network connection (auto-captured)        │
│                                                       │
│ fingerprint = SHA256(User-Agent|IP|Language)        │
│   ← ✅ GENERATE fingerprint                         │
│   ← ✅ Backend quyết định logic                     │
│                                                       │
│ Compare with DB → Detect new device if different    │
└──────────────────────────────────────────────────────┘

⭐ Key: Machine info được Browser gửi, KHÔNG phải Frontend
⭐ Nguyên lý: Browser tự động, Frontend developer không code
```

**So Sánh: Cùng Frontend Code, Khác Machine = Khác Headers:**

```
FRONTEND CODE (Cả 2 máy đều giống):
───────────────────────────────────
await fetch('/api/login', {
    body: JSON.stringify({username: 'john', password: '123'})
});

⭐ IDENTICAL code trên 2 máy


MACHINE A (Windows 10, Chrome, IP 192.168.1.100):
─────────────────────────────────────────────────
Browser tự động gửi:
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0
  Accept-Language: vi-VN
  IP: 192.168.1.100

Backend generate: fingerprint_A = SHA256("Windows|Chrome|192.168.1.100|vi")


MACHINE B (Mac, Firefox, IP 203.0.113.50):
──────────────────────────────────────────
Browser tự động gửi:
  User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15) Firefox/121
  Accept-Language: en-US
  IP: 203.0.113.50

Backend generate: fingerprint_B = SHA256("Mac|Firefox|203.0.113.50|en")


RESULT:
───────
⭐ fingerprint_A ≠ fingerprint_B
⭐ Backend detects 2 different devices
⭐ Can ask 2FA for new device
```

**❌ MISCONCEPTION vs ✅ CORRECT:**

```
❌ WRONG: "Frontend gửi fingerprint cho Backend"
   ("Frontend sends fingerprint to Backend")
   
❌ WRONG: "Frontend code gửi machine characteristics"
   ("Frontend code sends machine characteristics")
   
✅ CORRECT: "Browser tự động gửi headers (User-Agent, IP, Language)"
   ("Browser automatically sends headers")
   
✅ CORRECT: "Backend extract + generate fingerprint từ headers"
   ("Backend extracts + generates fingerprint from headers")
   
✅ CORRECT: "Frontend developer KHÔNG cần code fingerprint logic"
   ("Frontend developer doesn't need to code fingerprinting")
```

---

#### 🖥️ Backend Code: Cách Extract Device Info Từ Headers

**Ví dụ Thực Tế:**

```python
# ✅ Frontend CHỈ gửi username + password
# ✅ Browser TỰ ĐỘNG gửi headers
# ✅ Backend EXTRACT + GENERATE fingerprint

@app.route('/api/login', methods=['POST'])
def login():
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    
    # ⭐ Backend EXTRACT từ request headers (Browser tự động gửi):
    fingerprint = generate_device_fingerprint(request)
    print(f"Device fingerprint: {fingerprint['fingerprint']}")
    # Output: Device fingerprint: abc123def456789...
    # (Backend generate từ User-Agent, IP, Language)
    
    # ✓ Verify username/password
    user = User.query.filter_by(username=username).first()
    
    # ✓ Check device là known hay new
    known_device = DeviceLog.query.filter_by(
        user_id=user.id,
        fingerprint=fingerprint['fingerprint']
    ).first()
    
    if not known_device:
        # New device! Require 2FA
        return {'success': False, 'message': 'New device. Enter 2FA code'}, 202
    
    # Trusted device → login success
    session['user_id'] = user.id
    return {'success': True}
```

**Breakdown: Backend Extract từ Headers Nào:**

```python
def generate_device_fingerprint(request):
    """
    Extract device info từ HTTP request headers
    Những headers này do Browser tự động gửi, KHÔNG phải Frontend code gửi
    """
    import hashlib
    
    # ⭐ Tất cả những dòng dưới đây: Browser gửi, Backend extract
    
    # 1. User-Agent: Browser/OS/Platform info
    user_agent = request.headers.get('User-Agent', '')
    # Ví dụ: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"
    # Browser TỰ ĐỘNG gửi, Frontend không code
    
    # 2. Accept-Language: User's language preference
    language = request.headers.get('Accept-Language', '')
    # Ví dụ: "vi-VN,vi;q=0.9,en;q=0.8"
    # Browser đọc từ OS settings, Frontend không code
    
    # 3. IP Address: Network identifier
    ip_address = request.remote_addr
    # Ví dụ: "192.168.1.100"
    # Server tự động capture, Frontend không code
    
    # 4. Accept-Encoding: Supported compression
    encoding = request.headers.get('Accept-Encoding', '')
    # Ví dụ: "gzip, deflate, br"
    # Browser tự động gửi, Frontend không code
    
    # ⭐ Combine all + hash
    fingerprint_string = f"{user_agent}|{language}|{ip_address}|{encoding}"
    fingerprint_hash = hashlib.sha256(fingerprint_string.encode()).hexdigest()
    
    return {
        'fingerprint': fingerprint_hash,  # "abc123def456..."
        'details': {
            'user_agent': user_agent,
            'language': language,
            'ip_address': ip_address,
            'encoding': encoding
        }
    }

# ⭐ RESULT: Backend có device fingerprint mà KHÔNG cần Frontend code gì!
```

**Summary: Ai Gửi Cái Gì:**

```
┌─────────────────────────────────────────────────────┐
│ Frontend Developer                                   │
│ ├─ Gửi: username, password                         │
│ └─ KHÔNG gửi: User-Agent, IP, Language, etc.       │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ Browser (Automatic)                                 │
│ ├─ Gửi: User-Agent (từ OS/Browser detect)         │
│ ├─ Gửi: Accept-Language (từ OS settings)          │
│ ├─ Gửi: Accept-Encoding (từ Browser capabilities) │
│ ├─ Gửi: Cookie (từ Browser storage)               │
│ └─ Gửi: IP Address (từ network layer)             │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ Backend                                             │
│ ├─ Extract: request.headers.get('User-Agent')     │
│ ├─ Extract: request.headers.get('Accept-Language')|
│ ├─ Extract: request.remote_addr (IP)              │
│ ├─ Generate: fingerprint = sha256(...)            │
│ └─ Compare: với DB → detect new device?           │
└─────────────────────────────────────────────────────┘
```

---



**So Sánh Fingerprints Giữa Các Devices:**

```
Machine A (Chrome, Windows, IP 192.168.1.100):
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0
  IP: 192.168.1.100
  Language: vi-VN
  → Machine A Fingerprint = "abc123def456..."

Machine B (Firefox, Mac, IP 203.0.113.50):
  User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Firefox/121.0
  IP: 203.0.113.50
  Language: vi-VN
  → Machine B Fingerprint = "xyz789uvw012..." (KHÁC!)

Tab 1 (Chrome, Windows, 192.168.1.100):
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0
  IP: 192.168.1.100
  Language: vi-VN
  → Tab 1 Fingerprint = "abc123def456..." (GIỐNG Machine A!)

⭐ KEY: Fingerprint được Backend generate
⭐ Backend tự động compare → know device nào
```

**Các thông số đặc trưng cho máy:**

| Thông Số | Ví Dụ | Thay Đổi Khi? | Được Gửi? |
|---------|-------|-------------|----------|
| **IP Address** | 192.168.1.100 | Đổi máy, wifi | ✅ Tự động |
| **User-Agent** | Chrome/120.0 (Windows) | Đổi browser, OS | ✅ Tự động |
| **Language** | vi-VN | Thay language setting | ✅ Tự động |
| **Timezone** | UTC+7 | Đổi máy/vùng | ✅ Tự động |
| **Screen Size** | 1920x1080 | Đổi máy | ❌ Không gửi |
| **Device Memory** | 16GB | Đổi máy | ❌ Không gửi |

**❌ Frontend KHÔNG cần gửi fingerprint, vì:**
- Browser tự động gửi User-Agent header
- Request tự động include IP address (Backend nhận được)
- Request tự động include Accept-Language (Browser setting)
- **Backend chỉ cần extract + generate hash**

**✅ Backend tự động generate + so sánh**

#### 🎮 Backend Quyết Định Số Máy Được Phép

**Câu hỏi 2:** Số máy có thể sử dụng còn phụ thuộc vào BE có cho phép hay không?

**Trả lời:** ✅ **ĐÚNG 100%!** Backend quyết định hết!

```python
# Backend có toàn quyền quyết định:

# Option 1: Cho phép UNLIMITED devices (như Gmail)
# - User có thể dùng 100 máy, 1000 máy tùy thích
# - Mỗi máy ⟹ 1 session riêng
# - Server: Giới hạn session = unlimited

@app.route('/api/login', methods=['POST'])
def login_unlimited():
    """Allow user login from unlimited devices"""
    user = authenticate_user(username, password)
    
    # Create NEW session (không xóa session cũ)
    session['user_id'] = user.id
    session_id = generate_unique_id()
    
    # Save vào database → có thể có 1000 sessions cho 1 user!
    # ✅ User được phép login từ bao nhiêu máy tùy thích


# Option 2: Giới hạn MAX devices (như Netflix)
# - User chỉ được login từ tối đa 4 máy
# - Login máy 5 → tự động logout máy cũ nhất

@app.route('/api/login', methods=['POST'])
def login_limited_devices():
    """Allow max 4 concurrent devices"""
    user = authenticate_user(username, password)
    
    MAX_DEVICES = 4
    
    # Get all active sessions của user này
    user_sessions = Session.query.filter_by(user_id=user.id).all()
    
    # Nếu đã có 4 sessions, xóa session cũ nhất
    if len(user_sessions) >= MAX_DEVICES:
        oldest_session = min(user_sessions, key=lambda s: s.created_at)
        db.session.delete(oldest_session)
    
    # Tạo session mới
    session['user_id'] = user.id
    db.session.commit()
    
    return {'success': True}
    # ❌ Device 5 → Device 1 logout (automatic)


# Option 3: Cho phép 1 device duy nhất (Security cao)
# - User chỉ được dùng 1 device
# - Login từ máy mới → máy cũ logout

@app.route('/api/login', methods=['POST'])
def login_single_device():
    """Allow only 1 device per user"""
    user = authenticate_user(username, password)
    
    # Xóa tất cả sessions cũ
    old_sessions = Session.query.filter_by(user_id=user.id).all()
    for old_session in old_sessions:
        db.session.delete(old_session)
    
    # Tạo session mới (chỉ cái này valid)
    session['user_id'] = user.id
    db.session.commit()
    
    return {'success': True}
    # ❌ Chỉ device hiện tại được login
    # ❌ Machine B logout khi Machine A login


# Option 4: New Device Notification
# - Cho phép unlimited devices
# - Nhưng notify user khi login từ device mới

@app.route('/api/login', methods=['POST'])
def login_with_notification():
    """Allow unlimited devices + notify for new devices"""
    user = authenticate_user(username, password)
    
    # Get device fingerprint
    new_fingerprint = generate_device_fingerprint(request)
    
    # Check if device seen before
    known_device = DeviceFingerprint.query.filter_by(
        user_id=user.id,
        fingerprint=new_fingerprint['fingerprint']
    ).first()
    
    if not known_device:
        # New device! Send notification
        send_email(user.email, f"New login from {request.remote_addr}")
    
    # Create session + save device
    session['user_id'] = user.id
    device = DeviceFingerprint(
        user_id=user.id,
        fingerprint=new_fingerprint['fingerprint'],
        user_agent=new_fingerprint['details']['user_agent'],
        ip_address=new_fingerprint['details']['ip_address']
    )
    db.session.add(device)
    db.session.commit()
    
    return {'success': True}
```

**Bảng So Sánh - Backend Quyết Định:**

| Policy | Max Devices | When 5th Device Login? | Ví Dụ |
|--------|------------|----------------------|-------|
| **Unlimited** | ∞ | Cho phép ✅ Device 5 là valid | Gmail |
| **Limited (4)** | 4 | Xóa device cũ ❌ Device 1 logout | Netflix |
| **Single Device** | 1 | Xóa hết cũ ❌ All khác devices logout | Bank app |
| **Notify** | ∞ | Cho phép + gửi email ⚠️ User review | Facebook |

#### 🚨 Backend Control - Examples

```python
# Ví dụ 1: Get tất cả active devices của user

@app.route('/api/devices', methods=['GET'])
def get_user_devices():
    """List all active devices"""
    user_id = session.get('user_id')
    
    # Get all sessions của user
    user_sessions = Session.query.filter_by(user_id=user_id).all()
    
    devices = []
    for sess in user_sessions:
        devices.append({
            'device_id': sess.session_id,
            'ip_address': sess.ip_address,
            'user_agent': sess.user_agent,
            'last_active': sess.last_activity,
            'is_current': sess.session_id == session.sid  # Current device?
        })
    
    return {'success': True, 'data': devices}


# Ví dụ 2: Logout một device cụ thể

@app.route('/api/devices/<device_id>/logout', methods=['POST'])
def logout_specific_device(device_id):
    """Logout a specific device"""
    user_id = session.get('user_id')
    
    # Find session
    sess = Session.query.filter_by(
        session_id=device_id,
        user_id=user_id
    ).first()
    
    if not sess:
        return {'success': False, 'message': 'Device not found'}, 404
    
    db.session.delete(sess)
    db.session.commit()
    
    return {'success': True, 'message': f'Device {device_id} logged out'}


# Ví dụ 3: Detect suspicious login (khác device)

@app.route('/api/login', methods=['POST'])
def login_with_security():
    """Login with suspicious device detection"""
    user = authenticate_user(username, password)
    
    current_fingerprint = generate_device_fingerprint(request)
    
    # Get latest known fingerprint
    latest_device = DeviceFingerprint.query.filter_by(
        user_id=user.id
    ).order_by(DeviceFingerprint.created_at.desc()).first()
    
    if latest_device and latest_device.fingerprint != current_fingerprint['fingerprint']:
        # Device mới!
        # Option 1: Send verification code (2FA)
        verification_code = generate_code()
        send_sms(user.phone, f"Verification code: {verification_code}")
        
        # Store code tạm thời
        session['pending_2fa'] = {
            'code': verification_code,
            'user_id': user.id,
            'expires': time.time() + 300  # 5 minutes
        }
        
        return {
            'success': False,
            'message': 'New device detected. Enter verification code.'
        }, 202  # Accepted but pending
    
    # Device quen → login bình thường
    session['user_id'] = user.id
    return {'success': True, 'message': 'Logged in'}
```

#### 📊 Summary: Backend Controls Everything

```
┌─────────────────┐
│  User Account   │ user.py (database)
│  john@email.com │
└────────┬────────┘
         │
         ├─ Allowed IPs: ["192.168.1.100", "203.0.113.50"]
         │  (BE quyết định IP nào được access)
         │
         ├─ Max Concurrent Sessions: 3
         │  (BE quyết định bao nhiêu device được login cùng lúc)
         │
         ├─ Session Timeout: 7 days
         │  (BE quyết định session hết hạn bao lâu)
         │
         ├─ Trusted Devices: ["fingerprint_abc", "fingerprint_xyz"]
         │  (BE quyết định device nào "trusted")
         │
         ├─ Require 2FA: false
         │  (BE quyết định cần 2-factor authentication không)
         │
         ├─ Last Login: 2026-04-03 15:30:00
         │  (Backend log)
         │
         └─ Sessions (BE quyết định cấu hình)
            ├─ session_id=aaa111 (Machine A, IP 192.168.1.100)
            ├─ session_id=bbb222 (Machine B, IP 203.0.113.50)
            └─ session_id=ccc333 (Phone, IP 103.91.x.x)

⭐ KEY: Backend là "chủ nhân" của tất cả quyết định!
   - Bao nhiêu máy?
   - Từ IP nào?
   - Cookie hết hạn bao lâu?
   - Có require 2FA không?
   - Có notify user không?
   - etc. → TẤT CẢ do BE decide!
```

### Cookie Được Xác Định Dựa Trên Yếu Tố Nào?

#### 1️⃣ **Domain** - Website nào được phép dùng cookie

```
Cookie Domain: quizgenerator.com
├─ ✅ quizgenerator.com → Có thể gửi
├─ ✅ www.quizgenerator.com → Có thể gửi (subdomain)
├─ ✅ app.quizgenerator.com → Có thể gửi (subdomain)
└─ ❌ otherdomain.com → KHÔNG được gửi (khác domain)
```

**Ví dụ Flask:**
```python
response = make_response({'success': True})
response.set_cookie(
    'session_id',
    'xyz789',
    domain='quizgenerator.com',  # ← Domain
    path='/',
    max_age=7*24*60*60,  # 7 days
    secure=True,  # HTTPS only
    httponly=True  # JS không access
)
return response
```

#### 2️⃣ **Path** - URL path nào được phép dùng cookie

```
Cookie Path: /
├─ ✅ /api/quizzes → Có thể gửi
├─ ✅ /api/sessions → Có thể gửi
├─ ✅ /dashboard → Có thể gửi
└─ (mọi path đều được)

Cookie Path: /api
├─ ✅ /api/quizzes → Có thể gửi
├─ ✅ /api/sessions → Có thể gửi
└─ ❌ /dashboard → KHÔNG được gửi (khác path)
```

#### 3️⃣ **Expires / Max-Age** - Cookie hết hạn khi nào

```
Max-Age: 7*24*60*60 (7 ngày)
├─ Khi hết 7 ngày → Cookie tự động xóa

Expires: Wed, 10 Apr 2026 15:30:00 GMT
├─ Khi đến thời gian này → Cookie tự động xóa

Không set Expires/Max-Age
├─ Session cookie → Xóa khi close browser
```

**Ví dụ:**
```python
# Session cookie (xóa khi close browser)
response.set_cookie('session_id', 'xyz789')

# Persistent cookie (7 ngày)
response.set_cookie('session_id', 'xyz789', max_age=7*24*60*60)

# Persistent cookie (expires at specific date)
response.set_cookie('session_id', 'xyz789', expires='Wed, 10 Apr 2026 15:30:00')
```

#### 4️⃣ **Secure Flag** - Chỉ gửi qua HTTPS (secure connection)

```
Secure: true
├─ ✅ HTTPS://quizgenerator.com → Gửi cookie
└─ ❌ HTTP://quizgenerator.com → KHÔNG gửi (không secure)

Secure: false (hoặc không set)
├─ ✅ HTTP://quizgenerator.com → Gửi cookie
├─ ✅ HTTPS://quizgenerator.com → Gửi cookie
```

#### 5️⃣ **HttpOnly Flag** - JavaScript không thể access

```
HttpOnly: true
├─ ✅ Server có thể đọc: session.get('session_id')
├─ ❌ JavaScript KHÔNG thể: document.cookie (không hiện)
└─ 🔒 Security: Chống XSS attacks

HttpOnly: false
├─ ✅ Server có thể đọc
├─ ✅ JavaScript CÓ thể đọc: document.cookie
└─ ⚠️ Risk: Nếu hacker inject JS, có thể steal cookie
```

**Thiết lập HttpOnly:**
```python
response.set_cookie(
    'session_id', 
    'xyz789',
    httponly=True  # ⭐ JavaScript không thể access
)
```

### Cookie Header Format

**Khi Server gửi cookie:**
```
HTTP/1.1 200 OK
Set-Cookie: session_id=xyz789; Domain=quizgenerator.com; Path=/; Max-Age=604800; Secure; HttpOnly

(Các thuộc tính cách nhau bằng ;)
```

**Khi Browser gửi cookie lại:**
```
GET /api/quizzes HTTP/1.1
Cookie: session_id=xyz789

(Chỉ gửi name=value, không gửi lại các attributes)
```

### Ví Dụ Thực: QuizGenerator Cookie

**Backend gửi cookie:**
```python
@app.route('/api/login', methods=['POST'])
def login():
    user = User.query.filter_by(username='john').first()
    
    session['user_id'] = user.id
    session['username'] = user.username
    
    response = make_response({
        'success': True,
        'message': 'Logged in'
    })
    
    # ⭐ Set cookie with attributes
    response.set_cookie(
        key='session_id',           # Cookie name
        value=session.sid,          # Cookie value (unique)
        domain='.quizgenerator.com', # Domain + subdomains
        path='/',                    # All paths
        max_age=7*24*60*60,         # 7 days
        secure=True,                # HTTPS only
        httponly=True,              # JS cannot access
        samesite='Lax'              # CSRF protection
    )
    
    return response
```

**Browser tự động gửi cookie:**
```javascript
// Developer không cần làm gì
const response = await fetch('/api/quizzes', {
    credentials: 'include'  // Browser tự động gửi cookies
});

// Behind the scenes:
// GET /api/quizzes
// Cookie: session_id=xyz789  ← Browser tự động gửi!
```

### Cookie Security Best Practices

```python
response.set_cookie(
    'session_id',
    session.sid,
    # ✅ Phòng chống XSS (JavaScript injection)
    httponly=True,
    
    # ✅ Phòng chống Man-in-the-Middle
    secure=True,  # HTTPS only
    
    # ✅ Phòng chống CSRF (Cross-Site Request Forgery)
    samesite='Strict',  # Or 'Lax', 'None'
    # SameSite=Strict: Cookie được gửi chỉ khi same-site request
    # SameSite=Lax: Cookie gửi cho same-site + top-level navigation
    # SameSite=None: Cookie luôn gửi (cần + Secure=True)
    
    # ✅ Set reasonable expiry
    max_age=7*24*60*60,  # 7 days (không quá lâu)
    
    # ✅ Domain scope
    domain='.quizgenerator.com'  # Một domain duy nhất
)
```

### Cookie Size Limits

```
Max cookie size: ~4KB (per cookie)
Max cookies per domain: ~180-200 cookies

QuizGenerator típico:
- session_id: ~50 bytes
- Tổng: <100 bytes

✅ Không vượt quá limit
```

### Xóa Cookie

**Browser tự động xóa:**
```python
# Hết hạn (Max-Age = 7 days)
response.set_cookie('session_id', 'xyz789', max_age=604800)
# Sau 7 ngày → xóa tự động

# Close browser (Session cookie)
response.set_cookie('session_id', 'xyz789')
# Close browser → xóa
```

**Server xóa:**
```python
@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()  # Xóa session từ server
    
    response = make_response({'success': True})
    response.delete_cookie('session_id')  # ⭐ Xóa cookie từ browser
    # Hoặc:
    # response.set_cookie('session_id', '', max_age=0)
    
    return response
```

---

## Frontend Sending Data

### 1. Simple GET Request

```javascript
// ⭐ Browser tự động gửi cookies (nếu có set credentials)
const response = await fetch('/api/quizzes', {
    credentials: 'include'  // Gửi cookies
});
const data = await response.json();

console.log(data.data);  // [{quiz_id: 1, ...}, ...] của user hiện tại

// Behind the scenes:
// GET /api/quizzes
// Cookie: session_id=xyz789  ← Browser thêm tự động
//
// Backend đọc cookie → biết user #42 → gửi data của user #42
```

**Backend nhận và đọc cookies:**
```python
@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    # Python Flask tự động đọc cookies
    user_id = session.get('user_id')  # Từ cookies
    
    if not user_id:
        return {'success': False, 'message': 'Not logged in'}, 401
    
    # Gửi data của user này
    quizzes = Quiz.query.filter_by(user_id=user_id).all()
    return {'success': True, 'data': [q.to_dict() for q in quizzes]}
```

### 2. POST with JSON

```javascript
// Create new session
const response = await fetch('/api/sessions', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        quiz_id: 1,
        num_questions: 20,
        exam_duration: 60
    })
});

const result = await response.json();
console.log(result.data.session_id);
```

### 3. POST with FormData (File Upload)

```javascript
// Upload quiz from Excel file
const fileInput = document.getElementById('excelFile');
const quizNameInput = document.getElementById('quizName');

const formData = new FormData();
formData.append('quiz_name', quizNameInput.value);
formData.append('file', fileInput.files[0]);

const response = await fetch('/api/quizzes', {
    method: 'POST',
    body: formData  // FormData, không set Content-Type
});

const result = await response.json();
if (result.success) {
    console.log('✅ Uploaded quiz:', result.data);
} else {
    console.error('❌ Error:', result.message);
}
```

### 4. PUT with JSON (Update)

```javascript
// Update exam answers
const response = await fetch('/api/results/123', {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        status: 'SUBMITTED',
        answers: [
            { question_id: 1, user_answer: 'A' },
            { question_id: 2, user_answer: 'B' }
        ]
    })
});

const result = await response.json();
```

### 5. DELETE Request

```javascript
// Delete a quiz
const response = await fetch('/api/quizzes/15', {
    method: 'DELETE'
});

const result = await response.json();
if (result.success) {
    console.log('✅ Quiz deleted');
}
```

---

## Backend Receiving Data

### Flask (Python)

#### GET Request - Query Parameters

```python
# Frontend: GET /api/quizzes?limit=10&offset=0
# Backend:

@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    limit = request.args.get('limit', default=50, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    quizzes = Quiz.query.limit(limit).offset(offset).all()
    
    return {
        'success': True,
        'data': [q.to_dict() for q in quizzes]
    }
```

#### POST Request - JSON Body

```python
# Frontend: POST /api/sessions
# Body: { "quiz_id": 1, "num_questions": 20 }

@app.route('/api/sessions', methods=['POST'])
def create_session():
    data = request.get_json()
    
    quiz_id = data.get('quiz_id')
    num_questions = data.get('num_questions')
    
    session = Session(quiz_id=quiz_id, num_questions=num_questions)
    db.session.add(session)
    db.session.commit()
    
    return {
        'success': True,
        'data': {
            'session_id': session.id,
            'quiz_id': session.quiz_id
        }
    }, 201
```

#### POST Request - FormData (File Upload)

```python
# Frontend: POST /api/quizzes
# Body: FormData { quiz_name: "...", file: <File> }

@app.route('/api/quizzes', methods=['POST'])
def upload_quiz():
    quiz_name = request.form.get('quiz_name')
    file = request.files['file']
    
    # Validate
    if not file or not file.filename.endswith(('.xlsx', '.xls')):
        return {
            'success': False,
            'error_code': 'ERR_INVALID_FILE_TYPE',
            'message': 'Only .xlsx/.xls files allowed'
        }, 400
    
    # Process file → Extract questions → Save to DB
    quiz = Quiz(name=quiz_name)
    # ... process file ...
    db.session.add(quiz)
    db.session.commit()
    
    return {
        'success': True,
        'data': {
            'quiz_id': quiz.id,
            'quiz_name': quiz.name
        }
    }, 201
```

#### PUT Request - JSON Body

```python
# Frontend: PUT /api/results/123
# Body: { "status": "SUBMITTED", "answers": [...] }

@app.route('/api/results/<int:result_id>', methods=['PUT'])
def update_result(result_id):
    data = request.get_json()
    
    result = ExamResult.query.get(result_id)
    result.status = data.get('status')
    
    # Save answers
    for answer_data in data.get('answers', []):
        answer = UserAnswer(
            result_id=result_id,
            question_id=answer_data['question_id'],
            user_answer=answer_data['user_answer']
        )
        db.session.add(answer)
    
    db.session.commit()
    
    return {
        'success': True,
        'data': result.to_dict()
    }
```

---

## QuizGenerator Examples

### Full Flow: User Login → Upload Quiz → Share Data Automatically

```
Step 1: LOGIN
────────────
Frontend:
  POST /api/login
  Body: { username, password }
  
Backend:
  ✅ Verify username/password
  session['user_id'] = 42
  Response: Set-Cookie: session_id=xyz789

Browser: Lưu cookie session_id=xyz789 trong storage


Step 2: UPLOAD QUIZ (sau when already logged in)
───────────────────
Frontend:
  POST /api/quizzes
  formData: { quiz_name, file }
  ⭐ credentials: 'include' (gửi cookies)
  
Request gửi:
  POST /api/quizzes
  FormData: { quiz_name, file }
  Cookie: session_id=xyz789  ← Browser tự thêm!
  
Backend:
  user_id = session.get('user_id')  # = 42 (từ cookie)
  quiz = Quiz(name='Math', user_id=42)  # ⭐ Gắn user_id
  return quiz
  
Response:
  { success: true, data: { quiz_id: 15, quiz_name: 'Math' } }


Step 3: GET QUIZZES (multiple calls, many users online)
─────────────────────
User A:
  GET /api/quizzes
  Cookie: session_id=aaa  → BE biết user_id=10
  ← Return: quizzes của user #10

User B:
  GET /api/quizzes
  Cookie: session_id=bbb  → BE biết user_id=20
  ← Return: quizzes của user #20

User C:
  GET /api/quizzes
  Cookie: session_id=ccc  → BE biết user_id=30
  ← Return: quizzes của user #30

⭐ Tất cả đều request same URL, nhưng mỗi user nhận data riêng!
```

### Example 1: Upload Quiz (File + Text)

**Frontend HTML:**
```html
<form id="uploadForm">
    <input id="quizNameInput" type="text" placeholder="Quiz name" required>
    <input id="excelFileInput" type="file" accept=".xlsx,.xls" required>
    <button type="submit">Upload</button>
</form>
```

**Frontend JavaScript:**
```javascript
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const quizName = document.getElementById('quizNameInput').value;
    const file = document.getElementById('excelFileInput').files[0];
    
    // Validate
    if (!quizName || !file) {
        alert('Please fill all fields');
        return;
    }
    
    // Create FormData
    const formData = new FormData();
    formData.append('quiz_name', quizName);
    formData.append('file', file);
    
    try {
        // Send to backend
        const response = await fetch('/api/quizzes', {
            method: 'POST',
            body: formData,
            credentials: 'include'  // ⭐ Send cookies (user identification)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ Quiz uploaded!');
            window.location.href = '/list-quizzes';
        } else {
            alert('❌ Error: ' + result.message);
        }
    } catch (error) {
        alert('❌ Network error: ' + error.message);
    }
});
```

**Backend Python:**
```python
from flask import session

@app.route('/api/quizzes', methods=['POST'])
def upload_quiz():
    try:
        # ⭐ Extract user from cookie/session
        user_id = session.get('user_id')
        if not user_id:
            return {'success': False, 'error_code': 'ERR_NOT_LOGGED_IN', 'message': 'Please login first'}, 401
        
        quiz_name = request.form.get('quiz_name')
        file = request.files['file']
        
        # Validate
        if not quiz_name:
            return {'success': False, 'error_code': 'ERR_MISSING_NAME', 'message': 'Quiz name required'}, 400
        
        if not file or not file.filename.endswith(('.xlsx', '.xls')):
            return {'success': False, 'error_code': 'ERR_INVALID_FILE', 'message': 'Only .xlsx/.xls files'}, 400
        
        # Parse Excel → Create Quiz + Questions
        # ⭐ Associate quiz with current user
        quiz = create_quiz_from_excel(quiz_name, file, user_id=user_id)
        
        return {
            'success': True,
            'data': {'quiz_id': quiz.id, 'quiz_name': quiz.name}
        }, 201
        
    except Exception as e:
        return {'success': False, 'error_code': 'ERR_SERVER', 'message': str(e)}, 500
```

### Example 2: Load Questions (GET)

**Frontend JavaScript:**
```javascript
async function loadQuestions(sessionId) {
    try {
        const response = await fetch(`/api/sessions/${sessionId}/questions`, {
            credentials: 'include'  // ⭐ Send cookies
        });
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message);
        }
        
        // Display questions
        const questions = result.data;
        questions.forEach(q => {
            renderQuestion(q);
        });
        
    } catch (error) {
        console.error('Failed to load:', error);
    }
}
```

**Backend Python:**
```python
@app.route('/api/sessions/<int:session_id>/questions', methods=['GET'])
def get_session_questions(session_id):
    # ⭐ Get current user from cookie
    user_id = session.get('user_id')
    if not user_id:
        return {'success': False, 'message': 'Not logged in'}, 401
    
    # ⭐ Verify user owns this session
    session_obj = Session.query.get(session_id)
    if not session_obj or session_obj.user_id != user_id:
        return {'success': False, 'error_code': 'ERR_FORBIDDEN', 'message': 'Access denied'}, 403
    
    questions = session_obj.questions
    
    return {
        'success': True,
        'data': [q.to_dict() for q in questions]
    }
```

### Example 3: Submit Answers (PUT/POST)

**Frontend JavaScript:**
```javascript
async function submitAnswers(sessionId, answers) {
    try {
        const response = await fetch(`/api/sessions/${sessionId}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                answers: answers  // [{question_id, user_answer}, ...]
            }),
            credentials: 'include'  // ⭐ Send cookies
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message);
        }
        
        // Show results
        alert('✅ Submitted! Results:');
        window.location.href = `/results/${result.data.result_id}`;
        
    } catch (error) {
        alert('❌ Error: ' + error.message);
    }
}
```

**Backend Python:**
```python
@app.route('/api/sessions/<int:session_id>/submit', methods=['POST'])
def submit_session(session_id):
    # ⭐ Get current user from cookie
    user_id = session.get('user_id')
    if not user_id:
        return {'success': False, 'message': 'Not logged in'}, 401
    
    # ⭐ Verify user owns this session
    session_obj = Session.query.get(session_id)
    if not session_obj or session_obj.user_id != user_id:
        return {'success': False, 'message': 'Access denied'}, 403
    
    data = request.get_json()
    
    # Create result (associated with user)
    result = ExamResult.create(session_obj, user_id=user_id)
    
    # Save answers
    for answer_data in data.get('answers', []):
        UserAnswer.create(
            result_id=result.id,
            question_id=answer_data['question_id'],
            user_answer=answer_data['user_answer']
        )
    
    # Calculate score
    result.calculate_score()
    db.session.commit()
    
    return {
        'success': True,
        'data': {
            'result_id': result.id,
            'score': result.score,
            'status': result.status
        }
    }
```

---

## Common Patterns

### Error Handling Pattern

**Frontend:**
```javascript
async function apiCall(method, endpoint, data = null) {
    try {
        const options = {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'  // ⭐ Always send cookies for auth
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(endpoint, options);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message);
        }
        
        return result.data;
        
    } catch (error) {
        console.error('API Error:', error);
        showMessage('❌ ' + error.message, 'error');
        throw error;
    }
}

// Usage:
const quiz = await apiCall('GET', '/api/quizzes/1');
const session = await apiCall('POST', '/api/sessions', { quiz_id: 1 });
```

**Backend:**
```python
def error_response(error_code, message, status_code):
    return {
        'success': False,
        'error_code': error_code,
        'message': message,
        'data': None
    }, status_code

def success_response(data, status_code=200):
    return {
        'success': True,
        'error_code': None,
        'message': 'Success',
        'data': data
    }, status_code

# Usage:
if not quiz:
    return error_response('ERR_NOT_FOUND', 'Quiz not found', 404)

return success_response({'quiz_id': 1, 'name': 'Math'})
```

### Request/Response Debugging

**Frontend:**
```javascript
// Log tất cả requests
const originalFetch = window.fetch;
window.fetch = function(...args) {
    console.log('📤 Request:', args[0], args[1]);
    
    return originalFetch.apply(this, args)
        .then(response => {
            console.log('📥 Response:', response.status);
            return response;
        });
};
```

**Backend Flask:**
```python
@app.before_request
def log_request():
    print(f'📤 {request.method} {request.path}')
    print(f'   Headers: {dict(request.headers)}')
    if request.is_json:
        print(f'   Body: {request.get_json()}')

@app.after_request
def log_response(response):
    print(f'📥 Response: {response.status_code}')
    return response
```

---

## Tóm Tắt

**Frontend → Backend Communication:**
1. Frontend tạo HTTP request (GET/POST/PUT/DELETE)
2. Gửi qua network với dữ liệu (JSON/FormData)
3. **Browser tự động gửi Cookies** (user identification)
4. Backend nhận, đọc cookies → biết user nào
5. Backend xử lý dữ liệu của user đó
6. Backend gửi response (status + JSON data)
7. Frontend parse JSON, update UI

**Cách truyền dữ liệu:**
- **GET**: Query parameters (`?key=value`) + Cookies (tự động)
- **POST/PUT**: Body (JSON hoặc FormData) + Cookies (tự động)
- **Response**: JSON với `{success, error_code, message, data}`

**User Identification Flow:**
```
User A Login → Server set Cookie (session_id=aaa)
User B Login → Server set Cookie (session_id=bbb)

User A: fetch('/api/quizzes') 
  → Browser gửi Cookie: session_id=aaa
  → Backend: user_id = session['user_id'] = 10
  → Return quizzes của user #10

User B: fetch('/api/quizzes')
  → Browser gửi Cookie: session_id=bbb
  → Backend: user_id = session['user_id'] = 20
  → Return quizzes của user #20

⭐ Cùng URL, nhưng khác user → khác data được gửi!
```

**Best Practices:**
- ✅ Always use `credentials: 'include'` in fetch (send cookies)
- ✅ Validate user ownership (check `user_id` from session)
- ✅ Validate ở FE (UX tốt) + BE (security)
- ✅ Clear error messages + error codes
- ✅ Consistent response format
- ✅ Proper HTTP status codes
- ✅ Async/await + try/catch error handling
- ✅ Use HttpOnly cookies (prevent JS access)
