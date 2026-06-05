# Quiz Stats Server-side Pagination Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm server-side pagination (10 bản ghi/trang) vào bảng kết quả trang `/quiz-stats`, với stats được tính bằng SQL aggregation trên backend.

**Architecture:** Sửa `GET /api/results` để hỗ trợ `?page=&per_page=` khi có `quiz_id`. Backend chạy 2 query: (1) aggregation để tính stats, (2) LIMIT/OFFSET để lấy 10 bản ghi. Frontend xoá phần tính stats bằng JS, thêm pagination controls.

**Tech Stack:** Flask, SQLAlchemy 2.x, Vanilla JS, Jinja2, pytest

---

## Files Changed

| File | Thay đổi |
|------|----------|
| `modules/routes/result.py` | Sửa `list_results()` — thêm helper `_build_result_dict`, pagination + aggregation query |
| `static/js/quiz-stats.js` | Xoá tính stats FE, thêm `currentPage`, `loadPage()`, `renderPagination()`, `goToPage()` |
| `templates/quiz-stats.html` | Thêm `#paginationControls` div sau bảng |
| `tests/conftest.py` | Tạo mới — Flask test client fixture với in-memory SQLite |
| `tests/test_result_routes.py` | Tạo mới — test cho pagination API |

---

## Task 1: Test fixtures (conftest.py)

**Files:**
- Create: `tests/conftest.py`

- [ ] **Step 1: Tạo conftest.py với Flask test client fixture**

```python
# tests/conftest.py
import pytest
from app import create_app
from modules.models import db as _db
from config import TestingConfig


@pytest.fixture(scope='function')
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def db(app):
    return _db
```

- [ ] **Step 2: Chạy pytest để đảm bảo fixture không lỗi**

```bash
pytest tests/conftest.py -v
```

Expected: No errors (no tests collected is fine)

- [ ] **Step 3: Commit**

```bash
git add tests/conftest.py
git commit -m "test: add Flask test client fixture in conftest.py"
```

---

## Task 2: Viết failing tests cho paginated API

**Files:**
- Create: `tests/test_result_routes.py`

- [ ] **Step 1: Tạo helper tạo dữ liệu test**

```python
# tests/test_result_routes.py
import uuid
from datetime import datetime, timedelta
import pytest
from modules.models import db, Quiz, ExamSession, ExamResult


def _seed_results(db, quiz_name='Test Quiz', count=15, pass_count=10):
    """Tạo quiz + N exam results trong DB test."""
    quiz = Quiz(name=quiz_name, total_questions=20)
    db.session.add(quiz)
    db.session.flush()

    for i in range(count):
        session_id = str(uuid.uuid4())
        session = ExamSession(
            session_id=session_id,
            quiz_id=quiz.quiz_id,
            num_questions=20,
            exam_duration=30,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=1),
            status='submitted'
        )
        db.session.add(session)
        db.session.flush()

        status = 'PASS' if i < pass_count else 'FAIL'
        score = 80.0 if status == 'PASS' else 40.0
        result = ExamResult(
            session_id=session_id,
            quiz_id=quiz.quiz_id,
            score=score,
            correct_count=16 if status == 'PASS' else 8,
            incorrect_count=4 if status == 'PASS' else 12,
            skipped_count=0,
            status=status,
            submitted_at=datetime.utcnow() - timedelta(minutes=i),
            time_spent_seconds=1200
        )
        db.session.add(result)

    db.session.commit()
    return quiz.quiz_id
```

- [ ] **Step 2: Viết test pagination trả đúng 10 bản ghi trang 1**

```python
def test_list_results_paginated_returns_10_items(client, db):
    quiz_id = _seed_results(db, count=15)

    response = client.get(f'/api/results?quiz_id={quiz_id}&page=1&per_page=10')
    data = response.get_json()

    assert response.status_code == 200
    assert data['success'] is True
    assert len(data['data']) == 10
```

- [ ] **Step 3: Viết test pagination metadata chính xác**

