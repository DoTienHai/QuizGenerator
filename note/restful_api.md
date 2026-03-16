# RESTful API: Hiểu Rõ Về REST & RESTful

**Ngày tạo**: 2026-03-16  
**Mục đích**: Giải thích chi tiết về REST, RESTful, terminology và REST Maturity Model

---

## Mục Lục
- [RESTful Terminology](#restful-terminology---giải-thích-ful)
- ["ful" là gì?](#ful-là-gì)
- [RESTful nghĩa là gì?](#restful-nghĩa-là-gì)
- [Ví Dụ Minh Họa](#ví-dụ-minh-họa)
- [Tại sao gọi là RESTful?](#tại-sao-gọi-là-restful)
- [REST vs RESTful](#rest-vs-restful---phân-biệt)
- [REST Maturity Model](#rest-maturity-model)
- [Kết Luận](#kết-luận)

---

## RESTful Terminology - Giải Thích "ful"

### "ful" là gì?

**"ful"** là **suffix (tiền tố)** trong tiếng Anh có nghĩa là **"đầy", "tuân theo", "có tính chất của"**.

| Từ | Suffix | Cấu trúc | Nghĩa |
|----|----|---|---|
| beautiful | -ful | beautiful = beauty + ful | đầy vẻ đẹp → đẹp |
| meaningful | -ful | meaningful = meaning + ful | đầy ý nghĩa → có ý nghĩa |
| helpful | -ful | helpful = help + ful | đầy sự trợ giúp → hữu ích |
| peaceful | -ful | peaceful = peace + ful | đầy bình yên → yên bình |
| **RESTful** | **-ful** | **RESTful = REST + ful** | **tuân theo/đầy nguyên tắc REST** |

---

### RESTful nghĩa là gì?

**"RESTful"** = **"tuân thủ nguyên tắc REST"** hoặc **"có đủ các đặc tính của kiến trúc REST"**

```
REST = Kiến trúc (architecture, rules, constraints)
RESTful = Một API/hệ thống tuân theo REST nguyên tắc
Non-RESTful = API không tuân thủ REST
```

---

### Ví Dụ Minh Họa

**RESTful API** ✅ (Tuân theo REST):
```python
GET    /api/quizzes              # Lấy danh sách
POST   /api/quizzes              # Tạo mới (action suy ra từ POST method)
GET    /api/quizzes/<id>         # Lấy chi tiết (action suy ra từ GET method)
PUT    /api/quizzes/<id>         # Cập nhật toàn bộ (action suy ra từ PUT method)
DELETE /api/quizzes/<id>         # Xóa (action suy ra từ DELETE method)
```
**Đặc điểm**: Resource-based URLs, action suy ra từ HTTP method

**Non-RESTful API** ❌ (Không tuân theo REST):
```python
POST   /api/upload_quiz           # Có verb "upload" trong URL
GET    /api/getStats              # Có verb "get" trong URL
POST   /api/createSession         # Có verb "create" trong URL
GET    /api/deleteQuiz?id=1       # Dùng GET cho delete (sai method)
```
**Đặc điểm**: Action-based URLs, verb trong URL

---

### Tại sao gọi là "RESTful"?

**Vì nó có đủ các đặc tính của kiến trúc REST**:

1. ✅ **Stateless** - Mỗi request độc lập
2. ✅ **Client-Server** - Frontend ≠ Backend
3. ✅ **Uniform Interface** - API nhất quán
4. ✅ **Resource-Based URLs** - URL là resource, không phải action
5. ✅ **HTTP Methods** - GET/POST/PUT/DELETE suy ra hành động
6. ✅ **Representational** - Response là JSON/XML

```
Nếu API có cả 6 constraints → RESTful ✅
Nếu thiếu một vài → RESTful không hoàn hảo ⚠️
Nếu không có → Non-RESTful ❌
```

---

### REST vs RESTful - Phân Biệt

| Term | Ý Nghĩa | Loại |
|------|--------|------|
| **REST** | Kiến trúc (constraints, nguyên tắc) | Danh từ trừu tượng |
| **RESTful** | Tuân theo REST nguyên tắc | Tính từ (adjective) |
| **Non-RESTful** | Không tuân theo REST | Tính từ (adjective) |

**Ví dụ sử dụng**:
- "Tôi đang thiết kế một **REST API**" ✅
- "Tôi đang thiết kế một **RESTful API**" ✅ (Cả hai đều đúng)
- "Endpoint này **không RESTful**" ✅ (Vi phạm REST)
- "API này **không phải REST**" ✅ (Hoàn toàn khác)

---

## REST Maturity Model

Không phải tất cả API là "hoàn toàn RESTful". Có bậc:

### Level 0: RPC style (không phải REST)
- Dùng HTTP như transport layer
- Ví dụ: `POST /api/call?method=getQuizzes`
- **Đặc điểm**: Tất cả request dùng POST, action trong query string

### Level 1: Resource-based URLs (bắt đầu RESTful)
- Dùng tên resource trong URL
- Ví dụ: `GET /api/quizzes, POST /api/quizzes`
- **Đặc điểm**: Có resource concept nhưng chưa dùng HTTP methods

### Level 2: HTTP Methods (khá RESTful) ⭐
- Dùng GET/POST/PUT/DELETE đúng cách
- **QuizGenerator đang ở mức này**
- Ví dụ: `GET /api/quizzes, POST /api/quizzes, DELETE /api/quizzes/1`
- **Đặc điểm**: Đủ cho hầu hết ứng dụng

### Level 3: HATEOAS (hoàn toàn RESTful)
- Response chứa links để gọi hành động tiếp theo
- HATEOAS = Hypermedia As The Engine Of Application State
- Ví dụ:
```json
{
  "quiz_id": 1,
  "name": "Sample Quiz",
  "_links": {
    "self": { "href": "/api/quizzes/1", "method": "GET" },
    "update": { "href": "/api/quizzes/1", "method": "PUT" },
    "delete": { "href": "/api/quizzes/1", "method": "DELETE" },
    "create_session": { "href": "/api/quizzes/1/sessions", "method": "POST" }
  }
}
```
- **Đặc điểm**: Client có thể tìm hiểu hành động từ response

---

## Kết Luận

```
"RESTful" = từ tính từ
= "tuân theo nguyên tắc REST"
= "có đủ đặc tính kiến trúc REST"

⚠️ Naming là 20% - phần dễ nhất của REST
✅ Stateless, HTTP methods, status codes mới quan trọng 80%

📊 QuizGenerator:
   - Ở Level 2 (HTTP Methods) ✅
   - Có thể push lên Level 3 (HATEOAS) trong tương lai
   - Hiện tại đủ cho nhu cầu business
```

### Best Practices:
1. ✅ Dùng **resource-based URLs** (không verb)
2. ✅ Dùng **HTTP methods** đúng cách (GET ≠ POST)
3. ✅ Dùng **status codes** phù hợp (201 cho create, 204 cho delete)
4. ✅ API phải **stateless** (mỗi request độc lập)
5. ✅ Response là **JSON** (standard format)
6. ✅ Có thể thêm **HATEOAS** khi cần (links trong response)
