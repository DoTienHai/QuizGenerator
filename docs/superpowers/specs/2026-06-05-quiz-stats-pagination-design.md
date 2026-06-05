# Design: Server-side Pagination cho Quiz Stats

**Date**: 2026-06-05  
**Scope**: Trang `/quiz-stats` — bảng "Kết Quả Các Bài Exam"  
**Approach**: Server-side pagination với SQL LIMIT/OFFSET + aggregation stats

---

## Problem

Trang `/quiz-stats` hiện tải **toàn bộ** lịch sử thi của 1 quiz về frontend rồi:
1. Tính stats (trung bình, count) bằng JS
2. Render toàn bộ vào bảng HTML

Khi số lượng bài thi tăng, backend load tất cả vào RAM Python và serialize toàn bộ JSON → lãng phí.

---

## Solution

### 2 SQL queries thay vì 1 query lớn

**Query 1 — Aggregation** (tính 1 lần khi load trang):
```sql
SELECT 
    COUNT(*)                                         AS total_attempts,
    AVG(score)                                       AS avg_score,
    SUM(CASE WHEN status='PASS' THEN 1 ELSE 0 END)  AS pass_count
FROM exam_result
JOIN exam_session USING (session_id)
WHERE exam_result.quiz_id = :quiz_id
```

**Query 2 — Paginated list** (gọi lại mỗi khi đổi trang):
```sql
SELECT ... FROM exam_result
WHERE quiz_id = :quiz_id
ORDER BY submitted_at DESC
LIMIT 10 OFFSET (page - 1) * 10
```

---

## Backend Changes — `modules/routes/result.py`

### `GET /api/results`

Thêm query params:
- `page` (int, default=1)
- `per_page` (int, default=10, max=100)

**Backward compatibility**: Nếu `quiz_id` không được truyền (tức là `/exams` page đang gọi), trả toàn bộ như cũ — không phân trang.

Response khi có `quiz_id` + `page`:
```json
{
  "success": true,
  "data": [ ...10 bản ghi... ],
  "stats": {
    "total_attempts": 42,
    "pass_count": 30,
    "fail_count": 12,
    "avg_score": 71.5
  },
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 42,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

Response khi không có `quiz_id` (backward compat):
```json
{
  "success": true,
  "data": [ ...toàn bộ... ],
  "message": "Loaded completed exams"
}
```

---

## Frontend Changes

### `static/js/quiz-stats.js`

1. **Xoá** phần tính stats bằng JS (lines 36-57)
2. **Thêm** `currentPage = 1` state variable
3. Hàm `loadQuizStats()` gọi `GET /api/results?quiz_id=X&page=1&per_page=10`
4. Đọc `stats` từ response → update 4 thẻ thống kê
5. Đọc `data` từ response → render bảng
6. Đọc `pagination` → render pagination controls
7. Thêm hàm `goToPage(page)` để chuyển trang

### `templates/quiz-stats.html`

Thêm pagination controls dưới bảng:
```html
<div id="paginationControls">
  <button onclick="goToPage(currentPage - 1)">← Trang trước</button>
  <span>Trang 1 / 5 (42 bài)</span>
  <button onclick="goToPage(currentPage + 1)">Trang sau →</button>
</div>
```

---

## Data Flow

```
User mở /quiz-stats
    ↓
JS gọi GET /api/results?quiz_id=X&page=1&per_page=10
    ↓
Backend:
  ├── Query 1: SELECT COUNT, AVG, SUM → stats
  └── Query 2: SELECT ... LIMIT 10 OFFSET 0 → 10 bản ghi
    ↓
Response: { data, stats, pagination }
    ↓
JS:
  ├── stats → update 4 thẻ thống kê
  ├── data → render bảng
  └── pagination → render controls
    ↓
User click "Trang sau →"
    ↓
JS gọi GET /api/results?quiz_id=X&page=2&per_page=10
    ↓
Backend: LIMIT 10 OFFSET 10
```

---

## Files Affected

| File | Thay đổi |
|------|----------|
| `modules/routes/result.py` | Sửa `list_results()` — thêm pagination + aggregation query |
| `static/js/quiz-stats.js` | Xoá tính stats FE, thêm pagination state + controls |
| `templates/quiz-stats.html` | Thêm `#paginationControls` div |

**Không thay đổi**: `/exams` page, `results.html`, tất cả API khác.

---

## Constraints

- `per_page` tối đa 100 (tránh abuse)
- `page` tối thiểu 1
- Nếu page vượt quá total_pages → trả trang cuối
- Stats cards (`totalAttempts`, `passCount`, `failCount`, `avgScore`) luôn hiển thị tổng toàn bộ, không phải chỉ trang hiện tại