```python
def test_list_results_paginated_returns_pagination_metadata(client, db):
    quiz_id = _seed_results(db, count=15)

    response = client.get(f'/api/results?quiz_id={quiz_id}&page=1&per_page=10')
    data = response.get_json()

    pagination = data['pagination']
    assert pagination['page'] == 1
    assert pagination['per_page'] == 10
    assert pagination['total'] == 15
    assert pagination['total_pages'] == 2
    assert pagination['has_next'] is True
    assert pagination['has_prev'] is False
```

- [ ] **Step 4: Viết test stats được tính đúng**

```python
def test_list_results_paginated_returns_correct_stats(client, db):
    quiz_id = _seed_results(db, count=15, pass_count=10)

    response = client.get(f'/api/results?quiz_id={quiz_id}&page=1&per_page=10')
    data = response.get_json()

    stats = data['stats']
    assert stats['total_attempts'] == 15
    assert stats['pass_count'] == 10
    assert stats['fail_count'] == 5
    assert 'avg_score' in stats
```

- [ ] **Step 5: Viết test trang 2 trả đúng 5 bản ghi còn lại**

```python
def test_list_results_paginated_page2_returns_remaining(client, db):
    quiz_id = _seed_results(db, count=15)

    response = client.get(f'/api/results?quiz_id={quiz_id}&page=2&per_page=10')
    data = response.get_json()

    assert response.status_code == 200
    assert len(data['data']) == 5
    assert data['pagination']['page'] == 2
    assert data['pagination']['has_next'] is False
    assert data['pagination']['has_prev'] is True
```

- [ ] **Step 6: Viết test backward compat — không có page param trả toàn bộ**

```python
def test_list_results_without_page_returns_all(client, db):
    quiz_id = _seed_results(db, count=15)

    response = client.get(f'/api/results?quiz_id={quiz_id}')
    data = response.get_json()

    assert response.status_code == 200
    assert len(data['data']) == 15
    assert 'pagination' not in data
    assert 'stats' not in data
```

- [ ] **Step 7: Chạy tests và xác nhận chúng FAIL**

```bash
pytest tests/test_result_routes.py -v
```

Expected: 5 tests FAIL (API chưa có pagination)

- [ ] **Step 8: Commit failing tests**

```bash
git add tests/test_result_routes.py
git commit -m "test: add failing tests for paginated /api/results endpoint"
```

---

## Task 3: Implement backend pagination

**Files:**
- Modify: `modules/routes/result.py`

- [ ] **Step 1: Thêm import `func` và `case` từ sqlalchemy**

Mở [modules/routes/result.py](modules/routes/result.py) và sửa dòng import đầu file:

```python
from flask import Blueprint, jsonify, request
from sqlalchemy import func, case
from ..services import ScoringEngine
from ..models import ExamResult, Quiz, ExamSession, db
```

- [ ] **Step 2: Thêm helper `_build_result_dict` trước route**

Thêm hàm này ngay trước `@result_bp.route('/results', ...)`:

```python
def _build_result_dict(exam_result, quiz, session):
    return {
        'session_id': exam_result.session_id,
        'quiz_id': exam_result.quiz_id,
        'quiz_name': quiz.name,
        'score': exam_result.score,
        'correct_count': exam_result.correct_count,
        'incorrect_count': exam_result.incorrect_count,
        'skipped_count': exam_result.skipped_count,
        'status': exam_result.status,
        'submitted_at': exam_result.submitted_at.isoformat(),
        'time_spent_seconds': exam_result.time_spent_seconds,
        'num_questions': session.num_questions,
        'exam_duration': session.exam_duration
    }
```

- [ ] **Step 3: Thay toàn bộ hàm `list_results()` bằng version mới**

