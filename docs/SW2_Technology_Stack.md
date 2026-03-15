# SW2: Technology Stack Selection - QuizGenerator

**Last Updated**: 2026-03-15  
**Version**: 1.0  
**Status**: Design Phase  
**Author**: AI Assistant

---

## Table of Contents

- [Technology Stack Overview](#technology-stack-overview)
- [Backend Stack](#backend-stack)
- [Frontend Stack](#frontend-stack)
- [Database Stack](#database-stack)
- [Development Tools](#development-tools)
- [Deployment & Hosting](#deployment--hosting)
- [Technology Justification](#technology-justification)
- [Ecosystem & Community Support](#ecosystem--community-support)
- [Migration & Upgrade Path](#migration--upgrade-path)

---

## Technology Stack Overview

### Current Stack (Phase 1 - MVP)

```
┌──────────────────────────────────────────────────┐
│ Presentation Layer (Frontend)                    │
│ HTML5 / CSS3 / JavaScript (Vanilla)              │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│ Application Layer                                │
│ Python 3.8+ / Flask 2.x                         │
│ Flask-SQLAlchemy, Flask-WTF, Flask-CORS        │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│ Data Layer                                       │
│ SQLAlchemy ORM / SQLite                         │
│ openpyxl (Excel parsing)                        │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│ Storage                                          │
│ SQLite Database / Local Filesystem              │
└──────────────────────────────────────────────────┘
```

---

## Backend Stack

### Framework: Flask

**Version**: 2.x (LTS)

**Why Flask?**
1. **Lightweight**: Perfect for MVP, no unnecessary features
2. **Flexible**: Choose your own libraries, not opinionated
3. **Pythonic**: Clean, readable code
4. **Rapid Development**: Quick to prototype and test
5. **Microframework**: Scales from small to large apps
6. **Large ecosystem**: Extensive third-party extensions

**Alternatives Considered**:
- Django: Too heavy for simple single-user app
- FastAPI: Modern but less mature at time of decision
- Bottle: Lighter but smaller community

**Installation**:
```bash
pip install Flask==2.3.0
```

---

### Language: Python 3.8+

**Why Python?**
1. **Readability**: Clear, maintainable code
2. **Rapid Development**: Less boilerplate than Java/C#
3. **Data Processing**: Excellent libraries for data manipulation
4. **Community**: Massive Python community, lots of libraries
5. **Educational**: Good learning curve
6. **Cross-platform**: Windows, Mac, Linux support

**Version Rationale**: 3.8+ for f-strings, type hints, performance

**Installation**:
```bash
# Windows
python --version  # Should be 3.8 or higher

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

---

### ORM: SQLAlchemy

**Version**: 1.4+ (with Flask-SQLAlchemy 3.x)

**Why SQLAlchemy?**
1. **Type Safety**: Python object mapping to database
2. **SQL Injection Prevention**: Automatic parameterization
3. **Database Agnostic**: Can switch databases easily
4. **Relationships**: Built-in support for table relationships
5. **Query Builder**: Powerful, readable query syntax
6. **Migrations**: Alembic integration for schema changes

**Installation**:
```bash
pip install Flask-SQLAlchemy==3.0.0
pip install alembic  # For migrations
```

**Usage**:
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    total_questions = db.Column(db.Integer, nullable=False)
```

---

### Excel Parsing: openpyxl

**Version**: 3.10+

**Why openpyxl?**
1. **Safe Parsing**: Doesn't execute formulas, just extracts values
2. **Modern Format**: Full .xlsx support
3. **Pure Python**: No external dependencies
4. **Well-maintained**: Active development

**Alternatives Considered**:
- xlrd: Doesn't support .xlsx
- pandas: Too heavy, requires numpy
- pyExcelerator: Outdated

**Installation**:
```bash
pip install openpyxl==3.10.0
```

**Usage**:
```python
from openpyxl import load_workbook

wb = load_workbook('questions.xlsx', data_only=True)
for row in wb.active.iter_rows(values_only=True):
    question, opt_a, opt_b, opt_c, opt_d, correct = row
```

---

### CSRF Protection: Flask-WTF

**Version**: 1.1+

**Why Flask-WTF?**
1. **CSRF Prevention**: Automatic CSRF token generation
2. **Flask-native**: Works seamlessly with Flask
3. **Form Validation**: Built-in form handling
4. **Session Integration**: Uses Flask sessions

**Installation**:
```bash
pip install Flask-WTF==1.1.0
```

**Usage**:
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# In template
<form method="POST">
    {{ csrf_token() }}
    ...
</form>
```

---

## Frontend Stack

### HTML5

**Why HTML5?**
1. **Semantic**: Proper structure with semantic elements
2. **Accessibility**: Native ARIA support
3. **Modern**: Supports media, forms, canvas
4. **No Framework**: Simple, fast, maintainable

**Key Elements**:
```html
<!-- Semantic structure -->
<header>
<nav>
<main>
<section>
<form>
```

---

### CSS3

**Why CSS3?**
1. **Responsive**: Flexbox and Grid for responsive design
2. **Modern**: Variables, animations, gradients
3. **Lightweight**: Pure CSS, no dependencies
4. **Performance**: No build step needed

**Approach**:
- Mobile-first responsive design
- CSS variables for theming
- Flexbox for layout
- Media queries for breakpoints

**Directory Structure**:
```
static/
└── css/
    ├── main.css      (Primary styles)
    ├── responsive.css (Media queries)
    └── components.css (Component styles)
```

---

### JavaScript (Vanilla)

**Why Vanilla JavaScript?**
1. **No Dependencies**: No framework overhead
2. **Fast**: Direct DOM manipulation
3. **Learning**: Good for understanding JS fundamentals
4. **Maintenance**: Easy to understand and modify

**Alternatives Considered**:
- React: Overkill for small app
- Vue: Good but adds complexity
- jQuery: Outdated, modern JS is cleaner

**Key Modules**:

**1. Timer Module** (timer.js):
```javascript
class ExamTimer {
    constructor(durationMinutes, onWarning, onExpire) {
        this.totalSeconds = durationMinutes * 60;
        this.remainingSeconds = this.totalSeconds;
        this.onWarning = onWarning;
        this.onExpire = onExpire;
    }
    
    start() {
        this.intervalId = setInterval(() => {
            this.remainingSeconds--;
            this.updateDisplay();
            
            if (this.remainingSeconds === 300) {  // 5 minutes
                this.onWarning();
            }
            
            if (this.remainingSeconds <= 0) {
                this.onExpire();
                this.stop();
            }
        }, 1000);
    }
    
    updateDisplay() {
        // Update MM:SS display
        const mins = Math.floor(this.remainingSeconds / 60);
        const secs = this.remainingSeconds % 60;
        document.getElementById('timer').textContent = 
            `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
}
```

**2. Validation Module** (validation.js):
```javascript
class FormValidator {
    static validateFileInput(file) {
        const maxSize = 10 * 1024 * 1024;  // 10 MB
        const allowedTypes = ['application/vnd.ms-excel', 
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
        
        if (file.size > maxSize) {
            return { valid: false, error: 'File exceeds 10 MB' };
        }
        if (!allowedTypes.includes(file.type)) {
            return { valid: false, error: 'Only Excel files allowed' };
        }
        return { valid: true };
    }
    
    static validateNumQuestions(num, max) {
        if (isNaN(num) || num < 1 || num > max) {
            return { valid: false, error: `Must be between 1 and ${max}` };
        }
        return { valid: true };
    }
}
```

**3. Exam Module** (exam.js):
```javascript
class ExamHandler {
    constructor() {
        this.currentQuestion = 0;
        this.answers = {};
    }
    
    selectAnswer(questionId, answer) {
        this.answers[questionId] = answer;
        this.saveAnswerLocally();
    }
    
    saveAnswerLocally() {
        localStorage.setItem('exam_answers', JSON.stringify(this.answers));
    }
    
    submitExam() {
        fetch('/api/sessions/' + sessionId + '/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.answers)
        })
        .then(response => response.json())
        .then(data => this.handleResults(data));
    }
}
```

---

## Database Stack

### Primary Database: SQLite

**Version**: 3.35+

**Why SQLite?**
1. **Zero Setup**: Single file, no server needed
2. **Perfect for Local Apps**: Ideal for per-user database
3. **Sufficient for Scale**: Handles 10000+ questions easily
4. **ACID Compliance**: Data integrity guaranteed
5. **Python Built-in**: No additional dependencies

**Alternatives Considered**:
- PostgreSQL: Overkill, requires server setup
- MySQL: Also overkill, more complex deployment
- MongoDB: Not suitable for relational data model

**File Location**:
```
project/
├── quizgenerator.db    (Main database)
├── quizgenerator-backup.db  (Backup)
└── ...
```

**Connection String**:
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///quizgenerator.db'
```

### Backup Strategy

```python
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'quizgenerator_backup_{timestamp}.db'
    shutil.copy('quizgenerator.db', backup_file)
    print(f"Database backed up to {backup_file}")
```

---

## Development Tools

### Virtual Environment: venv

**Why venv?**
1. **Built-in**: Part of Python 3.3+
2. **Isolation**: Separate dependencies per project
3. **Reproducibility**: Easy to recreate environment

**Setup**:
```bash
# Create
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Deactivate
deactivate
```

---

### Dependency Management: pip

**Why pip?**
1. **Standard**: Python's official package manager
2. **Package Index**: Access to 400,000+ packages
3. **Requirements File**: Easy to specify versions

**Requirements File** (requirements.txt):
```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
openpyxl==3.10.0
Flask-WTF==1.1.0
python-dotenv==1.0.0
werkzeug==2.3.0
```

**Installation**:
```bash
pip install -r requirements.txt
```

---

### Version Control: Git

**Why Git?**
1. **Industry Standard**: Used everywhere
2. **Distributed**: Works offline
3. **History**: Full audit trail
4. **Branching**: Easy to manage features

**Setup**:
```bash
git init
git add .
git commit -m "Initial commit"
```

---

### Code Editor: VS Code

**Why VS Code?**
1. **Free**: No license cost
2. **Extensions**: Huge ecosystem
3. **Integration**: Built-in terminal, git
4. **Performance**: Fast, lightweight
5. **Python Support**: Excellent Python extension

**Recommended Extensions**:
- Python (by Microsoft)
- Pylance (code intelligence)
- Thunder Client (API testing)
- Better Comments

---

### Environment Variables: python-dotenv

**Why python-dotenv?**
1. **Secrets Management**: Keep secrets out of code
2. **Environment-specific Config**: Different settings per environment
3. **Simple**: Easy to use

**Setup**:
```bash
pip install python-dotenv
```

**Usage**:
```python
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

---

## Deployment & Hosting

### Development Server

**Built-in Flask Server**:
```python
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
```

**Limitations**: Single-threaded, not for production

### Production Server

**WSGI Server: Gunicorn**

**Why Gunicorn?**
1. **Production-ready**: Handles concurrency properly
2. **Simple**: Easy to configure
3. **Reliable**: Widely used in production
4. **Python-native**: Perfect for Flask

**Installation**:
```bash
pip install gunicorn
```

**Running**:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Hosting Options

**Option 1: Local Machine** (Current MVP)
- No hosting cost
- Full control
- Easy development

**Option 2: Cloud VPS** (Phase 2)
- Heroku: Easy, managed
- AWS EC2: More control
- DigitalOcean: Cost-effective

---

## Technology Justification

### Decision Matrix

| Criterion | Flask | Django | FastAPI |
|-----------|-------|--------|---------|
| Learning Curve | ★★★ Medium | ★★ Easy | ★★★★ Steep |
| Setup Time | ★★★★ Quick | ★★ Slow | ★★★★ Quick |
| Flexibility | ★★★★ High | ★★ Low | ★★★★ High |
| Community | ★★★★ Large | ★★★★★ Largest | ★★★ Growing |
| Ecosystem | ★★★★ Mature | ★★★★★ Mature | ★★★ Emerging |
| **Overall** | **BEST** | Similar | Similar |

**Decision**: **Flask** chosen for balance of simplicity, flexibility, and community support

---

## Ecosystem & Community Support

### Python Community
- **Forum**: Stack Overflow, Reddit (/r/Python)
- **Documentation**: Excellent official docs
- **Packages**: 400,000+ on PyPI
- **Learning Resources**: Hundreds of tutorials

### Flask Community
- **Documentation**: Comprehensive official docs
- **Extensions**: 200+ official extensions
- **Tutorial**: Miguel Grinberg's Flask Mega-Tutorial
- **Community Size**: 310K+ GitHub stars

### SQLAlchemy Community
- **Documentation**: Very detailed docs
- **Maturity**: 17+ years of development
- **Users**: Used by major companies (Uber, Spotify, etc.)
- **Active Development**: Continuous updates

---

## Migration & Upgrade Path

### Phase 1 to Phase 2 Upgrade Strategy

**No Breaking Changes Planned**, but can:
1. Add authentication (new tables, no schema changes)
2. Add new features (extend existing tables)
3. Optimize database (migrate to PostgreSQL if needed)

### PostgreSQL Migration (If Needed)

```python
# Change connection string only
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/quizgen'

# All ORM code remains the same
# SQLAlchemy handles dialect differences
```

### Performance Optimization Path

1. **Phase 1**: SQLite (sufficient for MVP)
2. **Phase 2**: Consider PostgreSQL if:
   - Multiple concurrent users
   - > 100GB data
   - Complex queries needed
3. **Phase 3**: Add Redis caching if needed

### Framework Upgrade Path

```
Flask 2.x → Flask 3.x (when released)
Minor version changes: pip install --upgrade Flask
Breaking changes: Rare, well-documented
```

---

## Summary Table

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Backend** | Flask | 2.3+ | Lightweight, flexible, rapid development |
| **Language** | Python | 3.8+ | Readable, extensive libraries |
| **ORM** | SQLAlchemy | 1.4+ | Type-safe, SQL injection prevention |
| **Database** | SQLite | 3.35+ | Zero setup, perfect for local app |
| **Excel Parser** | openpyxl | 3.10+ | Safe, modern format support |
| **CSRF Protection** | Flask-WTF | 1.1+ | Built-in, Flask-native |
| **Frontend** | HTML5/CSS3/JS | ES6+ | No dependencies, fast, maintainable |
| **Environment** | venv | Python 3.3+ | Isolation, reproducibility |
| **Deployment** | Gunicorn | 20.1+ | Production-ready WSGI server |
| **Dev Tools** | Git, VS Code | Latest | Industry standards |

---

## References

- See `docs/SW1_Requirement_Analysis.md` for system constraints (Technology Stack)
- See `docs/SW2_System_Architecture.md` for architecture decisions
- See `docs/SW2_Database_Schema.md` for database design
- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
