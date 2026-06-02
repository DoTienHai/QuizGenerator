# PostgreSQL Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the app automatically use PostgreSQL on Render (via `DATABASE_URL` env var) while keeping SQLite for local development.

**Architecture:** Add `ProductionConfig` to `config.py` that reads `DATABASE_URL` and fixes the `postgres://` → `postgresql://` prefix issue. Update `get_config()` to return `ProductionConfig` when `DATABASE_URL` is present. Add `psycopg2-binary` driver to `requirements.txt`.

**Tech Stack:** Flask-SQLAlchemy, psycopg2-binary, pytest

---

### Task 1: Write and run failing tests for config detection

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_config.py`

- [ ] **Step 1: Create the tests directory and empty `__init__.py`**

```bash
mkdir tests
touch tests/__init__.py
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_config.py`:

```python
import os
import pytest


def test_get_config_returns_development_without_database_url(monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)
    # Re-import to pick up env state
    import importlib
    import config
    importlib.reload(config)
    cfg = config.get_config()
    assert cfg.__name__ == 'DevelopmentConfig'


def test_get_config_returns_production_with_database_url(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgresql://user:pass@host/db')
    import importlib
    import config
    importlib.reload(config)
    cfg = config.get_config()
    assert cfg.__name__ == 'ProductionConfig'


def test_production_config_fixes_postgres_prefix(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgres://user:pass@host/db')
    import importlib
    import config
    importlib.reload(config)
    cfg = config.ProductionConfig
    assert cfg.SQLALCHEMY_DATABASE_URI.startswith('postgresql://')


def test_production_config_keeps_postgresql_prefix(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgresql://user:pass@host/db')
    import importlib
    import config
    importlib.reload(config)
    cfg = config.ProductionConfig
    assert cfg.SQLALCHEMY_DATABASE_URI == 'postgresql://user:pass@host/db'


def test_production_config_debug_is_false(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgresql://user:pass@host/db')
    import importlib
    import config
    importlib.reload(config)
    assert config.ProductionConfig.DEBUG is False
```

- [ ] **Step 3: Run tests and confirm they fail**

```bash
pytest tests/test_config.py -v
```

Expected: `ERROR` or `AttributeError: module 'config' has no attribute 'ProductionConfig'`

---

### Task 2: Implement `ProductionConfig` and update `get_config()`

**Files:**
- Modify: `config.py`

- [ ] **Step 1: Add `ProductionConfig` class after `TestingConfig`**

Open `config.py`. After the `TestingConfig` class (around line 128), add:

```python
class ProductionConfig(Config):
    """Production environment - Render deployment with PostgreSQL"""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False

    # Render injects DATABASE_URL as "postgres://..." but SQLAlchemy 2.x requires "postgresql://"
    _db_url = os.environ.get('DATABASE_URL', '')
    SQLALCHEMY_DATABASE_URI = _db_url.replace('postgres://', 'postgresql://', 1)
```

- [ ] **Step 2: Update `get_config()` to detect `DATABASE_URL`**

Replace the existing `get_config()` function body (currently hardcoded to `'development'`):

```python
def get_config():
    """
    Get application configuration based on environment.
    - DATABASE_URL present (Render/production): ProductionConfig with PostgreSQL
    - No DATABASE_URL (local dev): DevelopmentConfig with SQLite
    """
    if os.environ.get('DATABASE_URL'):
        return ProductionConfig

    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
    }
    env = os.environ.get('FLASK_ENV', 'development')
    return config_map.get(env, DevelopmentConfig)
```

- [ ] **Step 3: Run tests and confirm they all pass**

```bash
pytest tests/test_config.py -v
```

Expected output:
```
tests/test_config.py::test_get_config_returns_development_without_database_url PASSED
tests/test_config.py::test_get_config_returns_production_with_database_url PASSED
tests/test_config.py::test_production_config_fixes_postgres_prefix PASSED
tests/test_config.py::test_production_config_keeps_postgresql_prefix PASSED
tests/test_config.py::test_production_config_debug_is_false PASSED
5 passed
```

- [ ] **Step 4: Commit**

```bash
git add config.py tests/__init__.py tests/test_config.py
git commit -m "feat: add ProductionConfig with auto PostgreSQL detection via DATABASE_URL"
```

---

### Task 3: Add psycopg2-binary to requirements.txt

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Add the PostgreSQL driver**

Add this line to `requirements.txt` after the existing `SQLAlchemy==2.0.20` line:

```
psycopg2-binary==2.9.9
```

- [ ] **Step 2: Install locally to verify the package name is correct**

```bash
pip install psycopg2-binary==2.9.9
```

Expected: `Successfully installed psycopg2-binary-2.9.9` (or "already satisfied")

- [ ] **Step 3: Commit and push**

```bash
git add requirements.txt
git commit -m "chore: add psycopg2-binary for PostgreSQL support on Render"
git push origin main
```

After push, Render will auto-deploy. The app will:
1. Install `psycopg2-binary` from `requirements.txt`
2. Detect `DATABASE_URL` in the environment
3. Use `ProductionConfig` → connect to PostgreSQL
4. Run `db.create_all()` → create all 5 tables on the empty PostgreSQL database

---

## Verification

After Render deploy completes, check the deploy logs for:
```
✓ Database initialized: postgresql://...
✓ Tables created (quiz, question, exam_session, user_answer, exam_result)
```

If you see `sqlite:///` in the logs instead, `DATABASE_URL` was not detected — check Render environment variables.
