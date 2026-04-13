---
date: 2026-04-10 14:00
summary: Hướng dẫn phân tích API thông qua Browser Developer Tools (F12) - các tab chính, thông tin mỗi tab, và cách đọc request/response
---

## Mục Lục
- [Cách mở Developer Tools](#cach-mo-developer-tools)
- [Tab Console](#tab-console)
- [Tab Sources](#tab-sources)
- [Tab Network (QUAN TRỌNG NHẤT)](#tab-network-quan-trong-nhat)
- [Tab Elements/Inspector](#tab-elementsinspector)
- [Tab Application](#tab-application)
- [Quy trình phân tích API](#quy-trinh-phan-tich-api)
- [Ví dụ thực tế](#vi-du-thuc-te)

---

## Cách mở Developer Tools

### Windows/Linux:
- Nhấn `F12` (nhanh nhất)
- Hoặc: `Ctrl + Shift + I`

### macOS:
- `Cmd + Option + I`

Giao diện Developer Tools sẽ mở ở dưới cùng hoặc bên cạnh trình duyệt.

---

## Tab Console

**Đây là nơi xem lỗi JavaScript và kết quả console.log()**

### Thông tin được hiển thị:
- **Error messages** (lỗi đỏ): Xảy ra khi code bị lỗi
- **Warning messages** (cảnh báo vàng): Cảnh báo tiềm tàng
- **Info messages** (xanh lam): Thông tin từ `console.log()`, `console.info()`
- **Network logs**: Khi backend gửi thông tin qua console

### Cách sử dụng:
```javascript
// Developer được gửi từ backend để debug
console.log('Quiz data:', quizData);
console.error('Failed to fetch quiz:', error);
```

**Công dụng khi phân tích API**: Xem lỗi JavaScript, giá trị biến, log từ code Frontend

---

## Tab Sources

**Đây là nơi xem và debug code JavaScript**

### Thông tin được hiển thị:
- **Danh sách file JS**: Tất cả file JavaScript được tải
- **Breakpoints**: Điểm dừng để debug (nhấn số dòng)
- **Call stack**: Đống gọi hàm hiện tại
- **Variables**: Giá trị các biến tại breakpoint
- **Watch expressions**: Theo dõi biến cụ thể

### Cách sử dụng:
1. Nhấn vào số dòng → Đặt breakpoint (dấu chấm đỏ)
2. Tương tác trang web → Code sẽ dừng tại breakpoint
3. Xem giá trị biến, step through code

**Công dụng khi phân tích API**: Xem request được tạo ra như thế nào, biến nào được gửi

---

## Tab Network (QUAN TRỌNG NHẤT)

**Đây là tab CHÍNH để phân tích API - xem tất cả requests/responses**

### Bước 1: Kích hoạt Network Tab
1. Mở Developer Tools (F12)
2. Chọn tab **Network**
3. Trang sẽ tự động clear requests cũ
4. Tương tác trang web (submit form, click button, vv)
5. Bạn sẽ thấy các requests xuất hiện trong danh sách

### Bước 2: Loại requests được hiển thị
Cột **Type** cho biết loại request:
- **xhr** (XMLHttpRequest): API request từ JavaScript, quan trọng nhất ✓
- **fetch**: API request dùng Fetch API (cũng quan trọng) ✓
- **document**: Tải trang HTML chính
- **stylesheet**: File CSS
- **script**: File JavaScript
- **image**: Ảnh
- **font**: Font chữ
- **manifest**: Web app manifest

**Mẹo**: Bạn chỉ cần chú ý **xhr** và **fetch** khi phân tích API

### Bước 3: Cột thông tin chính
Khi xem danh sách requests:

| Cột | Ý nghĩa |
|-----|---------|
| **Name** | Tên endpoint API, ví dụ: `/api/quiz/submit` |
| **Status** | Mã HTTP: 200 (OK), 400 (lỗi client), 500 (lỗi server) |
| **Type** | xhr, fetch, document, vv |
| **Initiator** | File nào đã gửi request này |
| **Size** | Kích thước response (ví dụ: 1.2 KB) |
| **Time** | Thời gian response (ví dụ: 45ms) |

### Bước 4: Chi tiết từng Request - Tab "Headers"

Nhấn vào 1 request → Chọn tab **Headers** để xem:

#### Request Headers (Gửi đi):
```
Host: example.com
Method: POST                      // Phương thức: GET, POST, PUT, DELETE
URL: https://example.com/api/quiz/submit
Content-Type: application/json    // Loại dữ liệu: JSON
Authorization: Bearer token123    // Token xác thực (nếu có)
```

#### Response Headers (Nhận về):
```
Content-Type: application/json
Content-Length: 256              // Kích thước response
Set-Cookie: sessionId=abc123     // Cookie được set
Status Code: 200 OK
```

**Công dụng**: Kiểm tra headers đúng chưa, authorization có không

### Bước 5: Chi tiết Request - Tab "Payload" hoặc "Request Body"

**Payload** = Dữ liệu gửi từ Frontend → Backend

Ví dụ:
```json
{
  "quizId": "q123",
  "answers": ["A", "B", "D"],
  "timeSpent": 120,
  "userId": "user456"
}
```

**Công dụng**: Kiểm tra dữ liệu gửi đi có đúng không, có bị thiếu field nào không

### Bước 6: Chi tiết Response - Tab "Response" hoặc "Preview"

**Response** = Dữ liệu nhận về từ Backend → Frontend

Ví dụ:
```json
{
  "success": true,
  "score": 85,
  "totalQuestions": 10,
  "correctAnswers": 8,
  "message": "Quiz submitted successfully"
}
```

**Preview tab**: Hiển thị response dưới dạng JSON đẹp mắt
**Response tab**: Hiển thị raw response

**Công dụng**: Kiểm tra backend trả về response đúng không, có dữ liệu đúng không

---

## Tab Elements/Inspector

**Đây là nơi xem và sửa HTML, CSS của trang**

### Thông tin được hiển thị:
- **HTML tree**: Cấu trúc HTML của trang
- **CSS styles**: Các style áp dụng cho element
- **Attributes**: Các thuộc tính của element (id, class, data-vv)
- **Event listeners**: Các event bắt trên element

### Cách sử dụng:
1. Nhấn icon select (mũi tên góc trái)
2. Click vào element trên trang
3. Xem HTML và CSS của element đó

**Công dụng khi phân tích API**: 
- Kiểm tra form fields có đúng name không
- Xem data attributes có chứa thông tin dùng cho API không
- Xem event listeners để biết hàm JS nào xử lý

---

## Tab Application

**Đây là nơi xem storage: Cookies, LocalStorage, SessionStorage**

### Cookies (Lưu trữ nhỏ, gửi tự động với API)
```
Path: /
Domain: example.com
Expires: Thu Apr 10 2026
Value: sessionId=abc123xyz
```

**Công dụng**: Kiểm tra session cookie, check token trong cookie

### LocalStorage (Lưu trữ lớn, ko gửi tự động)
```javascript
localStorage.getItem('userToken')    // Lấy giá trị
localStorage.setItem('key', 'value') // Lưu giá trị
```

**Công dụng**: Xem token lưu trong localStorage, biến global lưu

### SessionStorage (Giống localStorage nhưng xóa khi đóng browser)
```javascript
sessionStorage.getItem('tempData')
```

**Công dụng**: Xem dữ liệu tạm của session

---

## Quy trình phân tích API

### Bước 1: Mở F12 → Network tab

### Bước 2: Clear requests cũ
Nhấn nút "clear" (biểu tượng trong Network tab)

### Bước 3: Kích hoạt action trên trang
- Submit form
- Click nút "Save"
- Click nút "Delete"
- Scroll page (nếu có pagination API)

### Bước 4: Xem request xuất hiện
Type = **xhr** hoặc **fetch**

### Bước 5: Nhấn vào request → Xem chi tiết

**Headers tab:**
- Method (GET, POST, vv)?
- URL là gì?
- Có authorization header không?
- Content-Type là gì?

**Payload/Request tab:**
- Dữ liệu gửi đi là gì?
- Có thiếu field nào không?
- Dữ liệu format đúng không (JSON)?

**Response tab:**
- Status code = bao nhiêu?
- Response format là gì (JSON)?
- Có lỗi từ backend không?
- Dữ liệu trả về đúng không?

### Bước 6: So sánh với documentation
- URL endpoint có match docs không?
- Method có đúng không?
- Request fields có match không?
- Response format có match không?

---

## Ví dụ thực tế

### Ví dụ 1: Phân tích API Submit Quiz

#### Bước 1-3: Tương tác trang
Người dùng điền câu trả lời → Nhấn "Submit Quiz"

#### Bước 4: Xem request
Trong Network tab, thấy request:
```
POST /api/quizzes/q123/submit
```

#### Bước 5: Xem Headers
```
Method: POST
URL: http://localhost:5000/api/quizzes/q123/submit
Content-Type: application/json
```

#### Bước 6: Xem Request Body (Payload)
```json
{
  "answers": {
    "q1": "A",
    "q2": "C",
    "q3": "B"
  },
  "timeSpent": 180
}
```

#### Bước 7: Xem Response
```json
{
  "success": true,
  "score": 90,
  "totalQuestions": 3,
  "correctAnswers": 3
}
```

**Kết luận:**
- ✓ API endpoint là `/api/quizzes/{quizId}/submit`
- ✓ Method: POST
- ✓ Request body: answers object + timeSpent
- ✓ Response: success flag + score info

---

### Ví dụ 2: Debug lỗi API

#### Tương tác trang → Request gửi → Nhận response error

#### Network tab hiển thị:
```
POST /api/quizzes/submit [Status: 400 Bad Request]
```

#### Mở request → Payload tab:
```json
{
  "answers": {},
  "timeSpent": 0
}
```

#### Mở response tab:
```json
{
  "error": "Answers are required",
  "code": "VALIDATION_ERROR"
}
```

**Vấn đề**: Frontend không gửi answers, backend reject

**Cách fix**: Kiểm tra JavaScript capture answers từ form

---

## Mẹo và thủ thuật

### 1. Filter requests
Được lọc theo type: XHR, CSS, JS, etc. Chỉ xem "XHR/fetch" để phân tích API

### 2. Xem request mạng slow
Nếu query nhanh, sử dụng "Throttling" → Chọn "Slow 3G" để thấy rõ timing

### 3. Copy request dưới dạng cURL
Nhấp phải vào request → "Copy as cURL" → Dùng để test API từ Terminal

### 4. Preserve logs
Nhấn option "Preserve log" → Logs không bị clear khi navigate trang

### 5. Xem Time dùng để response
**Time column** = Tổng thời gian từ lúc gửi đến nhận response
- < 100ms: Rất nhanh
- 100-500ms: Bình thường
- > 1000ms: Cần optimize

---

## Tóm tắt các tab quan trọng

| Tab | Dùng để | Cần cho phân tích API |
|-----|---------|-------|
| **Network** | Xem requests/responses | ✓✓✓ QUAN TRỌNG |
| **Console** | Xem lỗi JS, debug value | ✓ Useful |
| **Elements** | Xem HTML, CSS | ✓ Thỉnh thoảng |
| **Sources** | Debug code JS | ✓ Thỉnh thoảng |
| **Application** | Xem Cookies, LocalStorage | ✓ Check authentication |

---

## Ứng dụng thực tế vào QuizGenerator

Khi muốn biết API của QuizGenerator hoạt động thế nào:

1. **Mở F12 → Network tab**
2. **Tương tác trang**: Upload excel, submit quiz, vv
3. **Xem requests xuất hiện**: 
   - POST /upload (upload file)
   - GET /api/quiz/{id} (lấy quiz)
   - POST /api/submit (submit answers)
4. **Kiểm tra từng request**: Headers, Payload, Response
5. **So sánh với code BE** (app.py, routes/quiz.py) để hiểu logic

Ví dụ: Nếu thấy request gửi `{"answers": {...}}` nhưng response lỗi, có thể BE expects format khác → kiểm tra `routes/quiz.py` request.json validation
