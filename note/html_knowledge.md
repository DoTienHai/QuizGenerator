---
date: 2026-04-03 14:30
summary: Tổng hợp kiến thức HTML cơ bản - Template, Form, Input types, DOM selection và Frontend structure
---

# Kiến Thức HTML - QuizGenerator

## Mục Lục
- [Template Inheritance (Jinja2)](#template-inheritance-jinja2)
- [HTML Form](#html-form)
- [Input Types](#input-types)
- [HTML Attributes](#html-attributes)
- [DOM Structure](#dom-structure)
- [Semantic HTML](#semantic-html)
- [Input Validation](#input-validation)

---

## Template Inheritance (Jinja2)

### Khái Niệm
Template inheritance là cơ chế để **tái sử dụng code** trong Flask. Thay vì viết HTML đầy đủ mỗi page, chỉ cần định nghĩa `blocks` để override.

### Cấu Trúc

**base.html (Template chính):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <header>Logo & Header</header>
    <nav>Navigation Menu</nav>
    <main>
        {% block content %}
            <!-- Nội dung sẽ được override trong child template -->
        {% endblock %}
    </main>
    <footer>Footer</footer>
</body>
</html>
```

**upload.html (Template con):**
```html
{% extends "base.html" %}

{% block title %}Tải Quiz - QuizGenerator{% endblock %}

{% block content %}
    <h2>📤 Tải Quiz từ File Excel</h2>
    <!-- Nội dung riêng của page này -->
{% endblock %}
```

### Lợi Ích
- ✅ DRY (Don't Repeat Yourself) - Viết code 1 lần
- ✅ Dễ bảo trì - Thay đổi header ở 1 chỗ, tất cả page cập nhật
- ✅ Consistency - Tất cả page cùng style

### Ví Dụ Thực Tế

| Page | Base | Block Title | Block Content |
|------|------|-------------|----------------|
| upload.html | base.html | "Tải Quiz - QuizGenerator" | Form upload |
| exam.html | base.html | "Làm Bài - QuizGenerator" | Exam form + Timer |
| results.html | base.html | "Kết Quả - QuizGenerator" | Results display |

---

## HTML Form

### Định Nghĩa
Form là container chứa các input fields và button để gửi dữ liệu tới server.

### Cấu Trúc Cơ Bản
```html
<form id="uploadForm" method="POST" action="/api/quizzes">
    <!-- Input fields -->
    <input type="text" id="quizName" name="quizName" required>
    
    <!-- File input -->
    <input type="file" id="excelFile" name="excelFile" accept=".xlsx,.xls" required>
    
    <!-- Submit button -->
    <button type="submit">Submit</button>
</form>
```

### Form Attributes

| Attribute | Ý Nghĩa | Ví Dụ |
|-----------|---------|-------|
| `id` | Định danh form (dùng JavaScript) | `id="uploadForm"` |
| `name` | Tên form (khi có nhiều form) | `name="configForm"` |
| `method` | HTTP method (GET/POST) | `method="POST"` |
| `action` | URL server nhận form | `action="/api/quizzes"` |
| `enctype` | Encoding type (nếu upload file) | `enctype="multipart/form-data"` |

### Form Submission Flow

```
1. User nhập dữ liệu
   ↓
2. User click submit button
   ↓
3. Browser validate (required fields, etc.)
   ↓
4. Request gửi tới server (GET/POST)
   ↓
5. Server xử lý & gửi response
```

**Trong QuizGenerator:**
```html
<form id="uploadForm">
    <!-- Frontend validation: required attribute -->
    <input type="file" required>
    
    <!-- JavaScript validation: check file selected -->
    if (!excelFile) {
        showMessage('❌ Vui lòng chọn file', 'error');
        return;
    }
    
    <!-- Send FormData (file + text) -->
    const formData = new FormData();
    formData.append('quiz_name', quizName);
    formData.append('file', excelFile);
</form>
```

---

## Input Types

### Các Loại Input Phổ Biến

| Type | Ý Nghĩ | UI | Ví Dụ |
|------|--------|-----|-------|
| `text` | Text box thường | Single line input | `<input type="text">` |
| `email` | Email (validate format) | Single line + @ | `<input type="email">` |
| `password` | Mật khẩu (ẩn ký tự) | Dots/asterisks | `<input type="password">` |
| `file` | File picker | Browse button | `<input type="file">` |
| `number` | Con số | Spinner +/- | `<input type="number">` |
| `radio` | Chọn 1 từ nhiều | Radio circle | `<input type="radio">` |
| `checkbox` | Chọn nhiều | Checkboxes | `<input type="checkbox">` |
| `submit` | Nút gửi form | Button | `<button type="submit">` |
| `range` | Slider | Slider bar | `<input type="range">` |

### Ở QuizGenerator

**Upload page:**
```html
<!-- Tên quiz -->
<input type="text" id="quizName" placeholder="Kiểm Tra Tiếng Anh - Chương 1">

<!-- File Excel -->
<input type="file" id="excelFile" accept=".xlsx,.xls">

<!-- Submit button -->
<button type="submit">✅ Tải Lên Quiz</button>
```

**Exam page:**
```html
<!-- Số câu hỏi -->
<input type="number" id="numQuestions" min="1" max="50" value="10">

<!-- Thời gian (phút) -->
<input type="number" id="duration" min="1" max="180" value="30">

<!-- Multiple choice-->
<input type="radio" name="question_1" value="A">
<input type="radio" name="question_1" value="B">
```

---

## HTML Attributes

### Tổng Quan Attributes

```html
<!-- id: Định danh duy nhất (JavaScript) -->
<input id="quizName">

<!-- name: Tên field (gửi tới server) -->
<input name="quiz_name">

<!-- class: CSS class (styling) -->
<button class="btn btn-success">

<!-- placeholder, value, required, accept, style, disabled... -->
```

---

### ID (Định Danh Duy Nhất)

#### Khái Niệm
`id` là định danh **UNIQUE** (chỉ 1 element có ID này trong toàn page). Dùng để JavaScript tìm kiếm element:

```javascript
document.getElementById('quizNameInput').value
```

#### ❌ Nguy Hiểm của Duplicate IDs

```html
<!-- WRONG: Duplicate IDs -->
<form id="myForm">
    <input id="output">
</form>

<form id="myForm">  <!-- ⚠️ DUPLICATE! -->
    <input id="output">  <!-- ⚠️ DUPLICATE! -->
</form>

<!-- Result: JavaScript chỉ tìm được element thứ 1 -->
document.getElementById('myForm');    // Return form #1 only
document.getElementById('output');    // Return input #1 only
// Form #2 và input #2 không thể access → BUG khó tìm!
```

#### ✅ Best Practices: Đặt Tên ID Tốt

**Quy tắc 1: Xài camelCase (không kebab-case)**
```javascript
// ✅ GOOD: camelCase (viết naturally trong JS)
document.getElementById('quizNameInput').value

// ❌ BAD: kebab-case (phải quote kỳ quặc)
document.getElementById('quiz-name-input').value
```

**Quy tắc 2: Descriptive + Type Suffix**
```html
<!-- Input IDs: ...Input -->
<input id="quizNameInput">
<input id="durationInput">

<!-- Button IDs: ...Button or ...Btn -->
<button id="uploadButton">
<button id="resetBtn">

<!-- Container IDs: ...Container or ...Wrapper -->
<div id="progressContainer">
<div id="messageWrapper">

<!-- Lợi: Ngay biết element type là gì -->
```

**Quy tắc 3: Prefix theo component (Lựa chọn 1)**
```html
<!-- Upload form group -->
<form id="uploadForm">
    <input id="uploadQuizName">
    <input id="uploadExcelFile">
    <button id="uploadSubmit">
</form>

<!-- Settings form group -->
<form id="settingsForm">
    <input id="settingsMaxQuestions">
    <input id="settingsTimeLimit">
    <button id="settingsSubmit">
</form>
<!-- Lợi: Không nhầm lẫn, dễ tìm related IDs -->
```

**Quy tắc 4: Scoped per Page (Lựa chọn 2)**
```html
<!-- upload.html -->
<input id="uploadQuizName">
<input id="uploadExcelFile">

<!-- exam.html -->
<input id="examCurrentQuestion">
<button id="examSubmitAnswer">

<!-- results.html -->
<div id="resultsScoreDisplay">

<!-- Lợi: Mỗi trang riêng lẻ, không conflict -->
```

**Ví dụ Thực: QuizGenerator Upload Form**
```html
<!-- ✅ GOOD: Rõ ràng, mô tả, không nhầm lẫn -->
<form id="uploadForm">
    <input id="uploadQuizNameInput" placeholder="Tên quiz">
    <input id="uploadExcelFileInput" type="file">
    <button id="uploadSubmitBtn">Upload</button>
</form>

<div id="uploadProgressContainer" style="display: none;">
    <p id="uploadStatusMessage">Uploading...</p>
</div>

<!-- JavaScript: Tất cả rõ ràng -->
const quizName = document.getElementById('uploadQuizNameInput').value;
const file = document.getElementById('uploadExcelFileInput').files[0];
document.getElementById('uploadProgressContainer').style.display = 'block';
```

---

### Name & Class Attributes

#### Name Attribute

```html
<!-- name: Tên field (gửi tới server via FormData) -->
<input name="quiz_name">  <!-- formData.append('quiz_name', value) -->

<!-- Có thể duplicate (radio buttons, checkboxes) -->
<input type="radio" name="question_1" value="A">
<input type="radio" name="question_1" value="B">
<input type="radio" name="question_1" value="C">

<!-- Multiple checkboxes: multiple select -->
<input type="checkbox" name="topics" value="grammar">
<input type="checkbox" name="topics" value="vocabulary">
```

#### Class Attribute

```html
<!-- class: CSS styling (có thể duplicate) -->
<button class="btn btn-primary">Save</button>
<button class="btn btn-secondary">Cancel</button>

<!-- Multiple classes: space-separated -->
<div class="container flex-center active">

<!-- Lợi: Reuse CSS styles cho nhiều elements -->
```

#### ID vs Name vs Class

| Attribute | Unique? | Dùng cho | Ví dụ |
|-----------|---------|----------|--------|
| **id** | ✅ CÓ | JavaScript targeting | `getElementById('quizNameInput')` |
| **name** | ❌ Không | Form submission + radio/checkbox grouping | Multiple `<input name="option">` |
| **class** | ❌ Không | CSS styling | Many elements `.btn` class |

---

### Other Important Attributes

```html
<!-- required: Bắt buộc nhập (HTML validation) -->
<input type="text" required>

<!-- accept: Loại file cho phép -->
<input type="file" accept=".xlsx,.xls">

<!-- placeholder: Gợi ý text -->
<input type="text" placeholder="Nhập tên quiz">

<!-- value: Giá trị mặc định -->
<input type="number" value="30">

<!-- disabled: Vô hiệu hóa input -->
<input type="text" disabled>

<!-- style: CSS inline (tránh dùng quá nhiều) -->
<div style="margin-top: 30px; max-width: 600px;">
```

---

### Validation Attributes

| Attribute | Ý Nghĩa | Ví Dụ |
|-----------|---------|-------|
| `required` | Bắt buộc nhập | `<input required>` |
| `type="email"` | Email format validation | `<input type="email">` |
| `min/max` | Giới hạn con số | `<input type="number" min="1" max="50">` |
| `minlength/maxlength` | Độ dài text | `<input minlength="3" maxlength="100">` |
| `pattern` | Regex validate | `<input pattern="[0-9]+">` |
| `accept` | File types cho phép | `<input type="file" accept=".xlsx">` |

**Ví dụ:**
```html
<form>
    <input type="text" required minlength="3" maxlength="100">
    <input type="email" required>
    <input type="number" min="1" max="50">
    <input type="file" accept=".xlsx,.xls" required>
    <button type="submit">Submit</button>
</form>
```

---

## DOM Structure

### Định Nghĩa
DOM (Document Object Model) là tree structure đại diện cho HTML:

```html
<!DOCTYPE html>
<html>
    <head>
        <title>Page Title</title>
    </head>
    <body>
        <header>
            <h1>Logo</h1>
        </header>
        <main>
            <form>
                <input id="quizName">
                <input id="excelFile" type="file">
                <button>Submit</button>
            </form>
        </main>
    </body>
</html>
```

### DOM Tree

```
document
├── html
│   ├── head
│   │   └── title
│   └── body
│       ├── header
│       │   └── h1
│       ├── main
│       │   └── form
│       │       ├── input#quizName
│       │       ├── input#excelFile
│       │       └── button
```

### Navigating DOM (JavaScript)

```javascript
// Tìm elements
document.getElementById('uploadForm')        // By ID
document.querySelector('.btn')              // By CSS selector
document.querySelectorAll('input')           // Tất cả input

// Access properties
input.value                 // Giá trị input
input.files[0]             // File đầu tiên
element.textContent        // Text bên trong

// Thay đổi
element.style.display = 'block'   // Thay CSS
element.classList.add('active')   // Thêm class
element.innerHTML = '<p>...</p>'   // Thay nội dung HTML
```

---

## Semantic HTML

### Ý Nghĩa
**Semantic HTML** là dùng các **HTML tags có sẵn** (built-in) với ý nghĩa cụ thể thay vì chỉ dùng `<div>`:

```html
<!-- ❌ Non-semantic: Chỉ là div, không rõ ý nghĩa -->
<div id="header">...</div>
<div id="nav">...</div>
<div id="content">...</div>
<div id="footer">...</div>

<!-- ✅ Semantic: Rõ ràng ý nghĩa từng phần -->
<header>...</header>
<nav>...</nav>
<main>...</main>
<footer>...</footer>
```

### ⚠️ Quan Trọng: Tags Semantic Là Cố Định

**Semantic tags KHÔNG THỂ tự đặt được!** Chúng là các tag được HTML5 standard định sẵn:

| Có Sẵn Trong HTML5 | KHÔNG THỂ Tự Tạo |
|---|---|
| ✅ `<header>` | ❌ `<myheader>` (không phải semantic) |
| ✅ `<nav>` | ❌ `<mynav>` (không phải semantic) |
| ✅ `<main>` | ❌ `<mycontent>` (không phải semantic) |
| ✅ `<footer>` | ❌ `<myfooter>` (không phải semantic) |
| ✅ `<section>` | ❌ `<mysection>` (không phải semantic) |
| ✅ `<article>` | ❌ `<myarticle>` (không phải semantic) |

**Nếu tự tạo tag** → Browser không hiểu ý nghĩa → SEO xấu, accessibility xấu

---

### Các Semantic Tags Có Sẵn

| Tag | Ý Nghĩa | Khi Nào Dùng | Ví Dụ |
|-----|---------|------------|-------|
| `<header>` | Tiêu đề/top section | Trên cùng trang hoặc section | Logo, title, navigation |
| `<nav>` | Navigation menu | Menu chính | Tabs, links menu |
| `<main>` | Nội dung chính duy nhất | Một lần duy nhất per page | Main content area |
| `<section>` | Nhóm content có cùng chủ đề | Chia nhỏ main content | Quiz section, Result section |
| `<article>` | Content độc lập, reusable | Post, bài viết, card | Blog post, quiz card |
| `<aside>` | Content phụ, sidebar | Sidebar, ads, related | Sidebar, tips |
| `<footer>` | Chân trang | Dưới cùng | Copyright, contact info |

---

### Sơ Đồ Page Layout (QuizGenerator)

```html
<header>
    <!-- Logo, Tên app -->
    <h1>QuizGenerator</h1>
</header>

<nav>
    <!-- Navigation menu -->
    <ul>
        <li><a href="/">Upload</a></li>
        <li><a href="/list-quizzes">My Quizzes</a></li>
        <li><a href="/results">Results</a></li>
    </ul>
</nav>

<main>
    <!-- Main content -->
    
    <section id="uploadSection">
        <!-- Upload quiz section -->
        <h2>Tải Quiz</h2>
        <form>...</form>
    </section>
    
    <section id="recentSection">
        <!-- Recent quizzes section -->
        <h2>Quiz Gần Đây</h2>
        <article>Quiz 1</article>
        <article>Quiz 2</article>
    </section>
    
    <aside>
        <!-- Sidebar -->
        <h3>Tips</h3>
        <p>Use .xlsx format</p>
    </aside>
</main>

<footer>
    <!-- Footer -->
    <p>&copy; 2026 QuizGenerator</p>
</footer>
```

---

### Lợi Ích của Semantic HTML

✅ **SEO tốt hơn:**
- Search engines hiểu cấu trúc page
- Bọt tìm đúng main content (trong `<main>`)
- Bọt hiểu header, nav, footer

✅ **Accessibility tốt hơn:**
- Screen readers (cho người mù) hiểu page structure
- Users có thể navigate dễ hơn

✅ **Code dễ hiểu:**
- Lập trình viên khác hiểu code nhanh
- Bảo trì dễ hơn

✅ **Thêm styling mặc định:**
- Một số browsers style semantic tags hơi khác
- `<main>` tự động block-level

---

### ❌ Anti-Pattern: Dùng Div Cho Mọi Thứ

```html
<!-- ❌ BAD: Toàn div, không rõ ý nghĩa -->
<div class="header">
    <div class="logo">QuizGenerator</div>
    <div class="nav">
        <div class="nav-item"><a href="/">Upload</a></div>
        <div class="nav-item"><a href="/quizzes">Quizzes</a></div>
    </div>
</div>

<div class="content">
    <div class="main">
        <div class="section">
            <h2>Upload Form</h2>
            <form>...</form>
        </div>
    </div>
    <div class="sidebar">
        <h3>Tips</h3>
    </div>
</div>

<div class="footer">
    <p>Copyright</p>
</div>
```

✅ **GOOD: Dùng Semantic Tags**
```html
<header>
    <h1>QuizGenerator</h1>
    <nav>
        <a href="/">Upload</a>
        <a href="/quizzes">Quizzes</a>
    </nav>
</header>

<main>
    <section>
        <h2>Upload Form</h2>
        <form>...</form>
    </section>
    
    <aside>
        <h3>Tips</h3>
    </aside>
</main>

<footer>
    <p>Copyright</p>
</footer>
```

---

### Khi Nào Dùng `<section>` vs `<article>`

#### `<section>` - Nhóm Content Cùng Chủ Đề

```html
<section id="uploadSection">
    <h2>Tải Quiz Mới</h2>
    <!-- Form, instructions, etc. -->
</section>

<section id="quizzesSection">
    <h2>Quiz Của Tôi</h2>
    <!-- List of quizzes -->
</section>
```

**Khi dùng:**
- Group content cùng topic
- Mỗi section có heading
- Content liên quan trong 1 section

#### `<article>` - Content Độc Lập, Có Thể Reuse

```html
<article class="quizCard">
    <h3>Math Quiz - Chapter 1</h3>
    <p>20 questions, 30 minutes</p>
    <button>Start</button>
</article>

<article class="quizCard">
    <h3>English Quiz - Basics</h3>
    <p>15 questions, 20 minutes</p>
    <button>Start</button>
</article>
```

**Khi dùng:**
- Content có thể tồn tại độc lập
- Có thể reuse hoặc syndicate (RSS, etc.)
- Card, post, comment

---

### Quizz: Chọn Tag Đúng

```html
<!-- 1. Chứa navigation links -->
<nav> ✅ hoặc <div class="nav">? ❌
<nav>
    <a href="/">Home</a>
    <a href="/quizzes">Quizzes</a>
</nav>

<!-- 2. Chứa quiz card (có thể reuse) -->
<article> ✅ hoặc <div class="quiz">? ❌
<article class="quizCard">
    <h3>Math Quiz</h3>
    <button>Start</button>
</article>

<!-- 3. Chứa related quizzes (group) -->
<section> ✅ hoặc <div class="section">? ❌
<section>
    <h2>Related Quizzes</h2>
    <article>...</article>
    <article>...</article>
</section>

<!-- 4. Chứa sidebar tips -->
<aside> ✅ hoặc <div class="sidebar">? ❌
<aside>
    <h3>Tips & Tricks</h3>
    <p>Use Excel format</p>
</aside>

<!-- 5. Chứa copyright -->
<footer> ✅ hoặc <div class="footer">? ❌
<footer>
    <p>&copy; 2026</p>
</footer>
```

---

## Input Validation

### HTML Validation (Phía Client)

```html
<form>
    <!-- Required -->
    <input type="text" required>
    
    <!-- Email format -->
    <input type="email">
    
    <!-- Number với min/max -->
    <input type="number" min="1" max="50">
    
    <!-- File type -->
    <input type="file" accept=".xlsx,.xls">
</form>
```

**Khi user click submit:**
- Nếu invalid → Hiện error message
- Nếu valid → Gửi form

### JavaScript Validation (Phía Client)

```javascript
const file = document.getElementById('excelFile').files[0];

if (!file) {
    showMessage('❌ Vui lòng chọn file', 'error');
    return;
}

if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
    showMessage('❌ File phải là Excel (.xlsx hoặc .xls)', 'error');
    return;
}
```

### Server Validation (Phía Backend - Quan Trọng!)

```python
# Python Flask
@app.route('/api/quizzes', methods=['POST'])
def upload_quiz():
    # Validate file exists
    if 'file' not in request.files:
        return error_response('ERR_MISSING_FILE', 'File required', 400)
    
    # Validate file type
    file = request.files['file']
    if not file.filename.endswith(('.xlsx', '.xls')):
        return error_response('ERR_INVALID_FILE_TYPE', 'Only .xlsx/.xls allowed', 400)
    
    # Process file...
```

### Validation Tầng

```
┌──────────────────────────────────────┐
│ HTML Form Validation (required, etc) │ ← Ngăn submit if empty
├──────────────────────────────────────┤
│ JavaScript Client Validation         │ ← Kiểm tra file size, format
├──────────────────────────────────────┤
│ Server Validation (Backend)          │ ← CRITICAL - Never trust client!
├──────────────────────────────────────┤
│ Database Validation (Unique, etc)    │ ← Final check
└──────────────────────────────────────┘
```

---

## Tóm Tắt

**HTML trong QuizGenerator:**
- ✅ Template inheritance (Jinja2) để tái sử dụng layout
- ✅ Form + Input để collect user data
- ✅ Various input types (text, file, number, radio)
- ✅ Validation: HTML + JavaScript + Server
- ✅ Semantic HTML (header, nav, main, footer)
- ✅ IDs & names để JavaScript access

**Best Practices:**
1. Dùng semantic HTML (header, nav, main, footer)
2. Validate ở 3 tầng (HTML, JS, Server)
3. Dùng meaningful IDs (không dùng id1, id2)
4. Template inheritance để tái sử dụng code
5. Form structure rõ ràng (label, input, button)
