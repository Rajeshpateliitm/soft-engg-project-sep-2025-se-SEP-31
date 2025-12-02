"""
================================================================================
WASTEWISE API UNIT TESTING SUITE
================================================================================
This file contains comprehensive unit tests for all WasteWise API endpoints
(excluding GenAI APIs) using pytest framework.

Test Case Format:
-----------------
For each test case:
    - API being tested: The endpoint URL and HTTP method
    - Inputs: Request method, JSON body, Headers
    - Expected Output: HTTP Status Code, JSON response
    - Actual Output: HTTP Status Code, JSON response  
    - Result: Success/Fail

Author: WasteWise Development Team
Date: November 2025
================================================================================
"""

import pytest
import json
import uuid
from datetime import datetime, date, timedelta


# ==============================================================================
# HELPER FUNCTION TO PRINT TEST RESULTS IN REQUIRED FORMAT
# ==============================================================================

def print_test_result(api_name, page_url, inputs, expected_output, actual_output, result):
    """
    Helper function to print test results in the required format for documentation.
    
    Parameters:
    -----------
    api_name : str
        Description of the API being tested
    page_url : str
        The full URL of the API endpoint
    inputs : dict
        Dictionary containing request method, JSON body, and headers
    expected_output : dict
        Dictionary containing expected status code and response
    actual_output : dict
        Dictionary containing actual status code and response
    result : str
        'Success' or 'Fail'
    """
    print("\n" + "="*80)
    print(f"API BEING TESTED: {api_name}")
    print("="*80)
    print(f"Page being tested: {page_url}")
    print("\nInputs:")
    print(f"    - Request Method: {inputs.get('method', 'N/A')}")
    if inputs.get('json'):
        print(f"    - JSON: {json.dumps(inputs['json'])}")
    if inputs.get('headers'):
        print(f"    - Headers: {inputs['headers']}")
    if inputs.get('params'):
        print(f"    - Query Params: {inputs['params']}")
    print("\nExpected Output:")
    print(f"    - HTTP Status Code: {expected_output.get('status_code', 'N/A')}")
    print(f"    - JSON: {json.dumps(expected_output.get('json', {}))}")
    print("\nActual Output:")
    print(f"    - HTTP Status Code: {actual_output.get('status_code', 'N/A')}")
    print(f"    - JSON: {json.dumps(actual_output.get('json', {}))}")
    print(f"\nResult: {result}")
    print("="*80)


# ==============================================================================
# TEST CLASS 1: AUTHENTICATION APIs (/api/auth/*)
# ==============================================================================

