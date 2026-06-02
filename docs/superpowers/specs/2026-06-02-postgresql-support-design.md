# PostgreSQL Support Design

**Date**: 2026-06-02
**Status**: Approved

## Goal

Add PostgreSQL as the production database on Render while keeping SQLite for local development. The switch happens automatically via the `DATABASE_URL` environment variable injected by Render.

## Requirements

- Local dev: SQLite (no change, zero setup)
- Render production: PostgreSQL, fresh/empty on first deploy
- Auto-detect: no manual config switch required — presence of `DATABASE_URL` determines the database
- No data migration (PostgreSQL starts empty)

## Changes

### 1. `config.py`

Add `ProductionConfig` class and update `get_config()` to detect `DATABASE_URL`.

```python
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    # Render injects "postgres://" but SQLAlchemy 2.x requires "postgresql://"
    _db_url = os.environ.get('DATABASE_URL', '')
    SQLALCHEMY_DATABASE_URI = _db_url.replace('postgres://', 'postgresql://', 1)

def get_config():
    if os.environ.get('DATABASE_URL'):
        return ProductionConfig
    return DevelopmentConfig
```

### 2. `requirements.txt`

Add PostgreSQL driver:

```
psycopg2-binary==2.9.9
```

## Architecture

No changes to `app.py`, models, routes, or services. Flask-SQLAlchemy abstracts the database dialect — the same ORM code works for both SQLite and PostgreSQL.

Table creation on first deploy: `db.create_all()` in `app.py` runs at startup and creates all 5 tables on the empty PostgreSQL database automatically.

## Render Setup (already done)

- PostgreSQL service created on Render
- `DATABASE_URL` set to Internal Database URL in Web Service environment variables

## Data Flow

```
Render deploy starts
  → os.environ has DATABASE_URL
  → get_config() returns ProductionConfig
  → app.config uses postgresql:// URI
  → db.create_all() creates 5 tables on PostgreSQL
  → app serves requests using PostgreSQL
```

```
Local dev starts
  → os.environ has no DATABASE_URL
  → get_config() returns DevelopmentConfig
  → app.config uses sqlite:///quiz_generator.db
  → db.create_all() uses local SQLite file
```

## Error Handling

- If `DATABASE_URL` is set but malformed: SQLAlchemy raises `OperationalError` at startup — visible in Render logs
- If PostgreSQL service is down: connection error at startup — Render retries automatically

## Testing

- Existing `TestingConfig` (in-memory SQLite) is unaffected
- No new tests required — the change is config-only
