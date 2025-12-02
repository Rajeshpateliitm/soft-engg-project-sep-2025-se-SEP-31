# WasteWise API Test Suite

This directory contains comprehensive API tests for the WasteWise waste management system using pytest, based on the **OpenAPI 3.0.3 specification** (`api_swagger.yaml`).

## Test Structure

```
tests/
├── __init__.py                  # Package initialization
├── conftest.py                  # Pytest fixtures and configuration
├── requirements-test.txt        # Test dependencies
├── README.md                    # This file
├── test_api_documentation.py    # Tests based on API documentation (swagger)
├── test_api_discrepancies.py    # Tests showing actual vs expected differences
├── test_auth.py                 # Authentication API tests
├── test_primary.py              # Primary User API tests
├── test_secondary.py            # Secondary User (RWA/Collector) API tests
├── test_tertiary.py             # Tertiary User (Government/NGO) API tests
├── test_common.py               # Common API tests (recyclers, wards)
└── test_genai.py                # GenAI/Chatbot API tests
```

## Test Design (Input, Expected Output, Actual Output)

Each test case includes:
- **Input**: The request data sent to the API
- **Expected Output**: What the API should return according to documentation
- **Actual Output**: What the API actually returns

### Example Test Case Format

```python
def test_login_success(self, client):
    """
    Test Case: Successful login
    
    Input: Valid email and password
    Expected: 200 OK with access_token, token_type, and user object
    """
    # INPUT
    input_data = {
        "email": "user@test.com",
        "password": "password123"
    }
    
    # EXPECTED OUTPUT (from api_swagger.yaml)
    expected_status = 200
    expected_fields = ["access_token", "token_type", "user"]
    
    # ACTUAL OUTPUT
    response = client.post('/api/auth/login', json=input_data)
    actual_status = response.status_code
    actual_data = response.get_json()
    
    # ASSERTIONS
    assert actual_status == expected_status
    for field in expected_fields:
        assert field in actual_data
```

## API Documentation vs Implementation Discrepancies

The `test_api_discrepancies.py` file specifically demonstrates cases where the actual API behavior differs from documentation, showing how testing helps improve APIs:

| Discrepancy | Documentation | Actual Implementation |
|-------------|--------------|----------------------|
| Waste Log Request | `category`, `quantity_kg` | `wet_waste`, `dry_waste`, `hazardous_waste` |
| Pickup Accept Points | Fixed 15 points | Dynamic based on separated/recycled flags |
| Password Validation | minLength: 6 | May accept shorter passwords |

## Setup

### 1. Install Test Dependencies

```bash
cd backend
pip install -r tests/requirements-test.txt
```

Or install directly:

```bash
pip install pytest pytest-cov pytest-mock
```

### 2. Make sure main dependencies are installed

```bash
pip install -r requirements.txt
```

## Running Tests

### Run All Tests

```bash
cd backend
python -m pytest tests/ -v
```

### Run Documentation-Based Tests

```bash
python -m pytest tests/test_api_documentation.py -v
```

### Run Discrepancy Tests

```bash
python -m pytest tests/test_api_discrepancies.py -v
```

### Run Specific Test File

```bash
python -m pytest tests/test_auth.py -v
python -m pytest tests/test_primary.py -v
python -m pytest tests/test_secondary.py -v
python -m pytest tests/test_tertiary.py -v
python -m pytest tests/test_common.py -v
python -m pytest tests/test_genai.py -v
```

### Run with Coverage Report

```bash
python -m pytest tests/ --cov=app --cov-report=term-missing
```

### Run with HTML Coverage Report

