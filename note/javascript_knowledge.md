---
date: 2026-04-03 14:30
summary: Tổng hợp kiến thức JavaScript - Event Listeners, DOM Manipulation, Async/Await, Fetch API, FormData và Error Handling
---

# Kiến Thức JavaScript - QuizGenerator

## Mục Lục
- [JavaScript Basics](#javascript-basics)
- [Event Listeners](#event-listeners)
- [DOM Manipulation](#dom-manipulation)
- [FormData & File Upload](#formdata--file-upload)
- [Async & Await](#async--await)
- [Fetch API](#fetch-api)
- [Error Handling](#error-handling)
- [Common Patterns](#common-patterns)

---

## JavaScript Basics

### Ý Nghĩa
JavaScript (JS) là ngôn ngữ lập trình chạy **trên browser** để thêm tương tác:

```html
<button id="myBtn">Click Me</button>

<script>
    // JavaScript code
    const button = document.getElementById('myBtn');
    button.addEventListener('click', () => {
        alert('Button clicked!');
    });
</script>
```

### Variable Declaration

```javascript
/* var (old - avoid) */
var name = 'Quiz';
var name = 'Quiz 2';  // Can redeclare

/* let (block scope - preferred) */
let quizName = 'Math Quiz';
{
    let localVar = 5;  // Only inside {}
}
console.log(localVar);  // Error: not defined

/* const (constant - preferred) */
const MAX_QUESTIONS = 50;
MAX_QUESTIONS = 60;  // Error: cannot reassign
```

### Data Types

```javascript
/* Strings */
const name = 'Quiz Generator';
const msg = `Hello ${name}`;  // Template literal

/* Numbers */
const count = 10;
const score = 75.5;
const result = count + score;  // 85.5

/* Boolean */
const isValid = true;
const isEmpty = false;

/* Objects */
const quiz = {
    id: 1,
    name: 'Math Quiz',
    questions: 20
};
console.log(quiz.name);  // 'Math Quiz'

/* Arrays */
const items = ['item1', 'item2', 'item3'];
console.log(items[0]);  // 'item1'
console.log(items.length);  // 3

/* null vs undefined */
const x = null;  // Intentionally empty
const y = undefined;  // Not assigned
```

### Functions

```javascript
/* Function declaration */
function addNumbers(a, b) {
    return a + b;
}
console.log(addNumbers(5, 3));  // 8

/* Arrow function (modern) */
const multiply = (a, b) => {
    return a * b;
};
const multiply2 = (a, b) => a * b;  // Shorthand

/* Function with parameters */
function showMessage(message, type = 'info') {
    console.log(`[${type}] ${message}`);
}
showMessage('Hello');  // [info] Hello
showMessage('Error', 'error');  // [error] Error

/* Higher-order functions */
const numbers = [1, 2, 3, 4, 5];

// map: transform each item
const doubled = numbers.map(n => n * 2);  // [2, 4, 6, 8, 10]

// filter: keep items matching condition
const even = numbers.filter(n => n % 2 === 0);  // [2, 4]

// reduce: combine items into single value
const sum = numbers.reduce((total, n) => total + n, 0);  // 15
```

---

## Event Listeners

### Ý Nghĩa
Event Listeners "lắng nghe" các sự kiện (click, submit, change) và chạy code khi sự kiện xảy ra:

```html
<button id="submitBtn">Submit</button>

<script>
    // Lắng nghe event
    document.getElementById('submitBtn').addEventListener('click', () => {
        console.log('Button clicked!');
    });
</script>
```

### Syntax

```javascript
element.addEventListener('eventName', (event) => {
    // Code chạy khi event xảy ra
});
```

### Common Events

| Event | Khi nào | Ví dụ |
|-------|---------|-------|
| `click` | Click vào element | Button, link |
| `submit` | Submit form | `form.addEventListener('submit', ...)` |
| `change` | Giá trị input thay đổi | Select, radio, checkbox |
| `input` | Người dùng nhập text | Text input |
| `focus` | Focus vào input | `input.focus()` |
| `blur` | Mất focus khỏi input | `input.blur()` |
| `mouseover` | Hover vào element | Links, buttons |
| `mouseout` | Hover ra khỏi | |
| `keydown` | Nhấn phím | Keyboard |
| `load` | Page tải xong | `window.addEventListener('load', ...)` |
| `scroll` | Scroll trang | `window.addEventListener('scroll', ...)` |

### Event Object

```javascript
button.addEventListener('click', (event) => {
    console.log(event.type);        // 'click'
    console.log(event.target);      // Element được click
    console.log(event.target.id);   // ID của element
    
    event.preventDefault();         // Ngừng hành động mặc định
    event.stopPropagation();        // Ngừng event bubble
});
```

### Form Submit Event

```javascript
// ❌ Don't use button onclick
<button onclick="submitForm()">Submit</button>

// ✅ Use addEventListener on form
document.getElementById('myForm').addEventListener('submit', (e) => {
    e.preventDefault();  // Prevent default form submission (reload page)
    
    // Do custom logic here
    const formData = new FormData(document.getElementById('myForm'));
    // Send to server, etc.
});
```

---

## DOM Manipulation

### DOM (Document Object Model)
DOM là tree representation của HTML:

```html
<html>
    <body>
        <div id="container">
            <h1>Title</h1>
            <button id="submitBtn">Submit</button>
        </div>
    </body>
</html>
```

### Finding Elements

```javascript
/* By ID */
const element = document.getElementById('myId');

/* By class */
const elements = document.getElementsByClassName('myClass');

/* By tag name */
const buttons = document.getElementsByTagName('button');

/* Modern: CSS selectors */
const element = document.querySelector('#myId');           // First match
const elements = document.querySelectorAll('.myClass');    // All matches
const button = document.querySelector('button.primary');   // Specific
```

### Accessing & Changing Properties

```javascript
/* Get/set text content */
const element = document.getElementById('myElement');
console.log(element.textContent);   // Current text
element.textContent = 'New text';   // Change text

/* Get/set HTML */
element.innerHTML = '<strong>Bold text</strong>';

/* Get/set value (for inputs) */
const input = document.getElementById('nameInput');
console.log(input.value);      // Current value
input.value = 'New value';     // Change value

/* Get/set attributes */
element.getAttribute('class');      // Get attribute
element.setAttribute('class', 'active');  // Set attribute

/* Get/set classes */
element.classList.add('active');       // Add class
element.classList.remove('active');    // Remove class
element.classList.toggle('active');    // Toggle class
```

### Changing Styles

```javascript
const element = document.getElementById('myElement');

/* Inline styles (avoid for big projects) */
element.style.color = 'red';
element.style.fontSize = '20px';
element.style.display = 'none';
element.style.backgroundColor = '#f5f5f5';

/* Better: use classes */
element.classList.add('error');  // Define .error in CSS
```

### Creating & Removing Elements

```javascript
/* Create element */
const div = document.createElement('div');
div.textContent = 'Hello';
div.className = 'message';

/* Add to page */
const container = document.getElementById('container');
container.appendChild(div);  // Add as last child
container.insertBefore(div, container.firstChild);  // Add as first

/* Remove element */
div.remove();  // Remove from page

/* Clear all children */
container.innerHTML = '';  // Remove all children
```

### Example: Upload Form Feedback

```html
<form id="uploadForm">
    <input type="file" id="fileInput" required>
    <button type="submit">Upload</button>
</form>
<div id="uploadProgress" style="display: none;">
    <p>Uploading...</p>
</div>

<script>
    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show progress
        const progress = document.getElementById('uploadProgress');
        progress.style.display = 'block';
        
        try {
            // Upload logic here
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: new FormData(e.target)
            });
            
            const result = await response.json();
            
            // Hide progress
            progress.style.display = 'none';
            
            // Show success message
            const msg = document.createElement('div');
            msg.textContent = '✅ Upload successful!';
            msg.className = 'message success';
            document.body.appendChild(msg);
            
        } catch (error) {
            progress.style.display = 'none';
            // Show error
        }
    });
</script>
```

---

## FormData & File Upload

### FormData Object

```javascript
/* Create FormData */
const formData = new FormData();

/* Add text fields */
formData.append('quiz_name', 'Math Quiz');
formData.append('description', 'Chapter 1');

/* Add file */
const fileInput = document.getElementById('fileInput');
const file = fileInput.files[0];
formData.append('file', file);

/* Access FormData values */
for (let [key, value] of formData.entries()) {
    console.log(`${key}: ${value}`);
}
```

### Sending Files

```javascript
const formData = new FormData();
formData.append('quiz_name', 'My Quiz');
formData.append('file', document.getElementById('fileInput').files[0]);

/* Send to server */
const response = await fetch('/api/quizzes', {
    method: 'POST',
    body: formData
    // Don't set Content-Type header!
    // Browser will auto-set as multipart/form-data
});

const result = await response.json();
```

### File Validation

```javascript
const fileInput = document.getElementById('excelFile');
const file = fileInput.files[0];

if (!file) {
    showError('Please select a file');
    return;
}

// Check file type
if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
    showError('Only .xlsx or .xls files accepted');
    return;
}

// Check file size
const MAX_SIZE = 10 * 1024 * 1024;  // 10 MB
if (file.size > MAX_SIZE) {
    showError('File too large (max 10 MB)');
    return;
}

// File is valid, proceed
console.log('File valid:', file.name, file.size);
```

---

## Async & Await

### Ý Nghĩa
**Async/Await** là cách hiện đại để xử lý **bất đồng bộ** (asynchronous) code:

```javascript
/* ❌ Callback Hell (cũ) */
fetch('/api/data')
    .then(response => {
        response.json().then(data => {
            console.log(data);
        });
    });

/* ✅ Async/Await (hiện đại) */
async function getData() {
    const response = await fetch('/api/data');
    const data = await response.json();
    console.log(data);
}
```

### Async Function

```javascript
/* Define async function */
async function myAsyncFunction() {
    // Can use await inside
    const result = await somePromise();
    return result;
}

/* Call async function */
myAsyncFunction().then(result => {
    console.log('Result:', result);
});

/* Or with await */
const result = await myAsyncFunction();
```

### Await

```javascript
/* await pauses execution until Promise resolves */
const response = await fetch('/api/quiz');
console.log('Response received');  // Runs after response

const data = await response.json();
console.log('Data parsed');  // Runs after parsing
```

### Error Handling with Try/Catch

```javascript
async function uploadFile() {
    try {
        // Code that might fail
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Success:', result);
        
    } catch (error) {
        // Handle errors
        console.error('Error:', error.message);
        showMessage('Upload failed', 'error');
    }
}
```

---

## Fetch API

### Syntax

```javascript
fetch(url, options)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

/* Or with async/await */
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
```

### GET Request

```javascript
async function getQuizzes() {
    const response = await fetch('/api/quizzes');
    
    // Check if response is OK (200-299)
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
}
```

### POST Request (JSON)

```javascript
async function createSession(quizId) {
    const response = await fetch('/api/sessions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            quiz_id: quizId,
            num_questions: 20,
            exam_duration: 60
        })
    });
    
    return await response.json();
}
```

### POST Request (FormData - for file upload)

```javascript
async function uploadQuiz(formData) {
    const response = await fetch('/api/quizzes', {
        method: 'POST',
        body: formData
        // Don't set Content-Type! Browser auto-detects
    });
    
    return await response.json();
}
```

### Response Handling

```javascript
const response = await fetch('/api/data');

/* Check status */
console.log(response.status);       // 200, 404, 500, etc.
console.log(response.ok);           // true if 200-299

/* Parse response body (must call once) */
const data = await response.json();     // Parse as JSON
const text = await response.text();     // Parse as text
const blob = await response.blob();     // Parse as binary

/* Access headers */
console.log(response.headers.get('content-type'));
```

---

## Error Handling

### Types of Errors

```javascript
/* Network error - no internet */
try {
    const response = await fetch('/api/data');
} catch (error) {
    console.error('Network error:', error.message);  // 'Failed to fetch'
}

/* Wrong response type */
const response = await fetch('/api/data');
const contentType = response.headers.get('content-type');
if (!contentType.includes('application/json')) {
    throw new Error('Expected JSON but got: ' + contentType);
}

/* Server error - success: false */
const data = await response.json();
if (!data.success) {
    throw new Error(data.message || 'Server error');
}

/* Application error */
if (!file) {
    throw new Error('File is required');
}
```

### Error Handling Pattern (QuizGenerator)

```javascript
async function uploadFile(formData) {
    try {
        // Show loading
        document.getElementById('uploadProgress').style.display = 'block';
        
        // Send request
        const response = await fetch('/api/quizzes', {
            method: 'POST',
            body: formData
        });
        
        // Layer 1: Check if response is JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            throw new Error(`Server error (${response.status}): ${text.substring(0, 100)}`);
        }
        
        // Layer 2: Parse JSON
        const result = await response.json();
        
        // Layer 3: Check success flag
        if (!result.success) {
            throw new Error(result.message || 'Upload failed');
        }
        
        // Success!
        showMessage('✅ Upload successful!', 'success');
        setTimeout(() => {
            window.location.href = '/list-quizzes';
        }, 2000);
        
    } catch (error) {
        // All errors go here
        showMessage(`❌ ${error.message}`, 'error');
        
    } finally {
        // Always run (success or error)
        document.getElementById('uploadProgress').style.display = 'none';
    }
}
```

---

## Common Patterns

### Message Display

```javascript
function showMessage(text, type = 'info') {
    const container = document.getElementById('messageContainer');
    container.textContent = text;
    container.className = `message message-${type}`;
    container.style.display = 'block';
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        container.style.display = 'none';
    }, 3000);
}

/* Usage */
showMessage('✅ Success!', 'success');
showMessage('❌ Error occurred', 'error');
showMessage('⚠️ Warning', 'warning');
```

### Form Validation & Submit

```javascript
document.getElementById('myForm').addEventListener('submit', async (e) => {
    e.preventDefault();  // Prevent page reload
    
    // Validate inputs
    const name = document.getElementById('name').value;
    const file = document.getElementById('file').files[0];
    
    if (!name) {
        showMessage('Name is required', 'error');
        return;
    }
    
    if (!file) {
        showMessage('File is required', 'error');
        return;
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    
    try {
        // Submit
        const formData = new FormData();
        formData.append('name', name);
        formData.append('file', file);
        
        const response = await fetch('/api/submit', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message);
        }
        
        showMessage('✅ Submitted!', 'success');
        e.target.reset();  // Clear form
        
    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
});
```

### Page Redirect

```javascript
/* After 2 seconds */
setTimeout(() => {
    window.location.href = '/quiz-list';
}, 2000);

/* Immediately */
window.location.href = '/exam';

/* Back to previous page */
window.history.back();
```

### Toggle Visibility

```javascript
const element = document.getElementById('myElement');

/* Show/hide */
element.style.display = 'block';   // Show
element.style.display = 'none';    // Hide

/* Toggle */
if (element.style.display === 'none') {
    element.style.display = 'block';
} else {
    element.style.display = 'none';
}

/* Better: use class toggling */
element.classList.toggle('hidden');  // Requires CSS .hidden { display: none; }
```

---

## Tóm Tắt

**JavaScript trong QuizGenerator:**
- ✅ Event listeners: submit, click, change
- ✅ DOM manipulation: getElementById, textContent, style
- ✅ FormData: append text + files
- ✅ Async/await: non-blocking code execution
- ✅ Fetch API: GET/POST requests, error handling
- ✅ Error handling: try/catch + validation tầng

**Best Practices:**
1. Always use `try/catch` với async/await
2. Validate ở frontend + backend
3. Use `e.preventDefault()` on form submit
4. Don't set `Content-Type` for FormData (auto-detect)
5. Check `response.ok` or `result.success`
6. Provide user feedback (loading, success, error messages)
