# SW2: Security Design - QuizGenerator

**Last Updated**: 2026-04-13  
**Version**: 1.1  
**Status**: Implementation Phase  
**Author**: AI Assistant

---

## Table of Contents

- [Security Overview](#security-overview)
- [Threat Analysis](#threat-analysis)
- [Authentication & Authorization](#authentication--authorization)
- [Input Validation & Sanitization](#input-validation--sanitization)
- [Data Protection](#data-protection)
- [File Upload Security](#file-upload-security)
- [API Security](#api-security)
- [Infrastructure Security](#infrastructure-security)
- [Security Testing & Monitoring](#security-testing--monitoring)

---

## Security Overview

### Security Level
**Level 1 (Low Risk)** - Single user, local app, no sensitive personal data

### Security Approach
- Defense in depth (multiple layers)
- Principle of least privilege
- Secure defaults
- Regular security updates

### Compliance
- WCAG 2.1 (accessibility, includes usability)
- GDPR-compliant (if deployed in EU)
- Data protection best practices

---

## Threat Analysis

### Threat 1: Malicious Excel File Upload

**Risk**: Attacker uploads Excel with malicious content

**Threats**:
- Formula injection (Excel formulas executed)
- Oversized file (DoS)
- Corrupted file structure
- Malware embedded

**Mitigation**:
1. **File format validation**
   - Check file extension (.xlsx, .xls only)
   - Validate MIME type (application/vnd.ms-excel)
   - Inspect file headers (magic numbers)

2. **File size limit**: 10 MB maximum

3. **Safe parsing library**: Use `openpyxl` (Python)
   - Does not execute formulas
   - Safe extraction of cell values only

4. **Data validation**: Verify all inputs conform to schema
   - No special characters in question/options
   - Valid characters only (ASCII + Unicode)

5. **Quarantine**: Store uploaded files separately
   - Separate directory with restricted access
   - Delete after processing

---

### Threat 2: SQL Injection

**Risk**: Attacker injects SQL via form inputs

**Threats**:
- Unauthorized database access
- Data exfiltration
- Data modification/deletion

**Mitigation**:
1. **ORM (SQLAlchemy)**
   - Parameterized queries by default
   - No raw SQL exposed to user input
   - Prevents all SQL injection vectors

2. **Input validation**
   - Validate data types (integer, string, etc.)
   - Validate length constraints
   - Whitelist allowed values where applicable

3. **Example (Safe)**:
   ```python
   # Safe: SQLAlchemy ORM
   quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
   
   # Never do this:
   # quiz = db.session.execute(f"SELECT * FROM quiz WHERE quiz_id = {quiz_id}")
   ```

---

### Threat 3: Cross-Site Scripting (XSS)

**Risk**: Attacker injects JavaScript in question/options

**Threats**:
- Session hijacking
- Cookie theft
- Phishing
- Defacement

**Mitigation**:
1. **Template escaping**
   - Jinja2 auto-escapes by default
   - All user data escaped in templates

2. **Content Security Policy (CSP)**
   ```python
   @app.after_request
   def set_security_headers(response):
       response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
       return response
   ```

3. **Input validation**
   - No HTML allowed in text fields
   - Strip/reject tags from Excel data

4. **Output encoding**
   ```html
   <!-- Safe (auto-escaped) -->
   <p>{{ question_text }}</p>
   
   <!-- Only use if trusted -->
   <p>{{ question_text | safe }}</p>
   ```

---

### Threat 4: CSRF (Cross-Site Request Forgery)

**Risk**: Attacker tricks user into unauthorized actions

**Threats**:
- Submitting answers for user
- Uploading malicious quizzes
- Deleting user data

**Mitigation**:
1. **Flask-WTF CSRF protection**
   ```python
   from flask_wtf.csrf import CSRFProtect
   csrf = CSRFProtect(app)
   
   @app.route('/submit', methods=['POST'])
   @csrf.protect
   def submit():
       # Protected from CSRF
   ```

2. **CSRF tokens in forms**
   ```html
   <form method="POST">
       {{ csrf_token() }}
       <input name="answer" type="radio" value="A">
   </form>
   ```

3. **SameSite cookies**
   ```python
   app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
   app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
   ```

---

### Threat 5: Session Hijacking

**Risk**: Attacker obtains another user's session

**Threats**:
- Impersonation
- Data theft
- Exam tampering

**Mitigation**:
1. **Secure session IDs**
   - Use UUID4 (cryptographically secure)
   - Not sequential or predictable
   ```python
   import uuid
   session_id = str(uuid.uuid4())
   ```

2. **Session timeout**
   - 24-hour idle timeout
   - Auto-logout on expiration
   ```python
   expires_at = datetime.now() + timedelta(hours=24)
   ```

3. **Session validation**
   - Verify session exists before operations
   - Check session hasn't expired
   ```python
   session = ExamSession.query.get(session_id)
   if not session or session.status == 'expired':
       raise SessionError()
   ```

---

### Threat 6: Authorization Bypass

**Risk**: User accesses another user's sessions/results (Phase 2)

**Threats**:
- Viewing other user's scores
- Modifying other user's results

**Mitigation**:
1. **Access control checks**
   ```python
   @app.route('/results/<session_id>')
   def get_results(session_id):
       session = ExamSession.query.get(session_id)
       if session.user_id != current_user.id:
           abort(403)
   ```

2. **Resource-based authorization**
   - Check ownership before returning data
   - Fail closed (deny by default)

---

## Authentication & Authorization

### Phase 1 (Current)
**No authentication required** - Single user, local app

**Security Assumption**: Application runs locally on trusted machine

### Phase 2 (Future)
```
Authentication Method: Session-based with password
Authorization: User can only access own data
```

---

## Input Validation & Sanitization

### 1. Text Input Validation

**Rules**:
```python
class QuestionValidator:
    
    @staticmethod
    def validate_question_text(text):
        # Type check
        if not isinstance(text, str):
            raise ValueError("Must be string")
        
        # Length check
        if len(text) > 2000:
            raise ValueError("Max 2000 characters")
        
        if len(text.strip()) == 0:
            raise ValueError("Cannot be empty")
        
        # Character check (allow alphanumeric, punctuation, unicode)
        if contains_html_tags(text):
            raise ValueError("HTML not allowed")
        
        return text.strip()
    
    @staticmethod
    def validate_option_text(text):
        if not isinstance(text, str):
            raise ValueError("Must be string")
        if len(text) > 500:
            raise ValueError("Max 500 characters")
        if len(text.strip()) == 0:
            raise ValueError("Cannot be empty")
        return text.strip()
```

### 2. Numeric Input Validation

```python
class ConfigValidator:
    
    @staticmethod
    def validate_num_questions(num, max_available):
        if not isinstance(num, int):
            raise ValueError("Must be integer")
        if num < 1:
            raise ValueError("Minimum 1 question")
        if num > max_available:
            raise ValueError(f"Max {max_available} questions")
        return num
    
    @staticmethod
    def validate_duration(minutes):
        if not isinstance(minutes, int):
            raise ValueError("Must be integer")
        if minutes < 1:
            raise ValueError("Minimum 1 minute")
        if minutes > 480:  # 8 hours max
            raise ValueError("Maximum 480 minutes")
        return minutes
```

### 3. Choice Input Validation

```python
def validate_answer(answer):
    valid_answers = ['A', 'B', 'C', 'D']
    if answer not in valid_answers:
        raise ValueError(f"Must be one of: {valid_answers}")
    return answer
```

### 4. File Upload Validation

```python
from werkzeug.utils import secure_filename

def validate_uploaded_file(file):
    # Check if file exists
    if not file or file.filename == '':
        raise FileError("No file selected")
    
    # Check file extension
    allowed_extensions = {'xlsx', 'xls'}
    if not allowed_extension(file.filename, allowed_extensions):
        raise FileError("Only .xlsx and .xls files allowed")
    
    # Check MIME type
    if file.mimetype not in ['application/vnd.ms-excel', 
                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
        raise FileError("Invalid file format")
    
    # Check file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    if size > 10 * 1024 * 1024:  # 10 MB
        raise FileError("File too large (max 10 MB)")
    
    # Secure filename
    filename = secure_filename(file.filename)
    return file
```

---

## Data Protection

### 1. Data Encryption

**At Rest**:
```python
# If using sensitive data, encrypt with:
from cryptography.fernet import Fernet

key = Fernet.generate_key()  # Store in .env
cipher = Fernet(key)
encrypted = cipher.encrypt(data.encode())
```

**In Transit**:
```
- HTTPS/TLS (production)
- HTTP (development/local)
```

### 2. Hashing

**Passwords (Phase 2)**:
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Store hash, never plaintext
password_hash = generate_password_hash(password)

# Verify
if check_password_hash(password_hash, provided_password):
    # Correct password
```

### 3. Data Retention

**Current Policy**:
- Keep all session data indefinitely (single user)
- Delete only on explicit user request

**Recommended (Phase 2)**:
- Exam results: Keep 1 year
- Uploaded files: Keep for 30 days
- Sessions: Clean up after 24 hours

---

## File Upload Security

### 1. Safe Parsing

```python
from openpyxl import load_workbook

def safe_parse_excel(file_path):
    # openpyxl is safe (doesn't execute formulas)
    wb = load_workbook(file_path, data_only=True)
    valid_data = []
    
    for row in wb.active.iter_rows(values_only=True):
        # Extract values only, no formulas
        valid_data.append(row)
    
    return valid_data
```

### 2. File Storage

```python
import os
import tempfile

UPLOAD_FOLDER = 'uploads'
TEMP_FOLDER = tempfile.gettempdir()

def save_uploaded_file(file):
    # Generate unique filename
    import uuid
    filename = f"{uuid.uuid4()}.xlsx"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Create directory if not exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Save file
    file.save(filepath)
    
    # Set proper permissions (read-only for app user)
    os.chmod(filepath, 0o600)
    
    return filepath
```

### 3. File Cleanup

```python
import os
from datetime import datetime, timedelta

def cleanup_old_files():
    """Remove temporary files older than 7 days"""
    cutoff = datetime.now() - timedelta(days=7)
    
    for filename in os.listdir(TEMP_FOLDER):
        filepath = os.path.join(TEMP_FOLDER, filename)
        if os.stat(filepath).st_mtime < cutoff.timestamp():
            os.remove(filepath)
```

---

## API Security

### 1. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/submit', methods=['POST'])
@limiter.limit("5 per minute")  # Prevent spam
def submit_answers():
    pass
```

### 2. Request Validation

```python
from functools import wraps

def validate_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return {"error": "Content-Type must be application/json"}, 400
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/session', methods=['POST'])
@validate_json
def create_session():
    data = request.get_json()
    # data is guaranteed to be JSON
```

### 3. Error Handling

```python
@app.errorhandler(400)
def bad_request(error):
    # Don't expose implementation details
    return {
        "status": "error",
        "error": {
            "code": "INVALID_REQUEST",
            "message": "The request was invalid"
        }
    }, 400

@app.errorhandler(500)
def server_error(error):
    # Log internally, generic message to user
    logger.error(f"Server error: {error}")
    return {
        "status": "error",
        "error": {
            "code": "SERVER_ERROR",
            "message": "An internal server error occurred"
        }
    }, 500
```

---

## Infrastructure Security

### 1. Environment Variables

```python
# .env file (not committed to git)
DATABASE_URL=sqlite:///quizgenerator.db
SECRET_KEY=your-secret-key-here
DEBUG=False
```

**Correct usage**:
```python
import os
from dotenv import load_dotenv

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

### 2. Secret Key Management

```python
# Generate strong secret key
import os
secret_key = os.urandom(32).hex()
print(f"Add to .env: SECRET_KEY={secret_key}")

# In app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

### 3. Debug Mode

```python
# NEVER in production
app.config['DEBUG'] = False
app.config['TESTING'] = False
```

### 4. Security Headers

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

---

## Security Testing & Monitoring

### 1. Unit Tests

```python
import unittest

class SecurityTests(unittest.TestCase):
    
    def test_sql_injection_prevented(self):
        """Test that SQL injection is impossible"""
        malicious_input = "'; DROP TABLE quiz; --"
        result = Quiz.query.filter_by(name=malicious_input).first()
        # Should return None or raise no error
        self.assertIsNone(result)
    
    def test_xss_prevented(self):
        """Test that XSS is prevented"""
        xss_input = "<script>alert('xss')</script>"
        # Test that it's escaped in template
        rendered = self.app.jinja_env.from_string(
            "{{ text }}").render(text=xss_input)
        self.assertNotIn("<script>", rendered)
    
    def test_file_upload_validation(self):
        """Test file upload validation"""
        # Should reject non-Excel files
        result = validate_uploaded_file(mock_txt_file)
        self.assertRaises(FileError, result)
    
    def test_input_length_validation(self):
        """Test input length limits"""
        long_text = "a" * 3000  # Exceeds 2000 limit
        with self.assertRaises(ValueError):
            validate_question_text(long_text)
```

### 2. Security Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log security events
def log_security_event(event, details):
    logger.warning(f"SECURITY: {event} - {details}")

# Usage
try:
    validate_file(file)
except FileError as e:
    log_security_event("FILE_UPLOAD_REJECTED", str(e))
```

### 3. Regular Security Updates

```
# Keep dependencies updated
pip install --upgrade flask
pip install --upgrade sqlalchemy
pip install --upgrade werkzeug

# Check for vulnerabilities
pip install safety
safety check
```

### 4. Security Checklist

```
Phase 1 MVP:
✅ Input validation on all user inputs
✅ SQL injection prevention (ORM)
✅ XSS prevention (template auto-escape)
✅ Session ID security (UUID)
✅ File upload validation
✅ Error handling (no info leaks)
✅ Security headers in responses
✅ Environment variables for secrets

Phase 2 Enhancement:
❌ HTTPS/TLS encryption
❌ CSRF protection (if multi-page)
❌ Rate limiting
❌ Authentication mechanism
❌ Authorization checks
❌ Audit logging
❌ Security testing
```

---

## References

- See `docs/SW1_Requirement_Analysis.md` for security requirements (NFR-3)
- See `docs/SW2_API_Design.md` for API security
- See `docs/SW2_System_Architecture.md` for architecture security
- OWASP Top 10: https://owasp.org/www-project-top-ten/
