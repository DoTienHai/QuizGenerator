# API: Kiến Thức Cơ Bản & Cách Thiết Kế

**Ngày tạo**: 2026-03-15  
**Mục đích**: Ghi chép kiến thức về API và best practices thiết kế API

---

## Mục Lục
- [API là gì?](#1-api-la-gi)
- [Loại API](#2-loai-api)
- [HTTP Methods](#3-http-methods-verbs)
- [HTTP Status Codes](#4-http-status-codes)
- [Request & Response Structure](#5-request--response-structure)
- [Response Format](#6-response-format---best-practice)
- [API Design Best Practices](#7-api-design-best-practices)
- [API Development Workflow](#8-api-development-workflow)
- [Cách Test API](#9-cach-test-api)
- [Common Mistakes](#10-common-api-mistakes--solutions)
- [QuizGenerator API Summary](#11-quizgenerator-api-summary)
- [Key Takeaways](#12-key-takeaways)

---

## 1. API là gì?

**API** = Application Programming Interface

**Định nghĩa**: Một bộ quy tắc và giao thức cho phép các ứng dụng giao tiếp với nhau.

**Ví dụ thực tế**:
- Frontend (browser) gửi request → Backend (server)
- Backend xử lý → trả response JSON
- Frontend nhận dữ liệu → hiển thị trên giao diện

**Trong QuizGenerator**:
- Frontend (HTML/JS) gọi API
- Backend (Flask) xử lý logic
- Trả JSON response

---

## 2. Loại API

### 2.1 REST API (RESTful)
**Phổ biến nhất, được dùng trong QuizGenerator**

#### Định Nghĩa
**REST** = **RE**presentational **S**tate **T**ransfer

REST API là cách thiết kế API dựa trên **nguyên tắc client-server** sử dụng **HTTP protocol**:
- **Client**: Frontend (HTML/JS) hoặc bất kỳ app nào
- **Server**: Backend (Flask, Node.js, Python, etc)
- **HTTP**: Giao thức truyền dữ liệu qua internet

#### Nguyên Tắc REST (6 Constraints)

1. **Client-Server Architecture**
   - Client & Server độc lập
   - Frontend không cần biết backend implement thế nào
   - Backend không cần biết frontend hiển thị thế nào

2. **Statelessness** (Không lưu trạng thái)
   - Mỗi request là **độc lập toàn bộ**
   - Server không lưu session từ request trước
   - Mỗi request phải có **đủ thông tin** để server xử lý
   
   **Ví dụ**:
   ```
   Request 1: GET /api/quizzes/1
   Server không nhớ request 1
   
   Request 2: GET /api/sessions/5
   Server không biết client vừa request quiz 1 ở trước
   Mỗi request là mới, độc lập
   ```

3. **Uniform Interface** (Giao diện chuẩn)
   - Tất cả resources đều có cách sử dụng **giống nhau**
   - Sử dụng **HTTP methods** cho hành động
   - Sử dụng **URLs** cho tài nguyên (resources)
   
   **Ví dụ**:
   ```
   Cách tạo Quiz:    POST /api/quizzes
   Cách tạo Session: POST /api/sessions
   Cách tạo Result:  POST /api/results
   
   Tất cả đều follow: POST + URL → tạo resource mới
   ```

4. **Resource-Based URLs**
   - URL đại diện cho **resource** (tài nguyên), không đại diện cho **action**
   
   **✅ Tốt (RESTful)**:
   ```
   GET    /api/quizzes           → Resource: quizzes
   GET    /api/quizzes/1         → Resource: quiz với id=1
   POST   /api/quizzes           → Tạo quiz (action được suy ra từ POST method)
   DELETE /api/quizzes/1         → Xóa quiz 1 (action được suy ra từ DELETE method)
   ```
   
   **❌ Tệ (không RESTful)**:
   ```
   GET /api/getAllQuizzes        → Action trong URL
   GET /api/getQuizById?id=1     → Action trong URL
   POST /api/createQuiz          → Action trong URL
   GET /api/deleteQuiz?id=1      → Action trong URL (sai, DELETE phải là method)
   ```

5. **Representational** (Biểu diễn dữ liệu)
   - Resources được biểu diễn dưới dạng **JSON** (hoặc XML, HTML)
   - Response là **trạng thái hiện tại** của resource
   
   **Ví dụ**:
   ```json
   // Response của GET /api/quizzes/1
   {
     "quiz_id": 1,
     "total_questions": 50,
     "name": "Sample Quiz",
     "uploaded_at": "2026-03-15T10:30:00Z"
   }
   // Đây là "state" (trạng thái) hiện tại của quiz id=1
   ```

6. **Cacheability** (Có thể cache)
   - Response có thể cache để giảm tải server
   - Sử dụng HTTP cache headers (Cache-Control, ETag, etc)

#### Đặc Điểm REST API
- ✅ Dùng **HTTP methods** (GET, POST, PUT, DELETE, PATCH)
- ✅ Response format: **JSON** (hoặc XML)
- ✅ **Stateless** (không lưu session)
- ✅ **Dễ hiểu** (đơn giản, logic)
- ✅ **Dễ implement** (tiêu chuẩn)
- ✅ **Chuẩn hóa** (theo quy tắc REST)

#### So Sánh: REST API vs Non-REST API

**REST API** ✅:
```
GET    /api/quizzes              → Lấy danh sách quiz
GET    /api/quizzes/1            → Lấy chi tiết quiz 1
POST   /api/quizzes              → Tạo quiz mới
PUT    /api/quizzes/1            → Cập nhật toàn bộ quiz 1
PATCH  /api/quizzes/1            → Cập nhật một phần quiz 1
DELETE /api/quizzes/1            → Xóa quiz 1
```

**Non-REST API (RPC style)** ❌:
```
GET /api/getQuizzes                   → Phải gọi function
POST /api/getQuizById?id=1            → GET trong query string (không dùng method)
POST /api/createQuiz                  → Action trong URL
POST /api/updateQuiz?id=1             → Action trong URL
POST /api/deleteQuiz?id=1             → DELETE dùng POST method
```

#### Ví Dụ Thực Tế: QuizGenerator
```
Tạo phiên thi mới:
- URL: /api/sessions (resource = sessions)
- Method: POST (action = create, suy ra từ method)
- Request body:
  {
    "quiz_id": 1,
    "num_questions": 20,
    "exam_duration": 60
  }
- Response (201 Created):
  {
    "session_id": 123,
    "status": "active"
  }

Lấy chi tiết phiên thi:
- URL: /api/sessions/123 (resource = session với id=123)
- Method: GET (action = read, suy ra từ method)
- Response (200 OK):
  {
    "session_id": 123,
    "quiz_id": 1,
    "status": "active",
    "created_at": "2026-03-15T10:30:00Z"
  }

Xóa phiên thi:
- URL: /api/sessions/123 (resource = session với id=123)
- Method: DELETE (action = delete, suy ra từ method)
- Response (204 No Content): Không có body
```

#### REST API vs GraphQL

| Aspect | REST API | GraphQL |
|--------|----------|---------|
| **Flexibility** | Cố định (server định nghĩa) | Linh hoạt (client chọn fields) |
| **Learning Curve** | Dễ học | Khó học |
| **Performance** | Over-fetching* | Optimal |
| **Caching** | Dễ | Khó |
| **Use Case** | Thường dùng | APIs phức tạp |

*Over-fetching = Lấy quá nhiều dữ liệu không cần

#### REST API Maturity Model (Richardson)

**Level 0**: Chỉ dùng HTTP (RPC style - không phải REST)
```
POST /api/call?method=getQuizzes
POST /api/call?method=createSession
```

**Level 1**: Dùng Resources (URLs)
```
GET  /api/quizzes
GET  /api/sessions
```

**Level 2**: Dùng HTTP Methods (GET, POST, PUT, DELETE)
```
GET    /api/quizzes
POST   /api/quizzes
PUT    /api/quizzes/1
DELETE /api/quizzes/1
```

**Level 3**: Dùng HATEOAS (Hypertext As The Engine Of Application State)
```json
{
  "quiz_id": 1,
  "name": "Sample",
  "_links": {
    "self": { "href": "/api/quizzes/1" },
    "update": { "href": "/api/quizzes/1", "method": "PUT" },
    "delete": { "href": "/api/quizzes/1", "method": "DELETE" }
  }
}
```

**QuizGenerator** đang ở **Level 2** (Dùng HTTP Methods), đủ cho hầu hết ứng dụng.

### 2.2 GraphQL
- Query ngôn ngữ linh hoạt
- Frontend chỉ lấy dữ liệu cần thiết
- Phức tạp hơn REST

### 2.3 SOAP
- Cũ, phức tạp
- Ít dùng trong ứng dụng hiện đại

---

## Thêm: FastAPI là gì? Tại sao không được list?

### FastAPI Định Nghĩa

**FastAPI** không phải là **loại API**, mà là **framework** (khung công tác) để xây dựng **REST API**.

**Phân biệt**:
- **Loại API**: REST, GraphQL, SOAP, gRPC (cách thiết kế + giao thức)
- **Framework**: Flask, FastAPI, Django, Node.js, Spring (công cụ để xây dựng API)

**Tương tự**:
```
REST API     = Kiến trúc nhà
Flask/FastAPI = Công cụ xây nhà

GraphQL      = Kiến trúc nhà khác
FastAPI      = Vẫn là công cụ xây nhà

Bạn có thể dùng Flask OR FastAPI để xây cả REST hay GraphQL
```

### FastAPI là gì?

**FastAPI** là **web framework hiện đại** (2018) để xây dựng **REST APIs** bằng Python:
- **Modern**: Sử dụng Python 3.6+ features (async/await, type hints)
- **Fast**: Tốc độ xử lý nhanh nhất (gần với Node.js, Go)
- **Automatic Documentation**: Tự generate documentation (Swagger, ReDoc)
- **Type Hints**: Bắt buộc dùng type hints → dễ validate input
- **Async**: Hỗ trợ async/await → xử lý concurrent requests tốt hơn

### So Sánh: Flask vs FastAPI

| Aspect | Flask | FastAPI |
|--------|-------|---------|
| **Năm ra mắt** | 2010 | 2018 |
| **Tốc độ** | Chậm | Nhanh |
| **Type Hints** | Không bắt buộc | Bắt buộc |
| **Auto Documentation** | Không | Có (Swagger, ReDoc) |
| **Async Support** | Có nhưng khó | Dễ, native |
| **Learning Curve** | Dễ | Trung bình |
| **Popularity** | Rất phổ biến | Đang tăng |
| **Use Case** | Tất cả | Modern APIs |

### Ví Dụ: Flask vs FastAPI

**Flask** (dùng trong QuizGenerator):
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    # Không bắt buộc type hints
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(quiz.to_dict()), 200
```

**FastAPI** (hiện đại hơn):
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Định nghĩa response model
class QuizResponse(BaseModel):
    quiz_id: int
    total_questions: int
    name: str

@app.get('/api/quizzes/{quiz_id}', response_model=QuizResponse)
async def get_quiz(quiz_id: int):  # Type hints bắt buộc
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail='Quiz not found')
    return quiz

# FastAPI tự động:
# - Validate input type (quiz_id phải là int)
# - Validate output type (trả về QuizResponse)
# - Generate Swagger docs tại /docs
# - Generate ReDoc tại /redoc
```

### Lợi Điểm FastAPI

✅ **Tự động documentation**: API docs được generate tự động
```
http://localhost:8000/docs        → Swagger UI (interactive)
http://localhost:8000/redoc       → ReDoc (static)
```

✅ **Type safety**: Bắt lỗi type sớm
```python
@app.get('/api/sessions/{session_id}')
async def get_session(session_id: int):  # Nếu gửi string → lỗi
    return {...}

# GET /api/sessions/abc → Lỗi 422 (validation error)
# GET /api/sessions/123 → OK
```

✅ **Auto validation**: Input validation tự động
```python
class SessionRequest(BaseModel):
    quiz_id: int  # Phải là số
    num_questions: int = 10  # Default 10
    exam_duration: int  # Phải có

# POST /api/sessions với {"quiz_id": "abc"} → Lỗi validation
# POST /api/sessions với {"quiz_id": 1, "exam_duration": 60} → OK
```

✅ **Async**: Xử lý concurrent requests tốt hơn
```python
@app.get('/api/quizzes/{quiz_id}')
async def get_quiz(quiz_id: int):  # async function
    # Có thể await database calls
    quiz = await db.get_quiz(quiz_id)
    return quiz
```

### Nhược Điểm FastAPI

❌ **Learning curve**: Cần hiểu type hints, async/await
❌ **Overkill cho app nhỏ**: Flask đơn giản hơn
❌ **Ít template support**: FastAPI tập trung API, không HTML templates

### Tại Sao QuizGenerator Dùng Flask?

1. **App đơn giản**: Không cần performance tối ưu
2. **Dễ học**: Mới bắt đầu, Flask dễ tiếp cận hơn
3. **Đủ dùng**: Flask + SQLAlchemy đủ cho MVP
4. **Linh hoạt**: Flask cho phép mix HTML templates + APIs

### Khi Nào Dùng FastAPI?

✅ **Dùng FastAPI khi**:
- Cần performance cao
- API phức tạp nhiều endpoints
- Team muốn type safety
- Cần auto documentation
- Xây dựng microservices

❌ **Dùng Flask khi**:
- App nhỏ, đơn giản
- Mới bắt đầu học web dev
- Cần flexibility cao
- Mix HTML templates + APIs

### Kết Luận

| Khái Niệm | Ví Dụ | Loại |
|-----------|-------|------|
| **Loại API** | REST, GraphQL, SOAP, gRPC | Cách thiết kế |
| **Framework** | Flask, FastAPI, Django, Express | Công cụ xây dựng |

**FastAPI không được list vì nó không phải loại API, mà là framework để xây REST APIs.**

Giống như:
- "Loại xe": Sedan, SUV, Truck (REST, GraphQL, SOAP)
- "Hãng sản xuất": Toyota, BMW, Ford (Flask, FastAPI, Django)

---

## 3. HTTP Methods (Verbs)

| Method | Mục đích | Body? | Idempotent? |
|--------|---------|-------|------------|
| **GET** | Lấy dữ liệu | Không | Có |
| **POST** | Tạo dữ liệu mới | Có | Không |
| **PUT** | Cập nhật toàn bộ | Có | Có |
| **PATCH** | Cập nhật một phần | Có | Có |
| **DELETE** | Xóa dữ liệu | Không | Có |

**Idempotent** = Gọi nhiều lần kết quả vẫn giống nhau

### Ví dụ:
```python
# GET - Lấy dữ liệu (không thay đổi dữ liệu)
GET /api/quizzes/1

# POST - Tạo mới (mỗi lần gọi tạo 1 record mới)
POST /api/sessions
Body: { "quiz_id": 1, "num_questions": 20 }

# PUT - Cập nhật toàn bộ
PUT /api/quizzes/1
Body: { "name": "New Name", "total_questions": 50 }

# DELETE - Xóa
DELETE /api/quizzes/1
```

---

## 4. HTTP Status Codes

| Code | Ý nghĩa | Ví dụ |
|------|---------|-------|
| **2xx - Success** | ✅ Thành công | |
| 200 | OK | GET, PUT, PATCH, DELETE thành công |
| 201 | Created | POST tạo resource thành công |
| 204 | No Content | DELETE thành công, không dữ liệu |
| **4xx - Client Error** | ❌ Lỗi client | |
| 400 | Bad Request | Dữ liệu input sai |
| 401 | Unauthorized | Chưa đăng nhập |
| 403 | Forbidden | Không có quyền |
| 404 | Not Found | Resource không tồn tại |
| 405 | Method Not Allowed | Method không được phép (VD: GET cho POST endpoint) |
| **5xx - Server Error** | ⚠️ Lỗi server | |
| 500 | Internal Server Error | Lỗi không xác định |
| 503 | Service Unavailable | Server đang bảo trì |

**Trong QuizGenerator**:
```python
# 200 - GET thành công
GET /api/quizzes → 200 OK

# 201 - POST tạo mới thành công
POST /api/sessions → 201 Created

# 404 - Resource không tìm thấy
GET /api/quizzes/999 → 404 Not Found

# 400 - Input không hợp lệ
POST /api/sessions với num_questions=100 (chỉ có 50) → 400 Bad Request
```

---

## 5. Request & Response Structure

### Request (Frontend → Backend)
```
HTTP Method + URL + Headers + Body

GET /api/quizzes/1
Headers:
  - Content-Type: application/json
  - Authorization: Bearer token...

Body: (không có cho GET)
```

```
POST /api/sessions
Headers:
  - Content-Type: application/json

Body (JSON):
{
  "quiz_id": 1,
  "num_questions": 20,
  "exam_duration": 60
}
```

### Response (Backend → Frontend)
```
HTTP Status Code + Headers + Body

Response:
Status: 201 Created
Headers:
  - Content-Type: application/json

Body (JSON):
{
  "status": "success",
  "data": {
    "session_id": 123,
    "questions": [...]
  }
}
```

---

## 6. Response Format - Best Practice

### Standard Response Structure
```json
{
  "status": "success|error",
  "data": { ... },
  "error": { ... }
}
```

### Success Response (200, 201)
```json
{
  "status": "success",
  "data": {
    "quiz_id": 1,
    "total_questions": 50,
    "uploaded_at": "2026-03-15T10:30:00Z"
  }
}
```

### Error Response (400, 404, 500)
```json
{
  "status": "error",
  "error": {
    "code": "QUIZ_NOT_FOUND",
    "message": "Quiz with ID 999 not found",
    "field": "quiz_id"
  }
}
```

---

## 7. API Design Best Practices

### 7.1 Naming Convention

✅ **Tốt** (RESTful):
```
GET    /api/quizzes              → Lấy danh sách
GET    /api/quizzes/1            → Lấy chi tiết 1
POST   /api/quizzes              → Tạo quiz
DELETE /api/quizzes/1            → Xóa quiz 1
```

❌ **Tệ** (không RESTful):
```
GET /api/getQuizzes
GET /api/getQuizById/1
POST /api/createQuiz
GET /api/deleteQuiz?id=1
```

**Quy tắc**:
- Dùng **danh từ** (nouns) cho resource: `/quizzes`, `/sessions`, `/results`
- Không dùng **động từ** (verbs): ~~`/getQuizzes`~~, ~~`/createSession`~~
- Dùng `/` để chỉ hierarchy: `/quizzes/1/results`

### 7.2 Pagination (khi dữ liệu nhiều)

```
GET /api/quizzes?limit=10&offset=0

Response:
{
  "data": [...],
  "total_count": 150,
  "limit": 10,
  "offset": 0
}
```

### 7.3 Filtering & Sorting

```
GET /api/quizzes?status=active&sort=uploaded_at&order=desc
```

### 7.4 Versioning (nếu có nhiều phiên bản)

```
GET /api/v1/quizzes      → Version 1
GET /api/v2/quizzes      → Version 2
```

### 7.5 Documentation

- Mỗi endpoint cần có:
  - Mục đích (Purpose)
  - HTTP Method
  - URL Path
  - Query parameters (nếu có)
  - Request body format
  - Response format (success & error)
  - Status codes có thể trả về

**Ví dụ** (từ SW2_API_Design.md):
```markdown
#### Endpoint: Create Exam Session

**Method**: POST
**URL**: /api/sessions

**Purpose**: Create new exam session with configuration

**Request**:
{
  "quiz_id": 1,
  "num_questions": 20,
  "exam_duration": 60
}

**Response (201)**:
{
  "status": "success",
  "data": { ... }
}

**Response (400)**:
{
  "status": "error",
  "error": { ... }
}
```

---

## 8. API Development Workflow

### Bước 1: Thiết kế API (Design Phase)
- Định nghĩa endpoints
- Định nghĩa request/response format
- Định nghĩa status codes
- Viết documentation

**Ví dụ**: [SW2_API_Design.md](../docs/SW2_API_Design.md)

### Bước 2: Implement Endpoints (Development Phase)
- File: `app.py`
- Định nghĩa routes
- Xử lý request/response

```python
@app.route('/api/sessions', methods=['POST'])
def create_session():
    data = request.get_json()
    # Xử lý logic
    return jsonify({...}), 201
```

### Bước 3: Testing
- Test mỗi endpoint
- Verify response format
- Check status codes
- Kiểm tra error handling

**Tools**: Postman, curl, Insomnia

### Bước 4: Documentation
- Cập nhật API docs
- Viết examples
- Hướng dẫn sử dụng

---

## 9. Cách Test API

### Cách 1: Browser (chỉ GET)
```
http://localhost:5000/api/quizzes
```

### Cách 2: curl (Terminal)
```bash
# GET
curl http://localhost:5000/api/quizzes

# POST
curl -X POST http://localhost:5000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"quiz_id": 1, "num_questions": 20, "exam_duration": 60}'
```

### Cách 3: Postman (Desktop App)
1. Mở Postman
2. Chọn HTTP Method (GET/POST/etc)
3. Nhập URL
4. Thêm Headers (nếu cần): `Content-Type: application/json`
5. Thêm Body (JSON) nếu POST/PUT
6. Click Send
7. Xem Response

### Cách 4: Python requests
```python
import requests

# GET
response = requests.get('http://localhost:5000/api/quizzes')
print(response.json())

# POST
response = requests.post('http://localhost:5000/api/sessions',
  json={
    "quiz_id": 1,
    "num_questions": 20,
    "exam_duration": 60
  }
)
print(response.status_code)
print(response.json())
```

---

## 10. Common API Mistakes & Solutions

### ❌ Lỗi 1: Endpoint naming không consistent
```
GET /api/quizzes
GET /api/get/session
POST /createExam
```
✅ Fix: `GET /api/quizzes`, `GET /api/sessions/1`, `POST /api/exams`

### ❌ Lỗi 2: Không có error handling
```python
@app.route('/api/sessions/<int:session_id>')
def get_session(session_id):
    session = Session.query.get(session_id)
    return jsonify(session.to_dict())  # Crash nếu không tìm thấy!
```

✅ Fix:
```python
session = Session.query.get(session_id)
if not session:
    return jsonify({'error': 'Not found'}), 404
return jsonify({...}), 200
```

### ❌ Lỗi 3: Không validate input
```python
POST /api/sessions
{
  "num_questions": 1000  # Vượt quá tổng số câu!
}
```

✅ Fix: Validate trước xử lý logic

### ❌ Lỗi 4: Response format không consistent
```
Response 1: { "data": {...} }
Response 2: { "result": {...} }
Response 3: {...}  (không wrap)
```

✅ Fix: Luôn trả về format chuẩn:
```
{ "status": "...", "data": {...}, "error": {...} }
```

---

## 11. QuizGenerator API Summary

**Base URL**: `http://localhost:5000/api`

**11 Endpoints**:

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 1 | POST | /quizzes/upload | Upload Excel |
| 2 | GET | /quizzes | List quizzes |
| 3 | GET | /quizzes/{id} | Get quiz detail |
| 4 | GET | /quizzes/{id}/results | Get quiz results |
| 5 | POST | /sessions | Create session |
| 6 | GET | /sessions/{id} | Get session |
| 7 | GET | /sessions/{id}/status | Check status |
| 8 | POST | /sessions/{id}/answers | Submit answers |
| 9 | POST | /sessions/{id}/submit | Final submit |
| 10 | POST | /sessions/{id}/auto-submit | Auto-submit |
| 11 | GET | /results/{id} | Get results |

---

## 12. Key Takeaways

1. **REST API** dùng HTTP methods + nouns (không dùng verbs)
2. **Status codes**: 2xx=success, 4xx=client error, 5xx=server error
3. **Request/Response**: JSON format, consistent structure
4. **Design trước**: Viết docs trước implement
5. **Validate input**: Luôn kiểm tra dữ liệu client gửi
6. **Error handling**: Trả về error response rõ ràng, không crash
7. **Documentation**: Viết hướng dẫn chi tiết cho từng endpoint
8. **Testing**: Test manual (Postman) + unit tests

