# UUID (Universally Unique Identifier) - Giải Thích Chi Tiết

**Ngày tạo**: 2026-03-16  
**Mục đích**: Giải thích UUID là gì, cách tạo ra, lưu trữ trong SQLite, và ứng dụng trong QuizGenerator

---

## Mục Lục
- [UUID là gì?](#uuid-la-gi)
- [Cấu trúc UUID](#cau-truc-uuid)
- [Cách UUID được tạo ra](#cach-uuid-duoc-tao-ra)
- [UUID vs Integer ID](#uuid-vs-integer-id)
- [UUID trong SQLite3](#uuid-trong-sqlite3)
- [Ứng dụng trong QuizGenerator](#ung-dung-trong-quizgenerator)
- [Ví dụ Thực Tế](#vi-du-thuc-te)

---

## UUID là gì?

**UUID** (Universally Unique Identifier) là một chuỗi **36 ký tự** được sử dụng để đại diện cho một định danh duy nhất, toàn cầu.

**Đặc điểm chính:**
- ✅ **Duy nhất toàn cầu**: Gần như không thể có 2 UUID giống nhau (xác suất cực kỳ thấp)
- ✅ **Không thể đoán**: Giá trị hoàn toàn ngẫu nhiên, người ngoài không thể đoán được
- ✅ **Phân tán**: Có thể tạo offline mà không cần kết nối database
- ✅ **Tiêu chuẩn**: Tuân theo RFC 4122
- ✅ **Bảo mật**: Phù hợp cho dữ liệu nhạy cảm hoặc URL công khai

**Ví dụ:**
```
550e8400-e29b-41d4-a716-446655440000
```

---

## Cấu trúc UUID

UUID có 5 phần, được phân tách bằng dấu `-`:

```
550e8400-e29b-41d4-a716-446655440000
├─ 8 ký tự ┤  4 ký tự  4 ký tự  4 ký tự   12 ký tự
│          │
└─ Time Low─ Time Mid ─ Time Hi & Version ─ Clock Seq ─ Node
```

**Chi tiết các phần:**

| Phần | Dài | Ý Nghĩa | Ví Dụ |
|------|-----|---------|-------|
| **Time Low** | 8 hex | Phần đầu của timestamp | `550e8400` |
| **Time Mid** | 4 hex | Phần giữa timestamp | `e29b` |
| **Time Hi & Version** | 4 hex | Phần cuối + version | `41d4` |
| **Clock Seq** | 4 hex | Biến đổi & Sequence | `a716` |
| **Node** | 12 hex | MAC address hoặc ngẫu nhiên | `446655440000` |

**Tổng cộng**: 32 ký tự hex + 4 dấu gạch ngang = **36 ký tự**

---

## Cách UUID được tạo ra

Có **5 phiên bản UUID** (Version 1-5), nhưng phổ biến nhất là:

### **UUID Version 1 (Time-based)** - Dựa trên Thời gian + MAC Address

**Cách hoạt động:**
1. Lấy timestamp hiện tại (tính từ năm 1582)
2. Lấy MAC address của máy tính (hoặc giá trị ngẫu nhiên nếu không có)
3. Kết hợp + thêm version bits
4. Tính toán checksum

**Ưu điểm:**
- ✅ Có thể sắp xếp theo thời gian (tự động sort)
- ✅ Kích thước nhỏ

**Nhược điểm:**
- ❌ Tiết lộ MAC address (bảo mật)
- ❌ Dễ đoán nếu biết thời gian tạo

---

### **UUID Version 4 (Random)** - Sinh Ngẫu Nhiên ⭐

**Cách hoạt động:**
1. Sinh **122 bit** ngẫu nhiên
2. Đặt 4 bit version = 0100 (binary = 4)
3. Đặt 2 bit variant
4. Vậy là xong!

**Ưu điểm:**
- ✅ Hoàn toàn ngẫu nhiên, không thể đoán
- ✅ Có thể tạo offline
- ✅ Tốc độ nhanh
- ✅ Phù hợp bảo mật cao

**Nhược điểm:**
- ❌ Không thể sắp xếp theo thời gian

**Công thức xác suất đụng độ:**
```
2 UUID từ ~6 triệu giá trị → xác suất đụng độ = 50%
(tương tự Birthday Paradox)
```

---

### **UUID Version 5 (Name-based SHA-1)** - Dựa trên Tên

**Cách hoạt động:**
1. Lấy một "namespace" (UUID chuẩn) + tên input
2. Tạo SHA-1 hash của (namespace + tên)
3. Format thành UUID

**Ví dụ:**
```python
import uuid

namespace = uuid.NAMESPACE_DNS
name = "example.com"

uuid5_result = uuid.uuid5(namespace, name)
# Output: 886313e1-3b8a-5372-9b90-0c9aee199e5d
```

**Ưu điểm:**
- ✅ Deterministic (cùng input → cùng UUID)
- ✅ Bảo mật hơn version 1

**Nhược điểm:**
- ❌ Cần input cụ thể

---

## UUID vs Integer ID

### **So Sánh Chi Tiết:**

| Tiêu Chí | INT ID | UUID |
|----------|--------|------|
| **Format** | `1, 2, 3...` | `550e8400-e29b-41d4-a716-446655440000` |
| **Kích thước** | 4-8 bytes | 36 bytes (TEXT) hoặc 16 bytes (BINARY) |
| **Dễ nhớ** | ✅ Dễ | ❌ Khó |
| **Dễ đoán** | ❌ Dễ đoán (1, 2, 3) | ✅ Không thể đoán |
| **Brute Force** | ❌ Dễ attack (thử 1, 2, 3...) | ✅ Gần không thể attack |
| **Auto-increment** | ✅ Có | ❌ Không (phải sinh) |
| **Phân tán** | ❌ Không (cần database) | ✅ Có thể sinh offline |
| **Sắp xếp** | ✅ Tự động (sequential) | ⚠️ Chỉ V1 có thể |
| **Bảo mật** | ❌ Thấp | ✅ Cao |
| **Blockchain** | ❌ | ✅ Phù hợp |

---

## UUID trong SQLite3

SQLite3 **không có native UUID type**, nhưng có 2 cách lưu:

### **Cách 1: TEXT (Khuyến Nghị)**

```sql
CREATE TABLE exam_session (
  session_id TEXT PRIMARY KEY,
  -- "550e8400-e29b-41d4-a716-446655440000"
  ...
);
```

**Ưu điểm:**
- ✅ Dễ đọc, dễ debug (có thể xem trực tiếp)
- ✅ Tương thích với tất cả tools
- ✅ Dễ import/export

**Nhược điểm:**
- ❌ Tốn 36 bytes (không nén)

---

### **Cách 2: BLOB (Tối ưu)**

```sql
CREATE TABLE exam_session (
  session_id BLOB PRIMARY KEY,
  -- Lưu binary UUID (16 bytes)
  ...
);
```

**Ưu điểm:**
- ✅ Nhỏ gọn: 16 bytes vs 36 bytes
- ✅ Query nhanh hơn

**Nhược điểm:**
- ❌ Khó đọc (binary không hiểu được)
- ❌ Khó debug

---

## Ứng dụng trong QuizGenerator

### **Tại sao QuizGenerator dùng UUID cho session_id?**

1. **Bảo mật**
   - Exam session là dữ liệu **cá nhân** của user
   - Nếu dùng INT: người khác có thể đoán URL `/exam/1`, `/exam/2`, `/exam/3`
   - UUID: không thể đoán → `/exam/550e8400-e29b-41d4-a716-446655440000`

2. **URL công khai**
   - Nếu user share link exam với người khác
   - UUID URL: an toàn
   - INT URL: bất an toàn

3. **Stateless Design**
   - Có thể tạo session ID offline
   - Không cần database để sinh ID

### **Implementation trong Flask-SQLAlchemy**

```python
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class ExamSession(db.Model):
    __tablename__ = 'exam_session'
    
    session_id = db.Column(
        db.String(36),  # UUID format
        primary_key=True,
        default=lambda: str(uuid.uuid4())  # Auto generate UUID
    )
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    num_questions = db.Column(db.Integer, nullable=False)
    exam_duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(10), nullable=False, default='active')
```

### **Tạo Session trong Route**

```python
from models import ExamSession, db
import uuid

@session_bp.route('/sessions', methods=['POST'])
def create_session():
    quiz_id = request.json.get('quiz_id')
    num_questions = request.json.get('num_questions')
    exam_duration = request.json.get('exam_duration')
    
    # Sinh UUID tự động
    session_id = str(uuid.uuid4())
    
    session = ExamSession(
        session_id=session_id,
        quiz_id=quiz_id,
        num_questions=num_questions,
        exam_duration=exam_duration
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'session_id': session_id,
        'status': 'active'
    }), 201
```

---

## Ví dụ Thực Tế

### **Tạo UUID trong Python**

```python
import uuid

# Version 4 (Random) - Khuyến nghị
session_id = str(uuid.uuid4())
print(session_id)  # 550e8400-e29b-41d4-a716-446655440000

# Version 1 (Time-based)
time_uuid = str(uuid.uuid1())
print(time_uuid)   # 550e8400-e29b-11ed-99a0-0242ac130003

# Version 5 (Name-based)
namespace = uuid.NAMESPACE_DNS
name_uuid = str(uuid.uuid5(namespace, 'example.com'))
print(name_uuid)   # 886313e1-3b8a-5372-9b90-0c9aee199e5d
```

### **URLs trong QuizGenerator**

**Với INT ID (Không an toàn):**
```
GET /api/sessions/1
GET /api/sessions/2
GET /api/sessions/3
→ Dễ đoán, dễ brute force
```

**Với UUID (An toàn):**
```
GET /api/sessions/550e8400-e29b-41d4-a716-446655440000
GET /api/sessions/886313e1-3b8a-5372-9b90-0c9aee199e5d
GET /api/sessions/12345678-1234-5678-1234-567812345678
→ Không thể đoán, không thể brute force
```

---

## Kết Luận

| Điểm | Kết Luận |
|------|----------|
| **UUID là gì?** | Chuỗi 36 ký tự duy nhất toàn cầu, không thể đoán |
| **Cách tạo** | V4 (random) là đơn giản + bảo mật nhất |
| **SQLite** | Lưu dưới dạng TEXT, phù hợp với QuizGenerator |
| **QuizGenerator** | Dùng UUID cho bảo mật session data |
| **Ưu điểm** | Bảo mật cao, dễ tạo offline, không đoán được |
| **Nhược điểm** | URL dài, khó nhớ |

**→ QuizGenerator: Quyết định sử dụng UUID là đúng! ✅**
