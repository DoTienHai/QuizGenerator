"""
Configuration for QuizGenerator Flask App
Environment-specific settings (Development, Testing, Production)
"""

import os
from datetime import timedelta


class Config:
    """Base configuration - settings shared across all environments"""
    
    # ==================== SQLAlchemy Settings ====================
    # SQLALCHEMY_TRACK_MODIFICATIONS
    #   - False: disable automatic tracking of object changes
    #   - Benefit: saves memory, improves performance
    #   - Recommended: always False (SQLAlchemy warns if not set)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLALCHEMY_RECORD_QUERIES
    #   - True: record all executed SQL queries for debugging
    #   - Use: identify N+1 query problems, performance analysis
    #   - Cost: uses memory, only enable in development
    SQLALCHEMY_RECORD_QUERIES = True
    
    # ==================== Session Settings ====================
    # PERMANENT_SESSION_LIFETIME
    #   - Value: 24 hours (session timeout)
    #   - Behavior: user must re-login after 24h of no activity
    #   - If not set: session ends when browser closes
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # SESSION_COOKIE_SECURE
    #   - True: cookie only sent over HTTPS (not HTTP)
    #   - Protects against man-in-the-middle attacks
    #   - Note: override to False in development (localhost has no HTTPS)
    SESSION_COOKIE_SECURE = True
    
    # SESSION_COOKIE_HTTPONLY
    #   - True: JavaScript cannot access cookie (cannot be stolen via XSS)
    #   - Protects against Cross-Site Scripting (XSS) attacks
    #   - Recommended: keep True (security best practice)
    SESSION_COOKIE_HTTPONLY = True
    
    # SESSION_COOKIE_SAMESITE
    #   - 'Lax': cookie sent if top-level navigation (balanced security/usability)
    #   - 'Strict': never sent in cross-site requests
    #   - 'None': sent everywhere (requires Secure=True, requires HTTPS)
    #   - Protects against Cross-Site Request Forgery (CSRF)
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # ==================== Upload Settings ====================
    # MAX_CONTENT_LENGTH
    #   - Value: 16 * 1024 * 1024 = 16 MB
    #   - Limit: maximum file upload size
    #   - Behavior: Flask auto-rejects uploads > 16 MB (413 Payload Too Large)
    #   - Suitable: Excel file uploads (typical size 1-10 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class DevelopmentConfig(Config):
    """Development environment - localhost coding and testing"""
    
    # ==================== Flask Settings ====================
    # DEBUG = True
    #   - Behavior: auto-reloads on code changes (hot reload)
    #   - Shows: detailed error tracebacks + interactive debugger
    #   - ⚠️  NEVER use in production (critical security risk)
    DEBUG = True
    
    # TESTING = False
    #   - False: normal mode (not test mode)
    #   - Use TestingConfig for unit tests with isolated DB
    TESTING = False
    
    # ==================== Database ====================
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_generator.db'
    #   - Database: SQLite file (quiz_generator.db in project root)
    #   - Auto-created: first run of app.py creates the file + 5 tables
    #   - Tables: quiz, question, exam_session, user_answer, exam_result
    #   - Good for: MVP development (zero setup, portable)
    #   - Bad for: production (single connection, not scalable)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_generator.db'
    
    # SQLALCHEMY_ECHO = True
    #   - Prints: all SQL queries to console in real-time
    #   - Shows: SELECT, INSERT, UPDATE statements as they execute
    #   - Debug: performance issues, see generated SQL, N+1 problems
    #   - Note: disable in production (noise + performance)
    SQLALCHEMY_ECHO = False
    
    # ==================== Security (Relaxed for localhost) ====================
    # SESSION_COOKIE_SECURE = False
    #   - False: accept HTTP cookies (not HTTPS-only)
    #   - Why: localhost has no HTTPS, browsers reject Secure cookies on HTTP
    #   - Override: from base Config which has Secure=True
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    """Testing environment - unit tests with isolated database"""
    
    # ==================== Flask Settings ====================
    # DEBUG = True
    #   - Include: useful debugging info during test execution
    DEBUG = True
    
    # TESTING = True
    #   - Disable: request context exceptions (allows testing without app context)
    TESTING = True
    
    # ==================== Database ====================
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    #   - Database: in-memory SQLite (exists only during test run)
    #   - Auto-cleanup: database deleted when test finishes
    #   - Speed: fast execution (no disk I/O)
    #   - Isolation: no side effects between tests, no data persistence
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # SQLALCHEMY_ECHO = False
    #   - Quiet: don't log SQL queries (cleaner test output)
    SQLALCHEMY_ECHO = False
    
    # ==================== Security ====================
    # SESSION_COOKIE_SECURE = False
    #   - Allow: HTTP cookies in tests (tests run on localhost)
    SESSION_COOKIE_SECURE = False


# ==================== Config Selector ====================
def get_config():
    """
    Get application configuration
    
    Current behavior:
    - Uses DevelopmentConfig (hardcoded for MVP development)
    - SQLite database: quiz_generator.db
    - Auto-reload enabled: DEBUG=True
    - SQL queries logged: SQLALCHEMY_ECHO=True
    
    Available configurations:
    - DevelopmentConfig: SQLite, DEBUG=True, detailed logging, localhost
    - TestingConfig: In-memory DB, fast unit tests, isolated
    """
    # Hardcoded to development (MVP stage)
    env = 'development'
    
    # Map environment names to config classes
    config_map = {
        'development': DevelopmentConfig,      # SQLite, DEBUG=True, SQLALCHEMY_ECHO=True
        'testing': TestingConfig,              # In-memory DB, DEBUG=True
    }
    
    # Return the appropriate config class for environment
    return config_map.get(env, DevelopmentConfig)