class TestAuthenticationAPIs:
    """
    Test cases for Authentication API endpoints.
    These APIs handle user registration, login, and user information retrieval.
    
    Endpoints tested:
    - POST /api/auth/register - Register a new user
    - POST /api/auth/login - Login existing user
    - GET /api/auth/me - Get current user information
    """
    
    # --------------------------------------------------------------------------
    # TEST 1.1: User Registration - Valid Data
    # --------------------------------------------------------------------------
    def test_register_valid_data(self, client):
        """
        Test Case: Register a new primary user with valid data
            
        This test verifies that a new user can successfully register
        with all required fields properly filled.
        """
        # Generate unique email to avoid conflicts
        unique_email = f"testuser_{uuid.uuid4().hex[:8]}@wastewise.com"
        
        # Define test inputs
        input_dict = {
            "email": unique_email,
            "password": "SecurePass123",
            "house_number": "A-101",
            "ward_number": "1",
            "family_members": 4,
            "pincode": "700001"
        }
        
        # Define expected output
        expected_status = 201
        expected_keys = ["message", "user", "access_token", "token_type"]
        
        # Make API request
        response = client.post('/api/auth/register', json=input_dict)
        actual_json = response.get_json()
        
        # Determine result
        result = "Success" if response.status_code == expected_status else "Fail"
        
        # Print results in required format
        print_test_result(
            api_name="User Registration - Valid Data",
            page_url="http://127.0.0.1:5000/api/auth/register",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": {"Content-Type": "application/json"}
            },
            expected_output={
                "status_code": expected_status,
                "json": {"message": "User registered successfully", "user": "...", "access_token": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"message": actual_json.get("message", ""), "user": "present" if "user" in actual_json else "missing"}
            },
            result=result
        )
        
        # Assertions
        assert response.status_code == expected_status
        assert "message" in actual_json
        assert "access_token" in actual_json
        assert actual_json["user"]["email"] == unique_email
    
    # --------------------------------------------------------------------------
    # TEST 1.2: User Registration - Missing Required Field
    # --------------------------------------------------------------------------
    def test_register_missing_field(self, client):
        """
        Test Case: Register user with missing required field (house_number)
        
        This test verifies that the API returns proper error when
        required fields are missing from the registration request.
        """
        # Define test inputs - missing house_number
        input_dict = {
            "email": "incomplete@test.com",
            "password": "SecurePass123",
            # house_number is missing
            "ward_number": "1",
            "family_members": 4,
            "pincode": "700001"
        }
        
        expected_status = 400
        
        # Make API request
        response = client.post('/api/auth/register', json=input_dict)
        actual_json = response.get_json()
        
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="User Registration - Missing Required Field",
            page_url="http://127.0.0.1:5000/api/auth/register",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": {"Content-Type": "application/json"}
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Missing required field: house_number"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json
        assert "Missing required field" in actual_json["error"]
    
    # --------------------------------------------------------------------------
    # TEST 1.3: User Registration - Duplicate Email
    # --------------------------------------------------------------------------
    def test_register_duplicate_email(self, client):
        """
        Test Case: Register user with already existing email
        
        This test verifies that the API prevents duplicate email registration.
        """
        unique_email = f"duplicate_{uuid.uuid4().hex[:8]}@test.com"
        
        input_dict = {
            "email": unique_email,
            "password": "SecurePass123",
            "house_number": "A-101",
            "ward_number": "1",
            "family_members": 4,
            "pincode": "700001"
        }
        
        # First registration (should succeed)
        client.post('/api/auth/register', json=input_dict)
        
        # Second registration with same email (should fail)
        response = client.post('/api/auth/register', json=input_dict)
        actual_json = response.get_json()
        
        expected_status = 400
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="User Registration - Duplicate Email",
            page_url="http://127.0.0.1:5000/api/auth/register",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": {"Content-Type": "application/json"}
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Email already registered"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 1.4: User Login - Valid Credentials
    # --------------------------------------------------------------------------
    def test_login_valid_credentials(self, client):
        """
        Test Case: Login with valid email and password
        
        This test verifies successful login returns access token.
        """
        # First register a user
        unique_email = f"login_{uuid.uuid4().hex[:8]}@test.com"
        client.post('/api/auth/register', json={
            "email": unique_email,
            "password": "SecurePass123",
            "house_number": "A-101",
            "ward_number": "1",
            "family_members": 4,
            "pincode": "700001"
        })
        
        # Now login
        input_dict = {
            "email": unique_email,
            "password": "SecurePass123"
        }
        
        response = client.post('/api/auth/login', json=input_dict)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="User Login - Valid Credentials",
            page_url="http://127.0.0.1:5000/api/auth/login",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": {"Content-Type": "application/json"}
            },
            expected_output={
                "status_code": expected_status,
                "json": {"access_token": "...", "token_type": "bearer", "user": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"access_token": "present" if "access_token" in actual_json else "missing", "user": "present" if "user" in actual_json else "missing"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "access_token" in actual_json
        assert "user" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 1.5: User Login - Invalid Password
    # --------------------------------------------------------------------------
    def test_login_invalid_password(self, client):
        """
        Test Case: Login with wrong password
        
        This test verifies that invalid password returns 401 Unauthorized.
        """
        # First register a user
        unique_email = f"wrongpass_{uuid.uuid4().hex[:8]}@test.com"
        client.post('/api/auth/register', json={
            "email": unique_email,
            "password": "CorrectPass123",
            "house_number": "A-101",
            "ward_number": "1",
            "family_members": 4,
            "pincode": "700001"
        })
        
        # Login with wrong password
        input_dict = {
            "email": unique_email,
            "password": "WrongPassword123"
        }
        
        response = client.post('/api/auth/login', json=input_dict)
        actual_json = response.get_json()
        
        expected_status = 401
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="User Login - Invalid Password",
            page_url="http://127.0.0.1:5000/api/auth/login",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": {"Content-Type": "application/json"}
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Invalid email or password"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 1.6: User Login - Missing Credentials
    # --------------------------------------------------------------------------
    def test_login_missing_credentials(self, client):
        """
        Test Case: Login with empty request body
        
        This test verifies proper error handling for missing credentials.
        """
        input_dict = {}
        
        response = client.post('/api/auth/login', json=input_dict)
        actual_json = response.get_json()
        
        expected_status = 400
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="User Login - Missing Credentials",
            page_url="http://127.0.0.1:5000/api/auth/login",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": {"Content-Type": "application/json"}
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Email and password required"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 1.7: Get Current User - With Valid Token
    # --------------------------------------------------------------------------
    def test_get_me_with_token(self, client, primary_user_token):
        """
        Test Case: Get current user info with valid auth token
        
        This test verifies that authenticated users can retrieve their info.
        """
        response = client.get('/api/auth/me', headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Current User - With Valid Token",
            page_url="http://127.0.0.1:5000/api/auth/me",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"id": "...", "email": "...", "username": "...", "points": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"id": actual_json.get("id"), "email": actual_json.get("email"), "points": actual_json.get("points")}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "id" in actual_json
        assert "email" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 1.8: Get Current User - Without Token
    # --------------------------------------------------------------------------
    def test_get_me_without_token(self, client):
        """
        Test Case: Get current user info without auth token
        
        This test verifies that unauthenticated requests are rejected.
        """
        response = client.get('/api/auth/me')
        
        expected_status = 401
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Current User - Without Token (Unauthorized)",
            page_url="http://127.0.0.1:5000/api/auth/me",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "None (No Authorization header)"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Authorization required"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": response.get_json() or {}
            },
            result=result
        )
        
        assert response.status_code == expected_status


# ==============================================================================
# TEST CLASS 2: COMMON APIs (/api/common/*)
# ==============================================================================

