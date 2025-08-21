"""
Pytest Configuration and Fixtures

Shared test configuration and fixtures for the FastAPI application tests.
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture
def client():
    """
    Test client fixture
    
    Returns:
        TestClient: FastAPI test client instance
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_settings():
    """
    Mock settings fixture for testing
    
    Returns:
        dict: Mock settings configuration
    """
    return {
        "VERSION": "1.0.0-test",
        "ENVIRONMENT": "testing",
        "DEBUG": True,
        "HOST": "127.0.0.1",
        "PORT": 8000,
    }


@pytest.fixture(autouse=True)
def set_test_environment(monkeypatch):
    """
    Automatically set test environment for all tests
    
    Args:
        monkeypatch: Pytest monkeypatch fixture
    """
    monkeypatch.setenv("STOCK_ENVIRONMENT", "testing")
    monkeypatch.setenv("STOCK_ENABLE_CACHE", "false")
    monkeypatch.setenv("STOCK_MAX_RETRIES", "1")