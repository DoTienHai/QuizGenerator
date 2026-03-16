---
description: Tạo file note khi người dùng chat "note ..."
applyTo: 'khi người dùng bắt đầu message với "note" hoặc "note ..."'
---

# Hướng dẫn tạo file Note

## Khi nào tạo file Note?
- Khi người dùng chat bắt đầu với "note" hoặc "note ..." (ví dụ: "note cấu trúc project", "note lỗi trong validation")

## Quy tắc đặt tên file Note
- **Format**: `short_title_in_english.md`
- **Ví dụ**: `project_structure.md`, `user_quiz_config.md`, `uuid_explanation.md`
- Sử dụng **tiếng Anh**, chữ thường, dấu gạch dưới thay khoảng trắng
- Tên file ngắn gọn, mô tả nội dung chính
- **Không** sử dụng tiếng Việt trong tên file

## Cấu trúc Header của file Note
```markdown
---
date: YYYY-MM-DD HH:mm
summary: Tóm tắt ngắn gọn nội dung note (1-2 dòng)
---

# Tiêu đề Note
```

**Ví dụ:**
```markdown
---
date: 2026-03-03 10:45
summary: Tổng hợp cấu trúc project QuizGenerator và các components chính
---

# Cấu trúc Project QuizGenerator
```

## Nội dung Note
- **Ngôn ngữ**: Viết bằng tiếng Việt
- **Ngoại lệ**: Giữ nguyên các thuật ngữ kỹ thuật đặc thù (Flask, Excel, quiz, validation, etc.)
- **Định dạng**: Sử dụng markdown với heading, bullet points, code blocks
- **Chi tiết**: Tóm tắt các thông tin liên quan trong cuộc nói chuyện
- **Mục lục (TOC)**: Nếu note có từ 3 mục (heading level 2) trở lên, PHẢI có mục lục ở đầu file
  - Format mục lục: `- [Tiêu đề](#anchor-link)`
  - Anchor link sử dụng format: `#tieude-voi-dau-gach-duoi`
  - Mục lục nằm ngay sau header metadata

## Ví dụ
```markdown
---
date: 2026-03-03 10:45
summary: Tổng hợp cấu trúc folder và flow của ứng dụng QuizGenerator
---

## Mục Lục
- [Các components chính](#cac-components-chinh)
- [Flow chính](#flow-chinh)
- [Cấu trúc folder](#cau-truc-folder)

# Cấu trúc QuizGenerator

## Các components chính
- Flask application (app.py)
- Excel parser module
- Quiz generator engine
- Session-based data storage

## Flow chính
User Upload → Parsing Excel → Validation → Question Storage → Quiz Generation → Display/Download

## Cấu trúc folder
```
QuizGenerator/
├── app.py
├── templates/
└── utils/
```
```

**File name ví dụ**: `project_structure.md` hoặc `quizgenerator_architecture.md`

## Vị trí lưu file
Tất cả file note sẽ được lưu trong folder: `QuizGenerator/note/`