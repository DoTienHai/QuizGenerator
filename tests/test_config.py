import os
import pytest


def test_get_config_returns_development_without_database_url(monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)
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