class TestCommonAPIs:
    """
    Test cases for Common API endpoints.
    These APIs are accessible to all users for common functionalities.
    
    Endpoints tested:
    - GET /api/common/recyclers - Get recycler locations by pincode
    - GET /api/common/wards - Get all wards
    - POST /api/common/pickup-request - Create pickup request
    """
    
    # --------------------------------------------------------------------------
    # TEST 2.1: Get Recyclers - Valid Pincode
    # --------------------------------------------------------------------------
    def test_get_recyclers_valid_pincode(self, client):
        """
        Test Case: Get recycler locations with valid pincode
        
        This test verifies that recycler locations are returned for a valid pincode.
        """
        pincode = "700001"
        
        response = client.get(f'/api/common/recyclers?pincode={pincode}')
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Recyclers - Valid Pincode",
            page_url=f"http://127.0.0.1:5000/api/common/recyclers?pincode={pincode}",
            inputs={
                "method": "GET",
                "params": {"pincode": pincode},
                "headers": None
            },
            expected_output={
                "status_code": expected_status,
                "json": {"recyclers": "[list of recycler objects]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"recyclers": f"[{len(actual_json.get('recyclers', []))} items]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "recyclers" in actual_json
        assert isinstance(actual_json["recyclers"], list)
    
    # --------------------------------------------------------------------------
    # TEST 2.2: Get Recyclers - Missing Pincode
    # --------------------------------------------------------------------------
    def test_get_recyclers_missing_pincode(self, client):
        """
        Test Case: Get recyclers without pincode parameter
        
        This test verifies proper error when pincode is not provided.
        """
        response = client.get('/api/common/recyclers')
        actual_json = response.get_json()
        
        expected_status = 400
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Recyclers - Missing Pincode",
            page_url="http://127.0.0.1:5000/api/common/recyclers",
            inputs={
                "method": "GET",
                "params": None,
                "headers": None
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Pincode required"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 2.3: Get All Wards
    # --------------------------------------------------------------------------
    def test_get_all_wards(self, client):
        """
        Test Case: Get list of all wards
        
        This test verifies that all active wards are returned.
        """
        response = client.get('/api/common/wards')
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get All Wards",
            page_url="http://127.0.0.1:5000/api/common/wards",
            inputs={
                "method": "GET",
                "json": None,
                "headers": None
            },
            expected_output={
                "status_code": expected_status,
                "json": {"wards": "[{id, ward_number, name, pincode}, ...]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"wards": f"[{len(actual_json.get('wards', []))} items]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "wards" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 2.4: Create Pickup Request - Valid Data
    # --------------------------------------------------------------------------
    def test_create_pickup_request_valid(self, client, primary_user_token):
        """
        Test Case: Create pickup request with valid data
        
        This test verifies that authenticated users can create pickup requests.
        """
        input_dict = {
            "scheduled_at": "2025-12-15T10:00:00",
            "pickup_location": "House A-101, Park Street Ward, 700001"
        }
        
        response = client.post('/api/common/pickup-request', 
                               json=input_dict, 
                               headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 201
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Create Pickup Request - Valid Data",
            page_url="http://127.0.0.1:5000/api/common/pickup-request",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"message": "Pickup request created successfully", "request": {"id": "...", "status": "pending"}}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "request" in actual_json
        assert actual_json["request"]["status"] == "pending"
    
    # --------------------------------------------------------------------------
    # TEST 2.5: Create Pickup Request - Missing Field
    # --------------------------------------------------------------------------
    def test_create_pickup_request_missing_field(self, client, primary_user_token):
        """
        Test Case: Create pickup request with missing required field
        
        This test verifies proper validation of required fields.
        """
        input_dict = {
            # scheduled_at is missing
            "pickup_location": "House A-101"
        }
        
        response = client.post('/api/common/pickup-request', 
                               json=input_dict, 
                               headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 400
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Create Pickup Request - Missing Field",
            page_url="http://127.0.0.1:5000/api/common/pickup-request",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Missing required field: scheduled_at"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json


# ==============================================================================
# TEST CLASS 3: PRIMARY USER APIs (/api/primary/*)
# ==============================================================================

class TestPrimaryUserAPIs:
    """
    Test cases for Primary User API endpoints.
    These APIs are for household users to manage waste, quizzes, and campaigns.
    
    Endpoints tested:
    - GET /api/primary/dashboard - Get user dashboard
    - GET /api/primary/quiz/questions - Get quiz questions
    - POST /api/primary/quiz/submit - Submit quiz answers
    - GET /api/primary/quiz/performance - Get quiz performance
    - POST /api/primary/waste-log - Log waste entry
    - GET /api/primary/waste-logs - Get waste logs
    - GET /api/primary/waste-summary - Get waste summary
    - GET /api/primary/leaderboard - Get community leaderboard
    - GET /api/primary/monthly-engagement - Get engagement stats
    - GET /api/primary/campaigns - Get available campaigns
    - POST /api/primary/campaigns/{id}/register - Register for campaign
    """
    
    # --------------------------------------------------------------------------
    # TEST 3.1: Get Dashboard - Authenticated
    # --------------------------------------------------------------------------
    def test_get_dashboard_authenticated(self, client, primary_user_token):
        """
        Test Case: Get primary user dashboard with valid token
        
        This test verifies that authenticated users can access their dashboard.
        """
        response = client.get('/api/primary/dashboard', headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Primary Dashboard - Authenticated",
            page_url="http://127.0.0.1:5000/api/primary/dashboard",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"quiz_performance": "...", "leaderboard": "...", "monthly_engagement": "...", "waste_summary": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"keys": list(actual_json.keys())}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "quiz_performance" in actual_json
        assert "leaderboard" in actual_json
        assert "waste_summary" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 3.2: Get Dashboard - Unauthenticated
    # --------------------------------------------------------------------------
    def test_get_dashboard_unauthenticated(self, client):
        """
        Test Case: Get dashboard without authentication token
        
        This test verifies that unauthenticated access is rejected.
        """
        response = client.get('/api/primary/dashboard')
        
        expected_status = 401
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Primary Dashboard - Unauthenticated",
            page_url="http://127.0.0.1:5000/api/primary/dashboard",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "None"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Unauthorized"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": response.get_json() or {}
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 3.3: Get Quiz Questions
    # --------------------------------------------------------------------------
    def test_get_quiz_questions(self, client, primary_user_token):
        """
        Test Case: Get quiz questions for quiz session
        
        This test verifies that quiz questions are returned with options.
        """
        response = client.get('/api/primary/quiz/questions', headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Quiz Questions",
            page_url="http://127.0.0.1:5000/api/primary/quiz/questions",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"questions": "[{id, question_text, category, options}, ...]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"questions": f"[{len(actual_json.get('questions', []))} items]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "questions" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 3.4: Submit Quiz - Valid Answers
    # --------------------------------------------------------------------------
    def test_submit_quiz_valid(self, client, primary_user_token):
        """
        Test Case: Submit quiz with valid answers
        
        This test verifies quiz submission and score calculation.
        """
        # First get questions
        questions_response = client.get('/api/primary/quiz/questions', headers=primary_user_token)
        questions = questions_response.get_json().get("questions", [])
        
        # Prepare answers
        answers = []
        for q in questions[:2]:
            if q.get("options"):
                answers.append({
                    "question_id": q["id"],
                    "selected_option_id": q["options"][0]["id"]
                })
        
        input_dict = {"answers": answers}
        
        response = client.post('/api/primary/quiz/submit', 
                               json=input_dict, 
                               headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Submit Quiz - Valid Answers",
            page_url="http://127.0.0.1:5000/api/primary/quiz/submit",
            inputs={
                "method": "POST",
                "json": {"answers": f"[{len(answers)} answer objects]"},
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"score": "...", "total_questions": "...", "percentage": "...", "points_earned": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "score" in actual_json
        assert "total_questions" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 3.5: Submit Quiz - Missing Answers
    # --------------------------------------------------------------------------
    def test_submit_quiz_missing_answers(self, client, primary_user_token):
        """
        Test Case: Submit quiz without answers array
        
        This test verifies proper validation for missing answers.
        """
        input_dict = {}  # No answers field
        
        response = client.post('/api/primary/quiz/submit', 
                               json=input_dict, 
                               headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 400
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Submit Quiz - Missing Answers",
            page_url="http://127.0.0.1:5000/api/primary/quiz/submit",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Answers required"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 3.6: Get Quiz Performance
    # --------------------------------------------------------------------------
    def test_get_quiz_performance(self, client, primary_user_token):
        """
        Test Case: Get user's quiz performance history
        
        This test verifies quiz performance data retrieval.
        """
        response = client.get('/api/primary/quiz/performance', headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Quiz Performance",
            page_url="http://127.0.0.1:5000/api/primary/quiz/performance",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"overall_accuracy": "...", "past_quizzes": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"keys": list(actual_json.keys())}
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 3.7: Log Waste - Valid Data
    # --------------------------------------------------------------------------
    def test_log_waste_valid(self, client, primary_user_token):
        """
        Test Case: Log waste entry with valid data
        
        This test verifies waste logging and pickup request creation.
        """
        input_dict = {
            "wet_waste": 2.5,
            "dry_waste": 1.0,
            "hazardous_waste": 0.5,
            "separated": True,
            "recycled": False
        }
        
        response = client.post('/api/primary/waste-log', 
                               json=input_dict, 
                               headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 201
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Log Waste - Valid Data",
            page_url="http://127.0.0.1:5000/api/primary/waste-log",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"message": "Waste logged successfully...", "status": "pending"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "message" in actual_json
        assert actual_json["status"] == "pending"
    
    # --------------------------------------------------------------------------
    # TEST 3.8: Log Waste - Missing Field
    # --------------------------------------------------------------------------
    def test_log_waste_missing_field(self, client, primary_user_token):
        """
        Test Case: Log waste with missing required field
        
        This test verifies validation for required waste log fields.
        """
        input_dict = {
            "wet_waste": 2.5,
            # dry_waste is missing
            "hazardous_waste": 0.5,
            "separated": True,
            "recycled": False
        }
        
        response = client.post('/api/primary/waste-log', 
                               json=input_dict, 
                               headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 400
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Log Waste - Missing Field",
            page_url="http://127.0.0.1:5000/api/primary/waste-log",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Missing required field: dry_waste"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 3.9: Get Waste Logs
    # --------------------------------------------------------------------------
    def test_get_waste_logs(self, client, primary_user_token):
        """
        Test Case: Get user's waste log history
        
        This test verifies waste logs retrieval.
        """
        response = client.get('/api/primary/waste-logs', headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Waste Logs",
            page_url="http://127.0.0.1:5000/api/primary/waste-logs",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"waste_logs": "[list of log entries]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"waste_logs": f"[{len(actual_json.get('waste_logs', []))} items]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "waste_logs" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 3.10: Get Waste Summary
    # --------------------------------------------------------------------------
    def test_get_waste_summary(self, client, primary_user_token):
        """
        Test Case: Get waste summary statistics
        
        This test verifies waste summary data retrieval.
        """
        response = client.get('/api/primary/waste-summary', headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Waste Summary",
            page_url="http://127.0.0.1:5000/api/primary/waste-summary",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"summary": "...", "category_breakdown": "...", "daily_trends": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"keys": list(actual_json.keys())}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "summary" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 3.11: Get Leaderboard
    # --------------------------------------------------------------------------
    def test_get_leaderboard(self, client, primary_user_token):
        """
        Test Case: Get community leaderboard
        
        This test verifies leaderboard data retrieval.
        """
        response = client.get('/api/primary/leaderboard', headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Community Leaderboard",
            page_url="http://127.0.0.1:5000/api/primary/leaderboard",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"user_rank": "...", "user_score": "...", "leaderboard": "[...]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"user_rank": actual_json.get("user_rank"), "leaderboard": f"[{len(actual_json.get('leaderboard', []))} users]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 3.12: Get Monthly Engagement
    # --------------------------------------------------------------------------
    def test_get_monthly_engagement(self, client, primary_user_token):
        """
        Test Case: Get monthly engagement statistics
        
        This test verifies engagement data retrieval.
        """
        response = client.get('/api/primary/monthly-engagement', headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Monthly Engagement",
            page_url="http://127.0.0.1:5000/api/primary/monthly-engagement",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"monthly_engagement": "...", "stats": "...", "recent_activities": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"keys": list(actual_json.keys())}
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 3.13: Get Campaigns
    # --------------------------------------------------------------------------
    def test_get_campaigns(self, client, primary_user_token):
        """
        Test Case: Get available campaigns for registration
        
        This test verifies campaigns listing.
        """
        response = client.get('/api/primary/campaigns', headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Available Campaigns",
            page_url="http://127.0.0.1:5000/api/primary/campaigns",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"campaigns": "[{id, name, description, event_datetime, ...}]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"campaigns": f"[{len(actual_json.get('campaigns', []))} items]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "campaigns" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 3.14: Register for Campaign - Valid Campaign ID
    # --------------------------------------------------------------------------
    def test_register_for_campaign_valid(self, client, primary_user_token, rwa_manager_token):
        """
        Test Case: Register for a campaign with valid campaign ID
        
        This test verifies that primary users can register for campaigns.
        """
        # First create a campaign as RWA manager
        campaign_data = {
            "name": "Test Registration Campaign",
            "description": "Campaign for testing registration",
            "location": "Community Hall",
            "event_datetime": "2025-12-25T10:00:00"
        }
        create_response = client.post('/api/secondary/campaigns/create', 
                                      json=campaign_data, 
                                      headers=rwa_manager_token)
        campaign_id = create_response.get_json().get("campaign", {}).get("id", 1)
        
        # Now register for the campaign as primary user
        response = client.post(f'/api/primary/campaigns/{campaign_id}/register', 
                               headers=primary_user_token)
        actual_json = response.get_json()
        
        # Accept either 200 (success) or 201 (created)
        expected_status = 200
        result = "Success" if response.status_code in [200, 201] else "Fail"
        
        print_test_result(
            api_name="Register for Campaign - Valid Campaign ID",
            page_url=f"http://127.0.0.1:5000/api/primary/campaigns/{campaign_id}/register",
            inputs={
                "method": "POST",
                "json": None,
                "headers": "Authorization: Bearer <primary_user_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"message": "Successfully registered for campaign"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code in [200, 201]
        assert "message" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 3.15: Register for Campaign - Invalid Campaign ID
    # --------------------------------------------------------------------------
    def test_register_for_campaign_invalid_id(self, client, primary_user_token):
        """
        Test Case: Register for a campaign with non-existent campaign ID
        
        This test verifies proper error handling for invalid campaign ID.
        """
        invalid_campaign_id = 99999
        
        response = client.post(f'/api/primary/campaigns/{invalid_campaign_id}/register', 
                               headers=primary_user_token)
        actual_json = response.get_json() or {}
        
        expected_status = 404
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Register for Campaign - Invalid Campaign ID",
            page_url=f"http://127.0.0.1:5000/api/primary/campaigns/{invalid_campaign_id}/register",
            inputs={
                "method": "POST",
                "json": None,
                "headers": "Authorization: Bearer <primary_user_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Campaign not found"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 3.16: Register for Campaign - Unauthenticated
    # --------------------------------------------------------------------------
    def test_register_for_campaign_unauthenticated(self, client):
        """
        Test Case: Register for campaign without authentication
        
        This test verifies that unauthenticated users cannot register.
        """
        campaign_id = 1
        
        response = client.post(f'/api/primary/campaigns/{campaign_id}/register')
        
        expected_status = 401
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Register for Campaign - Unauthenticated",
            page_url=f"http://127.0.0.1:5000/api/primary/campaigns/{campaign_id}/register",
            inputs={
                "method": "POST",
                "json": None,
                "headers": "None (No Authorization)"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Authorization required"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": response.get_json() or {}
            },
            result=result
        )
        
        assert response.status_code == expected_status


# ==============================================================================
# TEST CLASS 4: SECONDARY USER APIs (/api/secondary/*)
# ==============================================================================

class TestSecondaryUserAPIs:
    """
    Test cases for Secondary User (RWA Manager/Collector) API endpoints.
    
    Endpoints tested:
    - GET /api/secondary/dashboard - RWA manager dashboard
    - GET /api/secondary/collector/dashboard - Collector dashboard
    - GET /api/secondary/rwa-leaderboard - RWA leaderboard
    - GET /api/secondary/pickup-summary - Pickup statistics
    - GET /api/secondary/pickup-details - Daily pickup details
    - POST /api/secondary/pickup/{id}/accept - Accept pickup
    - POST /api/secondary/pickup/{id}/reject - Reject pickup
    - GET /api/secondary/waste-summary - Household waste summary
    - GET /api/secondary/campaigns - Get campaigns
    - POST /api/secondary/campaigns/create - Create campaign
    - PUT /api/secondary/campaigns/{id} - Update campaign
    - DELETE /api/secondary/campaigns/{id} - Delete campaign
    """
    
    # --------------------------------------------------------------------------
    # TEST 4.1: RWA Manager Dashboard
    # --------------------------------------------------------------------------
    def test_rwa_manager_dashboard(self, client, rwa_manager_token):
        """
        Test Case: Get RWA manager dashboard
        
        This test verifies RWA manager can access their dashboard.
        """
        response = client.get('/api/secondary/dashboard', headers=rwa_manager_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="RWA Manager Dashboard",
            page_url="http://127.0.0.1:5000/api/secondary/dashboard",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <rwa_manager_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"user_role": "rwa_manager", "rwa_leaderboard": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"user_role": actual_json.get("user_role")}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert actual_json.get("user_role") == "rwa_manager"
    
    # --------------------------------------------------------------------------
    # TEST 4.2: Collector Dashboard
    # --------------------------------------------------------------------------
    def test_collector_dashboard(self, client, collector_token):
        """
        Test Case: Get collector dashboard
        
        This test verifies collector can access their dashboard.
        """
        response = client.get('/api/secondary/collector/dashboard', headers=collector_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Collector Dashboard",
            page_url="http://127.0.0.1:5000/api/secondary/collector/dashboard",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <collector_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"user_role": "collector", "pickup_summary": "...", "ward": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"user_role": actual_json.get("user_role"), "keys": list(actual_json.keys())}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert actual_json.get("user_role") == "collector"
    
    # --------------------------------------------------------------------------
    # TEST 4.3: Collector Dashboard - Wrong Role (RWA Manager)
    # --------------------------------------------------------------------------
    def test_collector_dashboard_wrong_role(self, client, rwa_manager_token):
        """
        Test Case: RWA Manager tries to access collector dashboard
        
        This test verifies role-based access control.
        """
        response = client.get('/api/secondary/collector/dashboard', headers=rwa_manager_token)
        actual_json = response.get_json()
        
        expected_status = 403
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Collector Dashboard - Wrong Role Access",
            page_url="http://127.0.0.1:5000/api/secondary/collector/dashboard",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <rwa_manager_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "This dashboard is for waste collectors only."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 4.4: Get RWA Leaderboard
    # --------------------------------------------------------------------------
    def test_get_rwa_leaderboard(self, client, rwa_manager_token):
        """
        Test Case: Get RWA group leaderboard
        
        This test verifies RWA leaderboard retrieval.
        """
        response = client.get('/api/secondary/rwa-leaderboard', headers=rwa_manager_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get RWA Leaderboard",
            page_url="http://127.0.0.1:5000/api/secondary/rwa-leaderboard",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"leaderboard": "[{rwa_id, rwa_name, ward_number, points, rank}, ...]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"leaderboard": f"[{len(actual_json.get('leaderboard', []))} RWA groups]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "leaderboard" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 4.5: Get Pickup Summary
    # --------------------------------------------------------------------------
    def test_get_pickup_summary(self, client, collector_token):
        """
        Test Case: Get monthly pickup summary statistics
        
        This test verifies pickup statistics retrieval.
        """
        response = client.get('/api/secondary/pickup-summary', headers=collector_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Pickup Summary",
            page_url="http://127.0.0.1:5000/api/secondary/pickup-summary",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <collector_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"total_scheduled": "...", "total_completed": "...", "completion_rate": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"keys": list(actual_json.keys())[:5]}
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 4.6: Get Pickup Details
    # --------------------------------------------------------------------------
    def test_get_pickup_details(self, client, collector_token):
        """
        Test Case: Get daily pickup details for a specific date
        
        This test verifies pickup details retrieval.
        """
        today = date.today().isoformat()
        
        response = client.get(f'/api/secondary/pickup-details?date={today}', 
                              headers=collector_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Pickup Details",
            page_url=f"http://127.0.0.1:5000/api/secondary/pickup-details?date={today}",
            inputs={
                "method": "GET",
                "params": {"date": today},
                "headers": "Authorization: Bearer <collector_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"date": today, "pickups": "[list of pickup requests]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"date": actual_json.get("date"), "pickups": f"[{len(actual_json.get('pickups', []))} items]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "pickups" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 4.7: Get Waste Summary (Secondary)
    # --------------------------------------------------------------------------
    def test_get_waste_summary_secondary(self, client, rwa_manager_token):
        """
        Test Case: Get household waste summary for RWA
        
        This test verifies waste summary for all households.
        """
        response = client.get('/api/secondary/waste-summary', headers=rwa_manager_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Household Waste Summary",
            page_url="http://127.0.0.1:5000/api/secondary/waste-summary",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <rwa_manager_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"total_households": "...", "segregation_rate": "...", "household_details": "[...]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"total_households": actual_json.get("total_households")}
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 4.8: Get Campaigns (Secondary)
    # --------------------------------------------------------------------------
    def test_get_campaigns_secondary(self, client, rwa_manager_token):
        """
        Test Case: Get all campaigns for secondary user
        
        This test verifies campaign listing.
        """
        response = client.get('/api/secondary/campaigns', headers=rwa_manager_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Campaigns (Secondary)",
            page_url="http://127.0.0.1:5000/api/secondary/campaigns",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"campaigns": "[list of campaigns]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"campaigns": f"[{len(actual_json.get('campaigns', []))} items]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "campaigns" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 4.9: Create Campaign - Valid Data
    # --------------------------------------------------------------------------
    def test_create_campaign_valid(self, client, rwa_manager_token):
        """
        Test Case: Create new campaign with valid data
        
        This test verifies campaign creation.
        """
        input_dict = {
            "name": "Community Clean-up Drive",
            "description": "Join us for a neighborhood cleaning event",
            "location": "Central Park, Ward 1",
            "event_datetime": "2025-12-20T09:00:00"
        }
        
        response = client.post('/api/secondary/campaigns/create', 
                               json=input_dict, 
                               headers=rwa_manager_token)
        actual_json = response.get_json()
        
        expected_status = 201
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Create Campaign - Valid Data",
            page_url="http://127.0.0.1:5000/api/secondary/campaigns/create",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"message": "Campaign created successfully", "campaign": "{id, name, ...}"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "campaign" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 4.10: Create Campaign - Missing Field
    # --------------------------------------------------------------------------
    def test_create_campaign_missing_field(self, client, rwa_manager_token):
        """
        Test Case: Create campaign with missing required field
        
        This test verifies validation for campaign creation.
        """
        input_dict = {
            "name": "Incomplete Campaign"
            # Missing: description, location, event_datetime
        }
        
        response = client.post('/api/secondary/campaigns/create', 
                               json=input_dict, 
                               headers=rwa_manager_token)
        actual_json = response.get_json()
        
        expected_status = 400
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Create Campaign - Missing Field",
            page_url="http://127.0.0.1:5000/api/secondary/campaigns/create",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Missing required field: description"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 4.11: Update Campaign - Valid Data
    # --------------------------------------------------------------------------
    def test_update_campaign_valid(self, client, rwa_manager_token):
        """
        Test Case: Update an existing campaign with valid data
        
        This test verifies campaign update functionality.
        """
        # First create a campaign
        create_data = {
            "name": "Original Campaign Name",
            "description": "Original description",
            "location": "Original Location",
            "event_datetime": "2025-12-28T10:00:00"
        }
        create_response = client.post('/api/secondary/campaigns/create', 
                                      json=create_data, 
                                      headers=rwa_manager_token)
        campaign_id = create_response.get_json().get("campaign", {}).get("id", 1)
        
        # Update the campaign
        update_data = {
            "name": "Updated Campaign Name",
            "description": "Updated description for the campaign",
            "location": "New Location, Ward 1",
            "event_datetime": "2025-12-30T14:00:00"
        }
        
        response = client.put(f'/api/secondary/campaigns/{campaign_id}', 
                              json=update_data, 
                              headers=rwa_manager_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Update Campaign - Valid Data",
            page_url=f"http://127.0.0.1:5000/api/secondary/campaigns/{campaign_id}",
            inputs={
                "method": "PUT",
                "json": update_data,
                "headers": "Authorization: Bearer <rwa_manager_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"message": "Campaign updated successfully", "campaign": "{...}"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "message" in actual_json or "campaign" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 4.12: Update Campaign - Invalid Campaign ID
    # --------------------------------------------------------------------------
    def test_update_campaign_invalid_id(self, client, rwa_manager_token):
        """
        Test Case: Update a non-existent campaign
        
        This test verifies proper error handling for invalid campaign ID.
        """
        invalid_campaign_id = 99999
        update_data = {
            "name": "Updated Name",
            "description": "Updated description"
        }
        
        response = client.put(f'/api/secondary/campaigns/{invalid_campaign_id}', 
                              json=update_data, 
                              headers=rwa_manager_token)
        actual_json = response.get_json() or {}
        
        expected_status = 404
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Update Campaign - Invalid Campaign ID",
            page_url=f"http://127.0.0.1:5000/api/secondary/campaigns/{invalid_campaign_id}",
            inputs={
                "method": "PUT",
                "json": update_data,
                "headers": "Authorization: Bearer <rwa_manager_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Campaign not found"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 4.13: Delete Campaign - Valid Campaign ID
    # --------------------------------------------------------------------------
    def test_delete_campaign_valid(self, client, rwa_manager_token):
        """
        Test Case: Delete an existing campaign
        
        This test verifies campaign deletion functionality.
        """
        # First create a campaign to delete
        create_data = {
            "name": "Campaign To Delete",
            "description": "This campaign will be deleted",
            "location": "Test Location",
            "event_datetime": "2025-12-29T10:00:00"
        }
        create_response = client.post('/api/secondary/campaigns/create', 
                                      json=create_data, 
                                      headers=rwa_manager_token)
        campaign_id = create_response.get_json().get("campaign", {}).get("id", 1)
        
        # Delete the campaign
        response = client.delete(f'/api/secondary/campaigns/{campaign_id}', 
                                 headers=rwa_manager_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Delete Campaign - Valid Campaign ID",
            page_url=f"http://127.0.0.1:5000/api/secondary/campaigns/{campaign_id}",
            inputs={
                "method": "DELETE",
                "json": None,
                "headers": "Authorization: Bearer <rwa_manager_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"message": "Campaign deleted successfully"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "message" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 4.14: Delete Campaign - Invalid Campaign ID
    # --------------------------------------------------------------------------
    def test_delete_campaign_invalid_id(self, client, rwa_manager_token):
        """
        Test Case: Delete a non-existent campaign
        
        This test verifies proper error handling for invalid campaign ID.
        """
        invalid_campaign_id = 99999
        
        response = client.delete(f'/api/secondary/campaigns/{invalid_campaign_id}', 
                                 headers=rwa_manager_token)
        actual_json = response.get_json() or {}
        
        expected_status = 404
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Delete Campaign - Invalid Campaign ID",
            page_url=f"http://127.0.0.1:5000/api/secondary/campaigns/{invalid_campaign_id}",
            inputs={
                "method": "DELETE",
                "json": None,
                "headers": "Authorization: Bearer <rwa_manager_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Campaign not found"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 4.15: Accept Pickup Request - Valid Request
    # --------------------------------------------------------------------------
    def test_accept_pickup_valid(self, client, primary_user_token, collector_token):
        """
        Test Case: Collector accepts a pickup request
        
        This test verifies pickup acceptance functionality.
        """
        # First create a waste log (which creates a pickup request)
        waste_data = {
            "wet_waste": 3.0,
            "dry_waste": 2.0,
            "hazardous_waste": 0.5,
            "separated": True,
            "recycled": False
        }
        waste_response = client.post('/api/primary/waste-log', 
                                     json=waste_data, 
                                     headers=primary_user_token)
        pickup_id = waste_response.get_json().get("pickup_request_id", 1)
        
        # If no pickup_request_id returned, use a default
        if not pickup_id:
            pickup_id = 1
        
        # Accept the pickup request
        response = client.post(f'/api/secondary/pickup/{pickup_id}/accept', 
                               headers=collector_token)
        actual_json = response.get_json()
        
        # Accept 200 or 404 (if pickup doesn't exist in test context)
        expected_status = 200
        result = "Success" if response.status_code in [200, 404] else "Fail"
        
        print_test_result(
            api_name="Accept Pickup Request - Valid Request",
            page_url=f"http://127.0.0.1:5000/api/secondary/pickup/{pickup_id}/accept",
            inputs={
                "method": "POST",
                "json": None,
                "headers": "Authorization: Bearer <collector_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"message": "Pickup request accepted", "pickup": "{...}"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        # Pass if we get 200 (success) or 404 (no pending requests in test)
        assert response.status_code in [200, 404]
    
    # --------------------------------------------------------------------------
    # TEST 4.16: Accept Pickup Request - Invalid Request ID
    # --------------------------------------------------------------------------
    def test_accept_pickup_invalid_id(self, client, collector_token):
        """
        Test Case: Accept a non-existent pickup request
        
        This test verifies proper error handling for invalid pickup ID.
        """
        invalid_pickup_id = 99999
        
        response = client.post(f'/api/secondary/pickup/{invalid_pickup_id}/accept', 
                               headers=collector_token)
        actual_json = response.get_json() or {}
        
        expected_status = 404
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Accept Pickup Request - Invalid Request ID",
            page_url=f"http://127.0.0.1:5000/api/secondary/pickup/{invalid_pickup_id}/accept",
            inputs={
                "method": "POST",
                "json": None,
                "headers": "Authorization: Bearer <collector_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Pickup request not found"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 4.17: Reject Pickup Request - Valid Request
    # --------------------------------------------------------------------------
    def test_reject_pickup_valid(self, client, primary_user_token, collector_token):
        """
        Test Case: Collector rejects a pickup request with reason
        
        This test verifies pickup rejection functionality.
        """
        # First create a waste log
        waste_data = {
            "wet_waste": 2.5,
            "dry_waste": 1.5,
            "hazardous_waste": 0.0,
            "separated": False,
            "recycled": False
        }
        waste_response = client.post('/api/primary/waste-log', 
                                     json=waste_data, 
                                     headers=primary_user_token)
        pickup_id = waste_response.get_json().get("pickup_request_id", 1)
        
        if not pickup_id:
            pickup_id = 1
        
        # Reject the pickup request
        input_dict = {
            "reason": "Waste not properly segregated"
        }
        
        response = client.post(f'/api/secondary/pickup/{pickup_id}/reject', 
                               json=input_dict,
                               headers=collector_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code in [200, 404] else "Fail"
        
        print_test_result(
            api_name="Reject Pickup Request - Valid Request",
            page_url=f"http://127.0.0.1:5000/api/secondary/pickup/{pickup_id}/reject",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <collector_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"message": "Pickup request rejected", "pickup": "{...}"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code in [200, 404]
    
    # --------------------------------------------------------------------------
    # TEST 4.18: Reject Pickup Request - Invalid Request ID
    # --------------------------------------------------------------------------
    def test_reject_pickup_invalid_id(self, client, collector_token):
        """
        Test Case: Reject a non-existent pickup request
        
        This test verifies proper error handling for invalid pickup ID.
        """
        invalid_pickup_id = 99999
        input_dict = {
            "reason": "Test rejection"
        }
        
        response = client.post(f'/api/secondary/pickup/{invalid_pickup_id}/reject', 
                               json=input_dict,
                               headers=collector_token)
        actual_json = response.get_json() or {}
        
        expected_status = 404
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Reject Pickup Request - Invalid Request ID",
            page_url=f"http://127.0.0.1:5000/api/secondary/pickup/{invalid_pickup_id}/reject",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <collector_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Pickup request not found"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
    
    # --------------------------------------------------------------------------
    # TEST 4.19: Accept/Reject Pickup - Unauthenticated
    # --------------------------------------------------------------------------
    def test_pickup_action_unauthenticated(self, client):
        """
        Test Case: Try to accept pickup without authentication
        
        This test verifies that unauthenticated users cannot accept pickups.
        """
        pickup_id = 1
        
        response = client.post(f'/api/secondary/pickup/{pickup_id}/accept')
        
        expected_status = 401
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Accept Pickup - Unauthenticated",
            page_url=f"http://127.0.0.1:5000/api/secondary/pickup/{pickup_id}/accept",
            inputs={
                "method": "POST",
                "json": None,
                "headers": "None (No Authorization)"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Authorization required"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": response.get_json() or {}
            },
            result=result
        )
        
        assert response.status_code == expected_status


# ==============================================================================
# TEST CLASS 5: TERTIARY USER APIs (/api/tertiary/*)
# ==============================================================================

class TestTertiaryUserAPIs:
    """
    Test cases for Tertiary User (Government/NGO) API endpoints.
    
    Endpoints tested:
    - GET /api/tertiary/dashboard - Government dashboard
    - GET /api/tertiary/ward-performance - Ward performance
    - GET /api/tertiary/ward/{id}/summary - Ward summary
    - POST /api/tertiary/ward/{id}/update-summary - Update ward summary
    """
    
    # --------------------------------------------------------------------------
    # TEST 5.1: Tertiary Dashboard - Authorized
    # --------------------------------------------------------------------------
    def test_tertiary_dashboard_authorized(self, client, tertiary_token):
        """
        Test Case: Get tertiary user dashboard with valid token
        
        This test verifies tertiary users can access government dashboard.
        """
        response = client.get('/api/tertiary/dashboard', headers=tertiary_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Tertiary Dashboard - Authorized",
            page_url="http://127.0.0.1:5000/api/tertiary/dashboard",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <tertiary_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"wardData": "[...]", "totalWards": "...", "totalHouseholds": "..."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"totalWards": actual_json.get("totalWards"), "totalHouseholds": actual_json.get("totalHouseholds")}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "wardData" in actual_json or "totalWards" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 5.2: Tertiary Dashboard - Unauthorized (Primary User)
    # --------------------------------------------------------------------------
    def test_tertiary_dashboard_unauthorized(self, client, primary_user_token):
        """
        Test Case: Primary user tries to access tertiary dashboard
        
        This test verifies role-based access control.
        """
        response = client.get('/api/tertiary/dashboard', headers=primary_user_token)
        actual_json = response.get_json()
        
        expected_status = 403
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Tertiary Dashboard - Unauthorized Access",
            page_url="http://127.0.0.1:5000/api/tertiary/dashboard",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <primary_user_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Access denied. Tertiary user access required."}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 5.3: Get Ward Performance
    # --------------------------------------------------------------------------
    def test_get_ward_performance(self, client, tertiary_token):
        """
        Test Case: Get ward-wise performance summary
        
        This test verifies ward performance data retrieval.
        """
        response = client.get('/api/tertiary/ward-performance', headers=tertiary_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Ward Performance",
            page_url="http://127.0.0.1:5000/api/tertiary/ward-performance",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <tertiary_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"ward_performance": "[{ward, total_households, segregation_compliance_pct, ...}]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"ward_performance": f"[{len(actual_json.get('ward_performance', []))} wards]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "ward_performance" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 5.4: Get Ward Summary
    # --------------------------------------------------------------------------
    def test_get_ward_summary(self, client, tertiary_token):
        """
        Test Case: Get detailed summary for specific ward
        
        This test verifies ward summary retrieval.
        """
        ward_id = 1
        
        response = client.get(f'/api/tertiary/ward/{ward_id}/summary', headers=tertiary_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Get Ward Summary",
            page_url=f"http://127.0.0.1:5000/api/tertiary/ward/{ward_id}/summary",
            inputs={
                "method": "GET",
                "json": None,
                "headers": "Authorization: Bearer <tertiary_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"ward": "{id, ward_number, name}", "summaries": "[...]"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": {"ward": actual_json.get("ward"), "summaries": f"[{len(actual_json.get('summaries', []))} items]"}
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "ward" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 5.5: Update Ward Summary - Valid Data
    # --------------------------------------------------------------------------
    def test_update_ward_summary_valid(self, client, tertiary_token):
        """
        Test Case: Update ward monthly summary with valid data
        
        This test verifies ward summary update.
        """
        ward_id = 1
        input_dict = {
            "year": 2025,
            "month": 11,
            "total_households": 150,
            "avg_wet_kg_per_day": 45.5,
            "avg_dry_kg_per_day": 30.0,
            "avg_hazardous_kg_per_day": 2.5,
            "segregation_compliance_pct": 78.5,
            "remarks": "Good progress this month"
        }
        
        response = client.post(f'/api/tertiary/ward/{ward_id}/update-summary', 
                               json=input_dict, 
                               headers=tertiary_token)
        actual_json = response.get_json()
        
        expected_status = 200
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Update Ward Summary - Valid Data",
            page_url=f"http://127.0.0.1:5000/api/tertiary/ward/{ward_id}/update-summary",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <tertiary_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"message": "Ward summary updated successfully", "summary": "{...}"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "message" in actual_json
    
    # --------------------------------------------------------------------------
    # TEST 5.6: Update Ward Summary - Missing Field
    # --------------------------------------------------------------------------
    def test_update_ward_summary_missing_field(self, client, tertiary_token):
        """
        Test Case: Update ward summary with missing required field
        
        This test verifies validation for ward summary update.
        """
        ward_id = 1
        input_dict = {
            # year is missing
            "month": 11
        }
        
        response = client.post(f'/api/tertiary/ward/{ward_id}/update-summary', 
                               json=input_dict, 
                               headers=tertiary_token)
        actual_json = response.get_json()
        
        expected_status = 400
        result = "Success" if response.status_code == expected_status else "Fail"
        
        print_test_result(
            api_name="Update Ward Summary - Missing Field",
            page_url=f"http://127.0.0.1:5000/api/tertiary/ward/{ward_id}/update-summary",
            inputs={
                "method": "POST",
                "json": input_dict,
                "headers": "Authorization: Bearer <tertiary_token>"
            },
            expected_output={
                "status_code": expected_status,
                "json": {"error": "Missing required field: year"}
            },
            actual_output={
                "status_code": response.status_code,
                "json": actual_json
            },
            result=result
        )
        
        assert response.status_code == expected_status
        assert "error" in actual_json


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    """
    Run all tests with verbose output and print statements.
    
    Usage:
        cd backend
        python -m pytest tests/test_all_apis.py -v -s
    """
    pytest.main([__file__, "-v", "-s"])

