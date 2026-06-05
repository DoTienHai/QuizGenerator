"""
Pytest configuration and shared fixtures for QuizGenerator tests
Provides app, client, and db fixtures for all tests
"""

import pytest
from app import create_app
from modules.models import db as _db
from config import TestingConfig


@pytest.fixture(scope='function')
def app():
    """Create Flask app with TestingConfig and isolated in-memory database"""
    app = create_app(TestingConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create Flask test client for making HTTP requests"""
    return app.test_client()


@pytest.fixture(scope='function')
def db(app):
    """Provide database instance for tests"""
    return _db
