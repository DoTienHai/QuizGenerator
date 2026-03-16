# Blueprint & Code Organization - Learning Notes

**Ngày tạo**: 2026-03-16  
**Mục đích**: Ghi chép về Blueprint, Coupling, Testing, và kiến trúc chia file

---

## Mục Lục
- [Blueprint là gì?](#1-blueprint-la-gi)
- [3 Cách Tách File & Routes](#2-3-cach-tach-file--routes)
- [Lightweight Coupling vs Tight Coupling](#3-lightweight-coupling-vs-tight-coupling)
- [Testing: Cách 2 vs Cách 3](#4-testing-cach-2-vs-cach-3)
- [Loose Coupling Không Phải Không Cần Phụ Thuộc](#5-loose-coupling-khong-phai-khong-can-phu-thuoc)
- [Blueprint Workflow](#6-blueprint-workflow)
- [QuizGenerator: Tại Sao Dùng Blueprint?](#7-quizgenerator-tai-sao-dung-blueprint)
- [Cấu Trúc Recommend](#8-cau-truc-recommend-cho-quizgenerator)
- [app.py Mới](#9-apppy-moi-sau-refactor)
- [Chia Endpoints vào Blueprints](#10-chia-endpoints-vao-blueprints)
- [Summary](#11-summary-loi-ich-cua-blueprint)
- [Tiếp Theo](#12-tiep-theo)

---

## 1. Blueprint là gì?

**Blueprint** = Một **bộ routes có thể tái sử dụng** trong Flask

- Giúp **nhóm routes liên quan** vào cùng một module
- Có thể **register vào Flask app** sau
- Là **"plugin" của Flask**

### Ví Dụ:
```python
# routes/quiz_routes.py
quiz_bp = Blueprint('quiz', __name__, url_prefix='/api')

@quiz_bp.route('/quizzes', methods=['GET'])
def list_quizzes():
    return {}

# app.py
app.register_blueprint(quiz_bp)
```

---

## 2. 3 Cách Tách File & Routes

### Cách 1: KHÔNG tách
- **app.py**: Tất cả routes + logic
- **services.py**: Business logic riêng
- **Ưu điểm**: Đơn giản
- **Nhược điểm**: app.py quá to, khó bảo trì

### Cách 2: Tách routes (Không Blueprint)
- **app.py**: Flask app, gọi `init_routes(app)`
- **routes/quiz_routes.py**: Hàm `init_routes()` thêm routes vào app
- **Ưu điểm**: Routes tách rời
- **Nhược điểm**: 
  - Routes BUỘC phụ thuộc app (tight coupling)
  - Không thể test blueprint mà không có app
  - Routes không tồn tại cho đến khi gọi `init_routes()`

### Cách 3: Blueprint (Recommended) ⭐
- **app.py**: Flask app, `register_blueprint()`
- **routes/quiz_routes.py**: Blueprint object + routes
- **Ưu điểm**: 
  - Routes độc lập (loose coupling)
  - Có thể test blueprint properties mà không cần app
  - Có thể register vào nhiều app
  - Flask standard practice
- **Nhược điểm**: Hơi phức tạp một chút

---

## 3. Lightweight Coupling vs Tight Coupling

### Tight Coupling (Cách 2):
```
routes.py → BUỘC phụ thuộc vào app.py
         (Imperative: phải gọi init_routes(app))
```

**Vấn đề**:
- Routes chỉ tồn tại sau khi gọi `init_routes()`
- Không thể test routes "properties" mà không có app
- Test phải gọi init → bắt buộc

### Loose Coupling (Cách 3):
```
blueprint.py → Độc lập
           → TỰ CHỌN phụ thuộc vào app.py
             (Declarative: register_blueprint() khi cần)
```

**Ưu điểm**:
- Blueprint tồn tại độc lập
- Có thể test blueprint properties mà KHÔNG cần app
- Có thể test routes với app (giống Cách 2)
- Linh hoạt hơn

---

## 4. Testing: Cách 2 vs Cách 3

### Cách 2: Test Routes (Phải có app)
```python
def test_list_quizzes():
    app = Flask(__name__)
    init_routes(app)  # ← BUỘC phải gọi
    
    client = app.test_client()
    assert client.get('/api/quizzes').status_code == 200
```

**Không có cách test nào khác!**

### Cách 3: Test Blueprint + Routes

**Test 1: Blueprint properties (KHÔNG cần app)**
```python
def test_blueprint_structure():
    from routes.quiz_routes import quiz_bp
    
    assert quiz_bp.name == 'quiz'
    assert quiz_bp.url_prefix == '/api'
    assert len(quiz_bp.deferred_functions) == 3  # 3 routes
    # ✅ Không cần app!
```

**Test 2: Routes logic (cần app)**
```python
def test_routes():
    app = Flask(__name__)
    app.register_blueprint(quiz_bp)
    
    client = app.test_client()
    assert client.get('/api/quizzes').status_code == 200
```

### Kết Luận Testing:
```
Cách 2:
  - Chỉ 1 cách: cần app + init
  - Không linh hoạt

Cách 3:
  - 2 cách: 
    1. Test blueprint (không app) ✅
    2. Test routes (cần app)
  - Linh hoạt hơn
```

---

## 5. Loose Coupling Không Phải "Không Cần Phụ Thuộc"

### Định Nghĩa Đúng:
```
Loose Coupling = Phụ thuộc linh hoạt, không bắt buộc

Cách 2 (Tight):
  routes.py → BUỘC phụ thuộc app.py
             (phải gọi init_routes(app))

Cách 3 (Loose):
  blueprint.py → Độc lập
              → Phụ thuộc app.py là TỰ CHỌN
                (khi gọi register_blueprint)
```

### Ưu Điểm Loose Coupling:
1. Blueprint tồn tại độc lập
2. Có thể test blueprint mà không cần app
3. Có thể register vào nhiều app
4. Không bị imperative coupling

---

## 6. Blueprint Workflow

```
1️⃣ Tạo Blueprint object
   quiz_bp = Blueprint('quiz', __name__, url_prefix='/api')

2️⃣ Thêm routes vào Blueprint
   @quiz_bp.route('/quizzes')
   def list_quizzes():
       return {}

3️⃣ App import Blueprint
   from routes.quiz_routes import quiz_bp

4️⃣ Register Blueprint vào App
   app.register_blueprint(quiz_bp)

5️⃣ Routes tự động merge vào Flask app
   GET  /api/quizzes
   POST /api/quizzes/upload
   ...
```

---

## 7. QuizGenerator: Tại Sao Dùng Blueprint?

**Điều kiện**:
- ✅ 11 endpoints (quá nhiều cho app.py)
- ✅ Endpoints nhóm theo chức năng (Quiz, Session, Result)
- ✅ Business logic phức tạp (Excel parsing, scoring)
- ✅ Design đã define 5-layer architecture

**Có nên dùng Blueprint?**
- ✅ **CÓ NÊN DÙNG** (Cách 3 - Blueprint)

---

## 8. Cấu Trúc Recommend Cho QuizGenerator

```
QuizGenerator/
├── app.py                          ← Main entry + Blueprint register
├── config.py                       ← Database config, env vars
├── requirements.txt
├── Procfile
│
├── modules/
│   ├── __init__.py
│   │
│   ├── models.py                   ← Layer 5: Database Models
│   │   ├── Quiz
│   │   ├── Question
│   │   ├── ExamSession
│   │   ├── UserAnswer
│   │   └── ExamResult
│   │
│   ├── services/                   ← Layer 3: Business Logic
│   │   ├── __init__.py
│   │   ├── quiz_service.py         ├─ QuizService
│   │   │   ├─ parse_excel()
│   │   │   ├─ store_quiz()
│   │   │   └─ get_quizzes()
│   │   │
│   │   ├── exam_service.py         ├─ ExamService
│   │   │   ├─ create_session()
│   │   │   ├─ get_questions()
│   │   │   ├─ shuffle_options()
│   │   │   └─ get_random_questions()
│   │   │
│   │   └── scoring_engine.py       ├─ ScoringEngine
│   │       ├─ calculate_score()
│   │       ├─ determine_status()
│   │       └─ save_result()
│   │
│   ├── repositories/ (Optional)    ← Layer 4: Data Access
│   │   ├── __init__.py
│   │   ├── quiz_repo.py
│   │   ├── session_repo.py
│   │   └── result_repo.py
│   │
│   └── routes/                     ← Layer 2: Application (Controllers)
│       ├── __init__.py
│       │
│       ├── quiz_routes.py          ← Blueprint: /api/quizzes
│       │   @quiz_bp.route('/quizzes', methods=['GET'])
│       │   @quiz_bp.route('/quizzes/upload', methods=['POST'])
│       │   @quiz_bp.route('/quizzes/<id>', methods=['GET'])
│       │   @quiz_bp.route('/quizzes/<id>/results', methods=['GET'])
│       │
│       ├── session_routes.py       ← Blueprint: /api/sessions
│       │   @session_bp.route('/sessions', methods=['POST'])
│       │   @session_bp.route('/sessions/<id>', methods=['GET'])
│       │   @session_bp.route('/sessions/<id>/status', methods=['GET'])
│       │   @session_bp.route('/sessions/<id>/answers', methods=['POST'])
│       │   @session_bp.route('/sessions/<id>/submit', methods=['POST'])
│       │   @session_bp.route('/sessions/<id>/auto-submit', methods=['POST'])
│       │
│       ├── result_routes.py        ← Blueprint: /api/results
│       │   @result_bp.route('/results/<id>', methods=['GET'])
│       │
│       └── frontend_routes.py      ← Blueprint: Frontend pages
│           @frontend_bp.route('/')
│           @frontend_bp.route('/upload')
│           @frontend_bp.route('/exam')
│           @frontend_bp.route('/results')
│
├── templates/                      ← Layer 1: Presentation
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   ├── exam.html
│   └── results.html
│
└── static/                         ← Frontend assets
    ├── css/
    └── js/
```

---

## 9. app.py Mới (Sau Refactor)

```python
# app.py - Chỉ main entry + Blueprint register
from flask import Flask
from config import Config
from modules.routes.quiz_routes import quiz_bp
from modules.routes.session_routes import session_bp
from modules.routes.result_routes import result_bp
from modules.routes.frontend_routes import frontend_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(frontend_bp)  # Frontend routes ("/", "/upload", etc)
app.register_blueprint(quiz_bp)      # API routes ("/api/quizzes")
app.register_blueprint(session_bp)   # API routes ("/api/sessions")
app.register_blueprint(result_bp)    # API routes ("/api/results")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

---

## 10. Chia Endpoints vào Blueprints

### Blueprint 1: Quiz Management
```python
# modules/routes/quiz_routes.py

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api')

@quiz_bp.route('/quizzes', methods=['GET'])
def list_quizzes():
    # GET /api/quizzes → List all quizzes
    pass

@quiz_bp.route('/quizzes/upload', methods=['POST'])
def upload_quiz():
    # POST /api/quizzes/upload → Upload Excel
    pass

@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    # GET /api/quizzes/1 → Get quiz details
    pass

@quiz_bp.route('/quizzes/<int:quiz_id>/results', methods=['GET'])
def get_quiz_results(quiz_id):
    # GET /api/quizzes/1/results → Get all results for quiz
    pass
```

### Blueprint 2: Exam Session
```python
# modules/routes/session_routes.py

session_bp = Blueprint('session', __name__, url_prefix='/api')

@session_bp.route('/sessions', methods=['POST'])
def create_session():
    # POST /api/sessions → Create exam session
    pass

@session_bp.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    # GET /api/sessions/1 → Get session + questions
    pass

@session_bp.route('/sessions/<int:session_id>/status', methods=['GET'])
def get_session_status(session_id):
    # GET /api/sessions/1/status → Check status
    pass

@session_bp.route('/sessions/<int:session_id>/answers', methods=['POST'])
def submit_answers(session_id):
    # POST /api/sessions/1/answers → Submit answers
    pass

@session_bp.route('/sessions/<int:session_id>/submit', methods=['POST'])
def submit_exam(session_id):
    # POST /api/sessions/1/submit → Final submit
    pass

@session_bp.route('/sessions/<int:session_id>/auto-submit', methods=['POST'])
def auto_submit(session_id):
    # POST /api/sessions/1/auto-submit → Auto-submit (timeout)
    pass
```

### Blueprint 3: Results
```python
# modules/routes/result_routes.py

result_bp = Blueprint('result', __name__, url_prefix='/api')

@result_bp.route('/results/<int:session_id>', methods=['GET'])
def get_results(session_id):
    # GET /api/results/1 → Get exam results
    pass
```

### Blueprint 4: Frontend Pages
```python
# modules/routes/frontend_routes.py

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    return render_template('index.html')

@frontend_bp.route('/upload')
def upload():
    return render_template('upload.html')

@frontend_bp.route('/exam')
def exam():
    return render_template('exam.html')

@frontend_bp.route('/results')
def results():
    return render_template('results.html')
```

---

## 11. Summary: Lợi Ích Của Blueprint

| Aspect | Benefit |
|--------|---------|
| **Organization** | Routes nhóm theo chức năng |
| **Maintainability** | Dễ đọc, dễ tìm code |
| **Scalability** | Dễ thêm features mới |
| **Testability** | Có thể test blueprint độc lập |
| **Reusability** | Có thể register vào nhiều app |
| **Flask Standard** | Theo best practice |

---

## 12. Tiếp Theo

**Phase 3 Development** (theo thứ tự):

1. ✅ **Frontend complete** (HTTP templates, JavaScript)
2. ⏭️ **Refactor: Tách thành Blueprint structure**
3. ⏭️ **Implement Database Models** (SQLAlchemy)
4. ⏭️ **Implement Services** (Business logic)
5. ⏭️ **Implement Routes** (Actual endpoint logic)
6. ⏭️ **Testing**
7. ⏭️ **Deploy lên Render.com**

---

**Status**: Hiểu rõ Blueprint + loose coupling + testing pattern ✓