```bash
python -m pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

## Test Categories

### API Documentation Tests (`test_api_documentation.py`)
Tests directly based on the OpenAPI swagger specification:
- Authentication endpoints (register, login, me)
- Primary user endpoints (dashboard, quiz, waste-log, leaderboard, campaigns)
- Secondary user endpoints (dashboards, pickup management, campaigns)
- Tertiary user endpoints (dashboard, ward performance, summaries)
- Common endpoints (recyclers, wards, pickup requests)
- GenAI endpoints (chat, clear history)
- Health check endpoints

### Discrepancy Tests (`test_api_discrepancies.py`)
Tests showing where actual and expected outputs differ:
- Field naming differences
- Validation behavior differences
- Response format inconsistencies
- Edge case handling

### Authentication Tests (`test_auth.py`)
- User registration (success, validation errors, duplicates)
- User login (success, wrong credentials)
- Token-based authentication (`/api/auth/me`)
- Role-based access (PRIMARY, SECONDARY, TERTIARY users)

### Primary User Tests (`test_primary.py`)
- Dashboard data retrieval
- Quiz system (get questions, submit answers, performance tracking)
- Waste logging (create, retrieve, summary)
- Leaderboard
- Monthly engagement analytics
- Campaign registration

### Secondary User Tests (`test_secondary.py`)
- RWA Manager dashboard (admin role only)
- Collector dashboard (collector role only)
- Pickup management (accept/reject)
- RWA leaderboard
- Pickup summary and details
- Waste summary for households
- Campaign management (CRUD)

### Tertiary User Tests (`test_tertiary.py`)
- Government/NGO dashboard
- Ward performance summaries
- Ward-level detailed summaries
- Update ward monthly summaries

### Common API Tests (`test_common.py`)
- Get recycler locations by pincode
- Get all wards
- Create pickup requests
- Health check endpoint

### GenAI Tests (`test_genai.py`)
- Chat endpoint (with mocked Gemini API)
- Chat history clearing
- Random quiz generation
- Error handling for API failures

## Test Fixtures

The `conftest.py` file provides these fixtures:

| Fixture | Description |
|---------|-------------|
| `app` | Flask application with test database |
| `client` | Test client for making HTTP requests |
| `primary_user_token` | Auth header for a registered primary user |
| `collector_token` | Auth header for predefined collector |
| `rwa_manager_token` | Auth header for predefined RWA manager |
| `tertiary_token` | Auth header for predefined tertiary user |

## Test Database

Tests use an **in-memory SQLite database** that is:
- Created fresh for each test session
- Seeded with sample data (users, wards, quiz questions, campaigns, recyclers)
- Uses transactions for test isolation

This ensures test isolation and repeatable results.

## Predefined Test Users

| Email | Password | Role |
|-------|----------|------|
| `collector1@wastewise.com` | `Collector@123` | Secondary (Collector) |
| `rwa_manager1@wastewise.com` | `RWA@Manager123` | Secondary (RWA Admin) |
| `tertiary@wastewise.com` | `Tertiary@123` | Tertiary (Government) |

Primary users are created dynamically during tests.

## API Coverage

The test suite covers all major API endpoints as documented in `api_swagger.yaml`:

| Endpoint Group | Endpoints Covered |
|---------------|-------------------|
| `/api/auth/*` | register, login, me |
| `/api/primary/*` | dashboard, quiz/*, waste-log, waste-summary, leaderboard, monthly-engagement, campaigns |
| `/api/secondary/*` | dashboard, collector/dashboard, rwa-leaderboard, pickup-*, campaigns/* |
| `/api/tertiary/*` | dashboard, ward-performance, ward/*/summary |
| `/api/common/*` | recyclers, wards, pickup-request |
| `/api/genai/*` | chat, chat/clear |
| `/api/health` | health check |
| `/` | root endpoint |

## Test Results Summary

Running all tests:
```
194 passed
```

## Continuous Integration

For CI/CD pipelines, use:

```bash
# Run tests with JUnit XML report
python -m pytest tests/ --junitxml=test-results.xml

# Run tests with coverage in CI
python -m pytest tests/ --cov=app --cov-report=xml
```

## Troubleshooting

### ImportError: No module named 'app'

Make sure you're running pytest from the `backend` directory:

```bash
cd backend
python -m pytest tests/
```

### Unicode Encoding Errors on Windows

Set the encoding environment variable:

```bash
$env:PYTHONIOENCODING='utf-8'
python -m pytest tests/ -v
```

### Tests are Slow

Some tests may be slow due to:
- Password hashing (uses strong algorithm)
- Database operations

Use `pytest -x` to stop on first failure for faster feedback during development.
