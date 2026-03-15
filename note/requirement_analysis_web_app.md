---
date: 2026-03-14 
summary: Dàn dựng các bước phân tích requirement cho một web app từ thông tin input đến output
---

# Requirement Analysis cho Web App

## Mục Lục
- [Bước 1: Xác định thông tin cơ bản](#buoc-1-xac-dinh-thong-tin-co-ban)
- [Bước 2: Xác định Input](#buoc-2-xac-dinh-input)
- [Bước 3: Xác định Output](#buoc-3-xac-dinh-output)
- [Bước 4: Xác định User Stories & Features](#buoc-4-xac-dinh-user-stories--features)
- [Bước 5: Xác định Technical Requirements](#buoc-5-xac-dinh-technical-requirements)

## Bước 1: Xác định thông tin cơ bản

Cần trả lời các câu hỏi:

1. **Purpose**: Web app này dùng để làm gì?
2. **Target Users**: Ai là người dùng chính?
3. **Problem Statement**: Giải quyết vấn đề gì?
4. **Business Goals**: Mục tiêu kinh doanh là gì?
5. **Success Metrics**: Đo lường thành công bằng cách nào?

**Ví dụ QuizGenerator:**
- Purpose: Tạo & thực hiện bài quiz từ file Excel
- Target Users: Teachers, educators
- Problem: Tạo quiz thủ công mất time, cần automation
- Goals: Giúp giáo viên tạo quiz nhanh, dễ, có nhiều tính năng
- Metrics: Số quiz tạo, user retention, satisfaction score

---

## Bước 2: Xác định Input

**Input là gì?** Dữ liệu vào từ người dùng hoặc hệ thống

### Các loại Input:

1. **User Input (from UI)**
   - Form submission
   - File upload (Excel, CSV, JSON)
   - Configuration settings
   - Manual entries (text, numbers)

2. **System Input**
   - Environment variables
   - Configuration files
   - Database data
   - API responses

3. **Data Constraints**
   - File types & sizes
   - Validation rules
   - Format requirements
   - Business logic constraints

**Ví dụ QuizGenerator:**
```
INPUT:
- Excel file (.xlsx, .xls) chứa questions
- User configuration: num_questions, exam_duration
- User answers: selected options, submitted time
```

### Input Metadata cần ghi:
- Định dạng (format)
- Kích thước tối đa (nếu có)
- Bắt buộc hay không
- Validation rules

---

## Bước 3: Xác định Output

**Output là gì?** Kết quả/dữ liệu trả về cho người dùng

### Các loại Output:

1. **UI Output**
   - Displayed content (tables, forms, results)
   - Download files (PDF, Excel, CSV)
   - Error messages
   - Success confirmations

2. **Data Output**
   - API responses (JSON/XML)
   - Database writes
   - Log files

3. **Business Output**
   - Reports
   - Analytics
   - Status changes

**Ví dụ QuizGenerator:**
```
OUTPUT:
- HTML page: Quiz form với questions & options
- JSON response: Quiz metadata, session info
- File download: Results file (PDF/Excel)
- Database: Save quiz session, answers, scores
```

### Output Metadata cần ghi:
- Format (HTML, JSON, PDF, etc.)
- Content structure
- Data fields & types
- Success/error cases

---

## Bước 4: Xác định User Stories & Features

**User Story format:** "As a [user type], I want [action], so that [benefit]"

**Ví dụ:**
```
1. As a teacher, I want to upload Excel file with questions, so that I can quickly create quiz
2. As a student, I want to answer quiz questions, so that I can test my knowledge
3. As a teacher, I want to see student results, so that I can evaluate performance
```

### Features từ User Stories:
- Upload & parse Excel file
- Configure quiz settings
- Display quiz to students
- Submit answers
- Auto-calculate scores
- Export results

---

## Bước 5: Xác định Technical Requirements

### Architecture:
- Backend: (Flask, Django, Node.js, etc.)
- Frontend: (React, Vue, plain HTML, etc.)
- Database: (PostgreSQL, MySQL, SQLite, etc.)
- Storage: (Local, Cloud, etc.)

### Functional Requirements:
- Features chi tiết
- Business logic rules
- Validation rules
- Error handling

### Non-Functional Requirements:
- Performance (response time, throughput)
- Scalability (số users, data volume)
- Security (authentication, authorization, data protection)
- Reliability (uptime, error recovery)
- Accessibility (UI/UX, browsers support)

### Constraints:
- Time limit
- Budget
- Technology stack
- Integration needs

---

## Checklist Requirement Analysis

- [ ] Purpose & goals định nghĩa rõ
- [ ] All input types identified & documented
- [ ] All output types identified & documented
- [ ] User stories viết rõ ràng
- [ ] Features list hoàn toàn
- [ ] Tech stack quyết định
- [ ] Validation rules defined
- [ ] Error handling cases covered
- [ ] Performance requirements stated
- [ ] Security requirements identified
