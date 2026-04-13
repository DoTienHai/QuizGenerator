# SW4: Frontend Implementation & User Flow - QuizGenerator

**Last Updated**: 2026-04-13  
**Version**: 1.3  
**Status**: Implementation (Quiz Stats & Results Refactored)  
**Author**: AI Assistant

---

## Table of Contents

- [Frontend Overview](#frontend-overview)
- [Page Structure](#page-structure)
- [User Flow](#user-flow)
- [Component Breakdown](#component-breakdown)
- [API Integration](#api-integration)
- [Session Management](#session-management)
- [Error Handling in Frontend](#error-handling-in-frontend)

---

## Frontend Overview

### Technology Stack

- **HTML5** - Structure
- **CSS3** - Styling (inline in templates)
- **JavaScript (Vanilla)** - Interactivity (no frameworks)
- **Session Storage** - Client-side session data
- **Fetch API** - HTTP requests to backend

### Architecture

**Single Page Navigation** with multiple views:
- Pages load into `<main>` container
- Navigation bar stays persistent
- State managed via JavaScript

---

## Page Structure

### Base Template: `templates/base.html`

Shared layout for all pages:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <!-- Meta & Title -->
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 QuizGenerator</h1>
        </header>
        
        <nav>
            <!-- Navigation Menu -->
            <a href="/">📤 Tải Quiz</a>
            <a href="/list-quizzes">📋 Danh Sách Quiz</a>
        </nav>
        
        <main>
            {% block content %}{% endblock %}
        </main>
        
        <footer><!-- Footer content --></footer>
    </div>
</body>
</html>
```

### Navigation Structure

| Page | URL | File | Purpose |
|------|-----|------|----------|
| **Upload** | `/` | `upload.html` | Upload Excel files with questions |
| **Quiz List** | `/list-quizzes` | `list-quizzes.html` | Browse available quizzes (Table view) |
| **Exam** | `/exam-do` | `exam.html` | Prepare & take exam |
| **Quiz Stats** | `/quiz-stats` | `quiz-stats.html` | View quiz statistics & all results |
| **Results** | `/results` | `results.html` | View detailed answer review |

### Default Landing

- **Homepage URL** (`/`) → Main entry point for application
- Users start with quiz upload page
- Single route endpoint for simplicity

---

## User Flow

### Complete User Journey

```
┌─────────────────────────────────────────────────────────────┐
│                     USER JOURNEY                             │
└─────────────────────────────────────────────────────────────┘

1. OPEN WEBSITE
   └─ GET / → renders upload.html (main entry point)
   
2. UPLOAD QUIZ
   Page: / (upload.html)
   ├─ User selects Excel file
   ├─ Click "Tải Quiz" button
   ├─ POST /api/quizzes {file}
   └─ Success: Show "Quiz uploaded!" message
      → Quizzes appear in list
   
3. VIEW QUIZZES
   Page: /list-quizzes (list-quizzes.html - Table format)
   ├─ GET /api/quizzes → Load quiz list
   ├─ Display quizzes in table with columns:
   │  ├─ # (Index)
   │  ├─ Tên Quiz
   │  ├─ Số Câu Hỏi
   │  ├─ Ngày Tải
   │  └─ Hành Động (2 buttons)
   ├─ Two action buttons per quiz:
   │  ├─ "🎮 Làm Bài" → Start exam
   │  └─ "📈 Thống Kê" → View statistics
   
4. VIEW QUIZ STATISTICS (NEW)
   Page: /quiz-stats (quiz-stats.html)
   ├─ GET /api/results → Load all results
   ├─ Filter by selected quiz_id
   ├─ Calculate & display stats:
   │  ├─ Total exams
   │  ├─ Pass rate
   │  ├─ Average score
   │  └─ All exam results in table
   ├─ User can click "👁️ Xem Chi Tiết" → View details
   
5. CONFIGURE & START EXAM
   Page: /exam-do (exam.html)
   ├─ Show config form:
   │  ├─ Number of questions (1-max)
   │  └─ Duration in minutes (default: 30)
   ├─ User fills form & clicks "🎮 Bắt Đầu Làm Bài"
   ├─ POST /api/exams
   │  Body: {quiz_id, num_questions, exam_duration}
   │  Response: {session_id, ...}
   │  Store: sessionId = response.data.session_id
   ├─ GET /api/exams/{sessionId}/questions
   │  Load questions into exam page
   └─ Display exam with timer & questions
   
6. TAKE EXAM
   ├─ User answers questions (A/B/C/D or skip)
   ├─ Each answer recorded: recordAnswer(questionId, answer)
   │  (Stored in local answers object, not real-time submission)
   ├─ Timer countdown (warning at 5 min)
   ├─ User options:
   │  ├─ "✅ Nộp Bài" → Submit all answers
   │  ├─ "🔄 Làm Lại" → Reset exam
   │  └─ Time expires → Auto-submit
   
7. SUBMIT EXAM
   ├─ POST /api/exams/{id}/submit
   │  Body: {answers: {questionId: userAnswer, ...}}
   ├─ Backend:
   │  ├─ Update user_answer.user_answer & is_correct
   │  ├─ Calculate score
   │  ├─ Determine PASS/FAIL (≥80%)
   │  └─ Save ExamResult
   ├─ Response: {score, status, correct_count, ...}
   ├─ Session storage: examSessionId = sessionId
   └─ Redirect to /results (after 1.5 sec)
   
7. VIEW RESULTS (DETAILED)
   Page: /results (results.html)
   ├─ GET /api/exams/{examSessionId}/answers-detail
   ├─ Display results card:
   │  ├─ Score percentage & status (PASS/FAIL - threshold: ≥80%)
   │  └─ Date submitted
   ├─ Display detailed Q&A section:
   │  ├─ Each question with:
   │  │  ├─ Question text
   │  │  ├─ All 4 options (A, B, C, D)
   │  │  ├─ User's answer
   │  │  ├─ Correct answer (highlighted green)
   │  │  └─ Status icon (✅/❌/❓)
   │  └─ Incorrect answers shown in warning box
   ├─ Navigation buttons at bottom:
   │  ├─ "🔄 Làm Lại" → Retake same exam with same params
   │  └─ "← Quay Lại" → Go back to quiz list
   └─ retakeExam() stores params in sessionStorage for replay
```

---

## Component Breakdown

### 1. Upload Page (`upload.html`)

**Functions**:
- File selection
- File validation (frontend)
- Upload to backend
- Progress feedback

**Key JavaScript**:

```javascript
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const file = document.getElementById('excelFile').files[0];
    
    if (!file) {
        showMessage('❌ Vui lòng chọn file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/quizzes', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!data.success) {
            showMessage(`❌ ${data.message}`, 'error');
            return;
        }
        
        showMessage('✅ Quiz tải lên thành công!', 'success');
        // Clear form
        document.getElementById('uploadForm').reset();
        
    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
});
```

### 2. Quiz List Page (`list-quizzes.html`)

**Functions**:
- Display all quizzes
- Select quiz for exam
- Navigate to exam

**Key JavaScript**:

```javascript
async function loadQuizzes() {
    try {
        const response = await fetch('/api/quizzes');
        const data = await response.json();
        
        if (!data.success) {
            showMessage(`❌ ${data.message}`, 'error');
            return;
        }
        
        const quizzes = data.data || [];
        const container = document.getElementById('quizList');
        container.innerHTML = quizzes.map(quiz => `
            <div class="card">
                <h3>${quiz.name}</h3>
                <p>📚 ${quiz.total_questions} câu hỏi</p>
                <button onclick="selectQuiz(${quiz.quiz_id}, '${quiz.name}', ${quiz.total_questions})">
                    ✅ Chọn
                </button>
            </div>
        `).join('');
        
    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}

function selectQuiz(quizId, quizName, totalQuestions) {
    sessionStorage.setItem('selectedQuizId', quizId);
    sessionStorage.setItem('selectedQuizName', quizName);
    sessionStorage.setItem('selectedQuizTotal', totalQuestions);
    window.location.href = '/exam';
}
```

### 3. Exam Page (`exam.html`)

**Three States**:

#### State 1: Quiz Selection & Configuration

```javascript
// Show config form if quiz already selected
function loadConfigSection() {
    const quizName = sessionStorage.getItem('selectedQuizName');
    document.getElementById('quizNameDisplay').textContent = quizName;
    document.getElementById('configSection').style.display = 'block';
}
```

#### State 2: Exam In Progress

**Timer Management**:

```javascript
function startTimer() {
    remainingTime = duration * 60;
    timerInterval = setInterval(() => {
        remainingTime--;
        updateTimerDisplay();
        
        if (remainingTime === 300) {
            showMessage('⚠️ Còn 5 phút!', 'info');
        }
        
        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            auto_submitExam();
        }
    }, 1000);
}
```

**Question Display**:

```javascript
async function loadQuestions(sessionId) {
    try {
        // NEW ENDPOINT (fixed):
        const response = await fetch(`/api/sessions/${sessionId}/questions`);
        const data = await response.json();
        
        if (!data.success) {
            showMessage(`❌ ${data.message}`, 'error');
            return;
        }
        
        // Questions in response.data array
        const questions = data.data || [];
        displayQuestions(questions);
        
    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}
```

**Answer Recording**:

```javascript
function recordAnswer(questionId, answer) {
    answers[questionId] = answer;
    // Automatically saved to answers object
}
```

#### State 3: Exam Submitted

```javascript
async function submitExam() {
    clearInterval(timerInterval);
    
    try {
        const response = await fetch(`/api/sessions/${sessionId}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answers: answers })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            showMessage(`❌ ${data.message}`, 'error');
            startTimer();
            return;
        }
        
        showMessage('✅ Nộp bài thành công!', 'success');
        sessionStorage.setItem('examSessionId', sessionId);
        
        // Redirect to results after 1.5 seconds
        setTimeout(() => {
            window.location.href = '/results';
        }, 1500);
        
    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}
```

### 4. Results Page (`results.html`)

**Display Results**:

```javascript
async function loadResults() {
    try {
        const sessionId = sessionStorage.getItem('examSessionId');
        
        if (!sessionId) {
            showMessage('❌ No exam session found', 'error');
            return;
        }
        
        const response = await fetch(`/api/results/${sessionId}`);
        const data = await response.json();
        
        if (!data.success) {
            showMessage(`❌ ${data.message}`, 'error');
            return;
        }
        
        displayResults(data.data);
        
    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}
```

---

## API Integration

### Request Pattern

**Standard fetch request**:

```javascript
async function apiCall(endpoint, method = 'GET', body = null) {
    try {
        const config = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (body) {
            config.body = JSON.stringify(body);
        }
        
        const response = await fetch(endpoint, config);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.message || 'Error occurred');
        }
        
        return data.data;
        
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
```

### Error Response Handling

```javascript
if (!response.ok) {
    throw new Error(data.message || 'HTTP Error: ' + response.status);
}

if (!data.success) {
    switch(data.error_code) {
        case 'ERR_SESSION_EXPIRED':
            // Redirect to new exam
            break;
        case 'ERR_QUIZ_NOT_FOUND':
            // Show quiz not found
            break;
        default:
            showMessage(`❌ ${data.message}`, 'error');
    }
}
```

---

## Session Management

### SessionStorage Keys

| Key | Value | Usage |
|-----|-------|-------|
| `selectedQuizId` | quiz_id | Passed to exam config |
| `selectedQuizName` | quiz name | Display in UI |
| `selectedQuizTotal` | total questions | Validate num_questions |
| `examSessionId` | session_id | Retrieve results after exam |

### Session Lifecycle

```javascript
// 1. SELECT QUIZ
sessionStorage.setItem('selectedQuizId', quizId);

// 2. CREATE SESSION
const response = await fetch('/api/sessions', {
    body: { quiz_id: sessionStorage.getItem('selectedQuizId'), ... }
});
sessionId = response.data.session_id;

// 3. SUBMIT EXAM
sessionStorage.setItem('examSessionId', sessionId);

// 4. VIEW RESULTS
const sessionId = sessionStorage.getItem('examSessionId');

// 5. RESET (Làm Lại button)
sessionId = null;
sessionStorage.clear();
```

---

## Error Handling in Frontend

### Error Codes Handled

```javascript
const errorHandlers = {
    'ERR_MISSING_FILE': () => console.log('File required'),
    'ERR_INVALID_FILE_TYPE': () => console.log('Invalid file type'),
    'ERR_QUIZ_NOT_FOUND': () => redirectToQuizList(),
    'ERR_SESSION_EXPIRED': () => restartExam(),
    'ERR_INVALID_ANSWER': () => showAnswerError(),
    'ERR_SESSION_NOT_FOUND': () => redirectToExam()
};
```

### User Feedback

- **Error**: Red message with ❌
- **Warning**: Orange message with ⚠️
- **Success**: Green message with ✅
- **Info**: Blue message with ℹ️

```javascript
function showMessage(message, type) {
    const container = document.getElementById('messageContainer');
    container.className = `message message-${type}`;
    container.textContent = message;
    container.style.display = 'block';
    
    setTimeout(() => {
        container.style.display = 'none';
    }, 3000); // Auto-hide after 3 seconds
}
```

---

## Browser Support

- **Chrome**: ✅ Full support
- **Firefox**: ✅ Full support
- **Safari**: ✅ Full support
- **Edge**: ✅ Full support
- **IE11**: ⚠️ Partial (SessionStorage supported, but no Promise.finally)

### Compatibility Notes

- Uses `Fetch API` (no IE11 support without polyfill)
- Uses `SessionStorage` (all modern browsers)
- Uses modern JavaScript (ES6+) - Transpile for older browsers

---

## Performance Considerations

### Optimization

- Lazy load questions only when exam starts
- Cache quiz list in sessionStorage
- Minimize API calls
- Debounce timer updates

### Future Improvements

- [ ] Service Worker for offline support
- [ ] Progressive Web App (PWA)
- [ ] Mobile-first responsive design
- [ ] Dark mode support
- [ ] Accessibility improvements (WCAG 2.1)

---

## Related Files

- Navigation: [`templates/base.html`](../templates/base.html)
- Upload: [`templates/upload.html`](../templates/upload.html)
- Quiz List: [`templates/list-quizzes.html`](../templates/list-quizzes.html)
- Exam: [`templates/exam.html`](../templates/exam.html)
- Results: [`templates/results.html`](../templates/results.html)
- Routes: [`modules/routes/frontend.py`](../modules/routes/frontend.py)