```python
@result_bp.route('/results', methods=['GET'])
def list_results():
    """
    List completed exams with scores.
    - Paginated mode: ?quiz_id=X&page=N&per_page=10 → returns data + stats + pagination
    - Legacy mode: no page param → returns all results (backward compat for /exams page)
    """
    try:
        quiz_id = request.args.get('quiz_id', type=int)
        page = request.args.get('page', type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)

        base_query = db.session.query(ExamResult, Quiz, ExamSession).join(
            Quiz, ExamResult.quiz_id == Quiz.quiz_id
        ).join(
            ExamSession, ExamResult.session_id == ExamSession.session_id
        )
        if quiz_id:
            base_query = base_query.filter(ExamResult.quiz_id == quiz_id)
        base_query = base_query.order_by(ExamResult.submitted_at.desc())

        # Paginated mode: quiz_id + page both provided
        if page is not None and quiz_id is not None:
            agg = db.session.query(
                func.count(ExamResult.result_id).label('total'),
                func.avg(ExamResult.score).label('avg_score'),
                func.sum(case((ExamResult.status == 'PASS', 1), else_=0)).label('pass_count')
            ).filter(ExamResult.quiz_id == quiz_id).one()

            total = agg.total or 0
            avg_score = round(float(agg.avg_score or 0), 1)
            pass_count = int(agg.pass_count or 0)
            total_pages = max(1, (total + per_page - 1) // per_page)
            page = max(1, min(page, total_pages))
            offset = (page - 1) * per_page

            results = base_query.limit(per_page).offset(offset).all()
            exam_list = [_build_result_dict(er, q, s) for er, q, s in results]

            return jsonify({
                'success': True,
                'data': exam_list,
                'stats': {
                    'total_attempts': total,
                    'pass_count': pass_count,
                    'fail_count': total - pass_count,
                    'avg_score': avg_score
                },
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                }
            }), 200

        # Legacy mode: return all results (used by /exams page)
        results = base_query.all()
        exam_list = [_build_result_dict(er, q, s) for er, q, s in results]
        return jsonify({
            'success': True,
            'data': exam_list,
            'message': 'Loaded completed exams'
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error loading exam results: {str(e)}'}), 500
```

- [ ] **Step 4: Chạy tests và xác nhận pass**

```bash
pytest tests/test_result_routes.py -v
```

Expected: 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add modules/routes/result.py
git commit -m "feat: add server-side pagination and aggregation stats to GET /api/results"
```

---

## Task 4: Update quiz-stats.js

**Files:**
- Modify: `static/js/quiz-stats.js`

- [ ] **Step 1: Thay toàn bộ nội dung `quiz-stats.js` bằng version mới**

```javascript
/**
 * Quiz Stats - Display quiz statistics and exam results with server-side pagination
 */

let currentPage = 1;
const PER_PAGE = 10;

document.addEventListener('DOMContentLoaded', () => {
    loadQuizStats();
});

/**
 * Load quiz header and first page of results
 */
async function loadQuizStats() {
    const quizId = parseInt(sessionStorage.getItem('selectedQuizId'));
    const quizName = sessionStorage.getItem('selectedQuizName');

    if (!quizId) {
        showMessage('Không tìm thấy thông tin quiz', 'error');
        return;
    }

    document.getElementById('quizName').textContent = `📚 ${quizName}`;
    await loadPage(quizId, 1);
}

/**
 * Fetch one page of results from server and render everything
 */
