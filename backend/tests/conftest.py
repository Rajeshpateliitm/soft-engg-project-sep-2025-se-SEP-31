"""
Pytest configuration and fixtures for WasteWise API testing.
"""
import pytest
import os
import sys
from datetime import datetime, date

# Add the backend directory to the path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)


class TestConfig:
    """Test configuration."""
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "test-jwt-secret-key"
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60
    TESTING = True
    SCHEDULER_API_ENABLED = False  # Disable scheduler during tests
    
    # Gemini API config (mock for testing)
    GEMINI_API_KEY = ""
    GEMINI_API_MODEL = "gemini-1.5-flash"
    GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    
    # Mail config (disabled for testing)
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = "test@wastewise.com"


@pytest.fixture(scope='session')
def app():
    """Create application for the entire test session."""
    from app import create_app
    
    application = create_app(TestConfig)
    
    # Push application context for the session
    ctx = application.app_context()
    ctx.push()
    
    yield application
    
    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    """Create test client for each test function."""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


# Helper functions for tests

def register_primary_user(client, email="testuser@test.com", password="TestPass123"):
    """Helper to register a primary user and return the response.
    
    Uses ward_number "1" (Park Street) and pincode "700001" which exist in seeded data.
    """
    return client.post('/api/auth/register', json={
        "email": email,
        "password": password,
        "house_number": "101",
        "ward_number": "1",  # Park Street ward
        "family_members": 4,
        "pincode": "700001"  # Park Street pincode
    })


def login_user(client, email, password):
    """Helper to login a user and return the response."""
    return client.post('/api/auth/login', json={
        "email": email,
        "password": password
    })


def get_auth_header(client, email, password):
    """Helper to get authorization header for authenticated requests."""
    response = login_user(client, email, password)
    if response.status_code == 200:
        token = response.get_json()['access_token']
        return {"Authorization": f"Bearer {token}"}
    return None


@pytest.fixture
def primary_user_token(client):
    """Create a primary user and return auth header."""
    import uuid
    # Use unique email for each test to avoid conflicts
    unique_email = f"primary_test_{uuid.uuid4().hex[:8]}@test.com"
    register_primary_user(client, unique_email, "PrimaryTest123")
    return get_auth_header(client, unique_email, "PrimaryTest123")


@pytest.fixture
def collector_token(client):
    """Get auth header for the predefined collector (from init_sample_data)."""
    return get_auth_header(client, "collector1@wastewise.com", "Collector@123")


@pytest.fixture
def rwa_manager_token(client):
    """Get auth header for the predefined RWA manager (from init_sample_data)."""
    return get_auth_header(client, "rwa_manager1@wastewise.com", "RWA@Manager123")


@pytest.fixture
def tertiary_token(client):
    """Get auth header for the predefined tertiary user (from init_sample_data)."""
    return get_auth_header(client, "tertiary@wastewise.com", "Tertiary@123")