async function loadPage(quizId, page) {
    try {
        const response = await fetch(`/api/results?quiz_id=${quizId}&page=${page}&per_page=${PER_PAGE}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Lỗi tải kết quả');
        }

        const { stats, pagination } = data;

        document.getElementById('totalAttempts').textContent = stats.total_attempts;
        document.getElementById('passCount').textContent = stats.pass_count;
        document.getElementById('failCount').textContent = stats.fail_count;
        document.getElementById('avgScore').textContent = stats.avg_score.toFixed(1) + '%';

        renderTable(data.data);
        renderPagination(quizId, pagination);
        currentPage = pagination.page;

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}

/**
 * Render the results table rows
 */
function renderTable(results) {
    const tableBody = document.getElementById('resultsTableBody');
    const noResults = document.getElementById('noResults');

    if (results.length === 0) {
        tableBody.style.display = 'none';
        noResults.style.display = 'block';
        return;
    }

    tableBody.style.display = 'table-row-group';
    noResults.style.display = 'none';
    tableBody.innerHTML = '';

    results.forEach(result => {
        const statusColor = result.status === 'PASS' ? '#48bb78' : '#f56565';
        const statusText = result.status === 'PASS' ? '✅ PASS' : '❌ FAIL';
        const total = result.correct_count + result.incorrect_count + result.skipped_count;

        const row = document.createElement('tr');
        row.style.borderBottom = '1px solid #e2e8f0';
        row.innerHTML = `
            <td style="padding: 12px; text-align: left;">
                ${new Date(result.submitted_at).toLocaleString('vi-VN')}
            </td>
            <td style="padding: 12px; text-align: center; font-weight: bold; color: #667eea;">
                ${result.score.toFixed(1)}%
            </td>
            <td style="padding: 12px; text-align: center;">
                ${result.correct_count}/${total}
            </td>
            <td style="padding: 12px; text-align: center;">
                ${result.incorrect_count}
            </td>
            <td style="padding: 12px; text-align: center;">
                ${result.skipped_count}
            </td>
            <td style="padding: 12px; text-align: center;">
                <span style="color: ${statusColor}; font-weight: bold;">
                    ${statusText}
                </span>
            </td>
            <td style="padding: 12px; text-align: center;">
                <button class="btn btn-primary" style="padding: 6px 12px; font-size: 12px;"
                        onclick="showExamDetails('${result.session_id}')">
                    👁️ Xem Chi Tiết
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

/**
 * Render prev/next pagination controls
 */
function renderPagination(quizId, pagination) {
    const controls = document.getElementById('paginationControls');

    if (pagination.total_pages <= 1) {
        controls.style.display = 'none';
        return;
    }

    controls.style.display = 'flex';
    document.getElementById('pageInfo').textContent =
        `Trang ${pagination.page} / ${pagination.total_pages} (${pagination.total} bài)`;
    document.getElementById('btnPrev').disabled = !pagination.has_prev;
    document.getElementById('btnNext').disabled = !pagination.has_next;
}

/**
 * Navigate to a specific page
 */
function goToPage(page) {
    const quizId = parseInt(sessionStorage.getItem('selectedQuizId'));
    loadPage(quizId, page);
}

/**
 * Show detailed exam results on separate page
 */
function showExamDetails(sessionId) {
    sessionStorage.setItem('examSessionId', sessionId);
    window.location.href = '/results';
}
```

- [ ] **Step 2: Commit**

```bash
git add static/js/quiz-stats.js
git commit -m "feat: update quiz-stats.js to use server-side pagination and stats"
```

---

## Task 5: Thêm pagination controls vào HTML

**Files:**
- Modify: `templates/quiz-stats.html`

- [ ] **Step 1: Thêm div `paginationControls` sau thẻ `.card` chứa bảng**

Mở [templates/quiz-stats.html](templates/quiz-stats.html). Sau thẻ đóng `</div>` của card bảng kết quả (dòng 58), thêm:

```html
    <!-- Pagination Controls -->
    <div id="paginationControls" style="display: none; justify-content: center; align-items: center; gap: 15px; margin-bottom: 30px;">
        <button id="btnPrev" class="btn btn-secondary" style="padding: 8px 18px;" onclick="goToPage(currentPage - 1)">← Trang trước</button>
        <span id="pageInfo" style="color: #667eea; font-weight: bold; font-size: 14px;"></span>
        <button id="btnNext" class="btn btn-primary" style="padding: 8px 18px;" onclick="goToPage(currentPage + 1)">Trang sau →</button>
    </div>
```

- [ ] **Step 2: Commit**

```bash
git add templates/quiz-stats.html
git commit -m "feat: add pagination controls to quiz-stats page"
```

---

## Task 6: Kiểm tra manual trên browser

- [ ] **Step 1: Chạy app**

```bash
python app.py
```

- [ ] **Step 2: Mở trang quiz-stats**

Vào trang danh sách quiz → click vào một quiz có hơn 10 bài thi → xác nhận:
- 4 thẻ thống kê hiển thị đúng tổng (không chỉ trang 1)
- Bảng hiển thị đúng 10 bài (hoặc ít hơn nếu tổng < 10)
- Pagination controls hiện ra nếu có > 10 bài
- Nút "Trang trước" bị disabled ở trang 1
- Click "Trang sau" → bảng cập nhật, stats không đổi

- [ ] **Step 3: Kiểm tra /exams page không bị ảnh hưởng**

Vào `/exams` → xác nhận danh sách bài làm vẫn hiển thị bình thường

- [ ] **Step 4: Chạy toàn bộ test suite**

```bash
pytest -v
```

Expected: Tất cả tests PASS
