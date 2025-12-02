"""
================================================================================
API FAILURE TESTS - Tests Demonstrating Issues/Bugs in the APIs
================================================================================

These tests are designed to FAIL to demonstrate where the API behavior differs
from expected/best practices. Each failure represents a potential issue that
needs to be fixed.

Purpose: "Showcase any API where the actual and expected outputs differ.
          (This demonstrates how testing helps improve your API.)"

Format for each test:
- API BEING TESTED
- Inputs
- Expected Output
- Actual Output
- Result: Success/Fail

Note: These tests are EXPECTED TO FAIL because they test for missing validations
and security features that the current API does not implement.

================================================================================
"""
import pytest
import uuid
import json


# =============================================================================
# ISSUE CATEGORY 1: MISSING INPUT VALIDATION
# =============================================================================

class TestInputValidationFailures:
    """
    Test cases demonstrating missing or weak input validation.
    These tests FAIL because the API accepts invalid inputs that should be rejected.
    """

    # -------------------------------------------------------------------------
    # TEST 1: Empty Password Accepted (SECURITY ISSUE)
    # -------------------------------------------------------------------------
    def test_register_accepts_empty_password(self, client):
        """
        ================================================================================
        FAILURE TEST 1: Empty Password Validation Missing
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/auth/register
        Description: Test that API rejects empty password - currently it does NOT.
        Security Issue: Empty passwords allow unauthorized access.
        """
        # Generate unique email for this test
        test_email = f"emptypass_{uuid.uuid4().hex[:8]}@test.com"
        
        input_data = {
            "email": test_email,
            "password": "",  # EMPTY PASSWORD - Should be rejected
            "house_number": "101",
            "ward_number": "1",
            "family_members": 4,
            "pincode": "700001"
        }
        
        expected_status = 400  # Should reject with Bad Request
        expected_error = "Password cannot be empty"
        
        # Make API call
        response = client.post('/api/auth/register', json=input_data)
        actual_status = response.status_code
        actual_data = response.get_json()
        
        # Determine if this is a pass or fail
        is_validated = actual_status == 400
        result = "Success" if is_validated else "Fail"
        
        # Print formatted output
        print("\n" + "=" * 80)
        print("API BEING TESTED: User Registration - Empty Password Validation")
        print("=" * 80)
        print(f"Endpoint: POST /api/auth/register")
        print(f"Issue Type: SECURITY - Missing Input Validation")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST")
        print(f"    - JSON Body:")
        print(f"        email: {test_email}")
        print(f"        password: '' (EMPTY)")
        print(f"        house_number: '101'")
        print(f"        ward_number: '1'")
        print(f"        family_members: 4")
        print(f"        pincode: '700001'")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Bad Request)")
        print(f"    - JSON: {{'error': '{expected_error}'}}")
        print(f"    - Behavior: API should REJECT empty passwords")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_data, indent=8) if actual_data else 'None'}")
        print(f"    - Behavior: API {'REJECTS' if is_validated else 'ACCEPTS'} empty passwords")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Empty passwords are accepted - this is a SECURITY VULNERABILITY!")
            print("    RECOMMENDATION: Add password validation to reject empty passwords.")
        print("=" * 80)
        
        # Assert to make test fail if issue exists
        assert actual_status == expected_status, \
            f"API accepts empty password! Expected 400, got {actual_status}"

    # -------------------------------------------------------------------------
    # TEST 2: Short Password Accepted (SECURITY ISSUE)
    # -------------------------------------------------------------------------
    def test_register_accepts_short_password(self, client):
        """
        ================================================================================
        FAILURE TEST 2: Short Password Validation Missing
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/auth/register
        Description: Test that API enforces minimum password length - currently it does NOT.
        Security Issue: Short passwords are easily guessable/crackable.
        """
        test_email = f"shortpass_{uuid.uuid4().hex[:8]}@test.com"
        
        input_data = {
            "email": test_email,
            "password": "abc",  # ONLY 3 CHARACTERS - Should be rejected
            "house_number": "101",
            "ward_number": "1",
            "family_members": 4,
            "pincode": "700001"
        }
        
        expected_status = 400
        expected_error = "Password must be at least 8 characters"
        
        response = client.post('/api/auth/register', json=input_data)
        actual_status = response.status_code
        actual_data = response.get_json()
        
        is_validated = actual_status == 400
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: User Registration - Short Password Validation")
        print("=" * 80)
        print(f"Endpoint: POST /api/auth/register")
        print(f"Issue Type: SECURITY - Weak Password Policy")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST")
        print(f"    - JSON Body:")
        print(f"        email: {test_email}")
        print(f"        password: 'abc' (ONLY 3 CHARACTERS)")
        print(f"        house_number: '101'")
        print(f"        ward_number: '1'")
        print(f"        family_members: 4")
        print(f"        pincode: '700001'")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Bad Request)")
        print(f"    - JSON: {{'error': '{expected_error}'}}")
        print(f"    - Behavior: API should REJECT passwords shorter than 8 characters")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_data, indent=8) if actual_data else 'None'}")
        print(f"    - Behavior: API {'REJECTS' if is_validated else 'ACCEPTS'} 3-char password")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: 3-character passwords are accepted!")
            print("    RECOMMENDATION: Enforce minimum 8-character password policy.")
        print("=" * 80)
        
        assert actual_status == expected_status, \
            f"API accepts 3-char password! Expected 400, got {actual_status}"

    # -------------------------------------------------------------------------
    # TEST 3: Invalid Email Format Accepted
    # -------------------------------------------------------------------------
    def test_register_accepts_invalid_email_format(self, client):
        """
        ================================================================================
        FAILURE TEST 3: Invalid Email Format Validation Missing
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/auth/register
        Description: Test that API validates email format - currently it does NOT.
        Issue: Invalid emails prevent user communication.
        """
        input_data = {
            "email": "not-an-email",  # INVALID EMAIL FORMAT
            "password": "TestPass123",
            "house_number": "101",
            "ward_number": "1",
            "family_members": 4,
            "pincode": "700001"
        }
        
        expected_status = 400
        expected_error = "Invalid email format"
        
        response = client.post('/api/auth/register', json=input_data)
        actual_status = response.status_code
        actual_data = response.get_json()
        
        is_validated = actual_status == 400
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: User Registration - Email Format Validation")
        print("=" * 80)
        print(f"Endpoint: POST /api/auth/register")
        print(f"Issue Type: DATA QUALITY - Missing Format Validation")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST")
        print(f"    - JSON Body:")
        print(f"        email: 'not-an-email' (INVALID FORMAT - no @ symbol)")
        print(f"        password: 'TestPass123'")
        print(f"        house_number: '101'")
        print(f"        ward_number: '1'")
        print(f"        family_members: 4")
        print(f"        pincode: '700001'")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Bad Request)")
        print(f"    - JSON: {{'error': '{expected_error}'}}")
        print(f"    - Behavior: API should REJECT invalid email formats")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_data, indent=8) if actual_data else 'None'}")
        print(f"    - Behavior: API {'REJECTS' if is_validated else 'ACCEPTS'} 'not-an-email'")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Invalid email 'not-an-email' is accepted!")
            print("    RECOMMENDATION: Add email format validation using regex.")
        print("=" * 80)
        
        assert actual_status == expected_status, \
            f"API accepts invalid email! Expected 400, got {actual_status}"

    # -------------------------------------------------------------------------
    # TEST 4: Negative Waste Values Accepted
    # -------------------------------------------------------------------------
    def test_waste_log_accepts_negative_values(self, client, primary_user_token):
        """
        ================================================================================
        FAILURE TEST 4: Negative Waste Values Not Rejected
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/primary/waste-log
        Description: Test that API rejects negative waste quantities - currently it does NOT.
        Issue: Negative waste values are logically impossible and corrupt data.
        """
        input_data = {
            "wet_waste": -5.0,  # NEGATIVE VALUE - Should be rejected
            "dry_waste": 1.0,
            "hazardous_waste": 0.5,
            "separated": True,
            "recycled": False
        }
        
        expected_status = 400
        expected_error = "Waste quantity cannot be negative"
        
        response = client.post('/api/primary/waste-log', 
                               json=input_data, headers=primary_user_token)
        actual_status = response.status_code
        actual_data = response.get_json()
        
        is_validated = actual_status == 400
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: Waste Log - Negative Value Validation")
        print("=" * 80)
        print(f"Endpoint: POST /api/primary/waste-log")
        print(f"Issue Type: DATA INTEGRITY - Missing Range Validation")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST")
        print(f"    - Authorization: Bearer <primary_user_token>")
        print(f"    - JSON Body:")
        print(f"        wet_waste: -5.0 (NEGATIVE VALUE)")
        print(f"        dry_waste: 1.0")
        print(f"        hazardous_waste: 0.5")
        print(f"        separated: true")
        print(f"        recycled: false")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Bad Request)")
        print(f"    - JSON: {{'error': '{expected_error}'}}")
        print(f"    - Behavior: API should REJECT negative waste quantities")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_data, indent=8) if actual_data else 'None'}")
        print(f"    - Behavior: API {'REJECTS' if is_validated else 'ACCEPTS'} negative waste (-5.0 kg)")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Negative waste quantity (-5.0 kg) is accepted!")
            print("    RECOMMENDATION: Add validation to ensure waste >= 0.")
        print("=" * 80)
        
        assert actual_status == expected_status, \
            f"API accepts negative waste! Expected 400, got {actual_status}"

    # -------------------------------------------------------------------------
    # TEST 5: Invalid Pincode Format Accepted
    # -------------------------------------------------------------------------
    def test_pincode_accepts_invalid_format(self, client):
        """
        ================================================================================
        FAILURE TEST 5: Invalid Pincode Format Not Validated
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/auth/register
        Description: Test that API validates pincode format (6 digits) - currently it does NOT.
        Issue: Invalid pincodes affect delivery and location services.
        """
        test_email = f"badpin_{uuid.uuid4().hex[:8]}@test.com"
        
        input_data = {
            "email": test_email,
            "password": "TestPass123",
            "house_number": "101",
            "ward_number": "1",
            "family_members": 4,
            "pincode": "12345"  # ONLY 5 DIGITS - Indian pincodes are 6 digits
        }
        
        expected_status = 400
        expected_error = "Invalid pincode format (must be 6 digits)"
        
        response = client.post('/api/auth/register', json=input_data)
        actual_status = response.status_code
        actual_data = response.get_json()
        
        is_validated = actual_status == 400
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: User Registration - Pincode Format Validation")
        print("=" * 80)
        print(f"Endpoint: POST /api/auth/register")
        print(f"Issue Type: DATA QUALITY - Missing Format Validation")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST")
        print(f"    - JSON Body:")
        print(f"        email: {test_email}")
        print(f"        password: 'TestPass123'")
        print(f"        house_number: '101'")
        print(f"        ward_number: '1'")
        print(f"        family_members: 4")
        print(f"        pincode: '12345' (ONLY 5 DIGITS - should be 6)")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Bad Request)")
        print(f"    - JSON: {{'error': '{expected_error}'}}")
        print(f"    - Behavior: API should REJECT invalid pincode format")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_data, indent=8) if actual_data else 'None'}")
        print(f"    - Behavior: API {'REJECTS' if is_validated else 'ACCEPTS'} 5-digit pincode")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Invalid pincode '12345' is accepted!")
            print("    RECOMMENDATION: Add pincode validation for 6-digit format.")
        print("=" * 80)
        
        assert actual_status == expected_status, \
            f"API accepts invalid pincode! Expected 400, got {actual_status}"


# =============================================================================
# ISSUE CATEGORY 2: DATA INTEGRITY ISSUES
# =============================================================================

class TestDataIntegrityFailures:
    """
    Test cases demonstrating data integrity issues.
    These tests FAIL because the API accepts logically invalid data.
    """

    # -------------------------------------------------------------------------
    # TEST 6: Campaign with Past Date Accepted
    # -------------------------------------------------------------------------
    def test_campaign_accepts_past_date(self, client, rwa_manager_token):
        """
        ================================================================================
        FAILURE TEST 6: Campaign Creation Accepts Past Dates
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/secondary/campaigns/create
        Description: Test that API rejects campaigns with past dates - currently it does NOT.
        Issue: Campaigns in the past are useless and confuse users.
        """
        input_data = {
            "name": "Past Campaign Test",
            "description": "This campaign is scheduled for the past",
            "location": "Test Location",
            "event_datetime": "2020-01-01T10:00:00"  # PAST DATE - 4+ years ago
        }
        
        expected_status = 400
        expected_error = "Event date cannot be in the past"
        
        response = client.post('/api/secondary/campaigns/create', 
                               json=input_data, headers=rwa_manager_token)
        actual_status = response.status_code
        actual_data = response.get_json()
        
        is_validated = actual_status == 400
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: Campaign Creation - Past Date Validation")
        print("=" * 80)
        print(f"Endpoint: POST /api/secondary/campaigns/create")
        print(f"Issue Type: DATA INTEGRITY - Logical Validation Missing")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST")
        print(f"    - Authorization: Bearer <rwa_manager_token>")
        print(f"    - JSON Body:")
        print(f"        name: 'Past Campaign Test'")
        print(f"        description: 'This campaign is scheduled for the past'")
        print(f"        location: 'Test Location'")
        print(f"        event_datetime: '2020-01-01T10:00:00' (PAST DATE)")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Bad Request)")
        print(f"    - JSON: {{'error': '{expected_error}'}}")
        print(f"    - Behavior: API should REJECT past event dates")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_data, indent=8) if actual_data else 'None'}")
        print(f"    - Behavior: API {'REJECTS' if is_validated else 'ACCEPTS'} past date (2020-01-01)")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Campaign with past date (2020-01-01) is accepted!")
            print("    RECOMMENDATION: Add date validation to reject past dates.")
        print("=" * 80)
        
        assert actual_status == expected_status, \
            f"API accepts past campaign date! Expected 400, got {actual_status}"

    # -------------------------------------------------------------------------
    # TEST 7: Zero Family Members Accepted
    # -------------------------------------------------------------------------
    def test_family_members_accepts_zero(self, client):
        """
        ================================================================================
        FAILURE TEST 7: Zero Family Members Not Validated
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/auth/register
        Description: Test that API requires at least 1 family member - currently it does NOT.
        Issue: Zero family members is logically impossible for a household.
        """
        test_email = f"zerofam_{uuid.uuid4().hex[:8]}@test.com"
        
        input_data = {
            "email": test_email,
            "password": "TestPass123",
            "house_number": "101",
            "ward_number": "1",
            "family_members": 0,  # ZERO MEMBERS - Should be at least 1
            "pincode": "700001"
        }
        
        expected_status = 400
        expected_error = "Family members must be at least 1"
        
        response = client.post('/api/auth/register', json=input_data)
        actual_status = response.status_code
        actual_data = response.get_json()
        
        is_validated = actual_status == 400
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: User Registration - Zero Family Members Validation")
        print("=" * 80)
        print(f"Endpoint: POST /api/auth/register")
        print(f"Issue Type: DATA INTEGRITY - Logical Validation Missing")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST")
        print(f"    - JSON Body:")
        print(f"        email: {test_email}")
        print(f"        password: 'TestPass123'")
        print(f"        house_number: '101'")
        print(f"        ward_number: '1'")
        print(f"        family_members: 0 (ZERO MEMBERS)")
        print(f"        pincode: '700001'")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Bad Request)")
        print(f"    - JSON: {{'error': '{expected_error}'}}")
        print(f"    - Behavior: API should REJECT households with 0 members")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_data, indent=8) if actual_data else 'None'}")
        print(f"    - Behavior: API {'REJECTS' if is_validated else 'ACCEPTS'} 0 family members")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Zero family members is accepted!")
            print("    RECOMMENDATION: Add validation to require family_members >= 1.")
        print("=" * 80)
        
        assert actual_status == expected_status, \
            f"API accepts 0 family members! Expected 400, got {actual_status}"


# =============================================================================
# ISSUE CATEGORY 3: AUTHORIZATION/ACCESS CONTROL ISSUES
# =============================================================================

class TestAuthorizationFailures:
    """
    Test cases demonstrating authorization and access control issues.
    These tests check if role-based access control is properly enforced.
    """

    # -------------------------------------------------------------------------
    # TEST 8: Primary User Accessing Secondary Endpoints
    # -------------------------------------------------------------------------
    def test_primary_user_accessing_secondary_endpoint(self, client, primary_user_token):
        """
        ================================================================================
        FAILURE TEST 8: Primary User Access to Secondary Endpoints
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: GET /api/secondary/pickup-summary
        Description: Test that primary users cannot access secondary-only endpoints.
        Issue: Role-based access control must be enforced.
        """
        expected_status = 403  # Forbidden
        expected_error = "Access denied - requires secondary user role"
        
        response = client.get('/api/secondary/pickup-summary', 
                              headers=primary_user_token)
        actual_status = response.status_code
        actual_data = response.get_json()
        
        # 403 = properly denied, 401 = also acceptable (not authorized)
        is_restricted = actual_status in [401, 403]
        result = "Success" if is_restricted else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: Secondary Pickup Summary - Role-Based Access Control")
        print("=" * 80)
        print(f"Endpoint: GET /api/secondary/pickup-summary")
        print(f"Issue Type: AUTHORIZATION - Cross-Role Access Control")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: GET")
        print(f"    - Authorization: Bearer <PRIMARY_USER_TOKEN>")
        print(f"    - User Role: PRIMARY (attempting to access SECONDARY endpoint)")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Forbidden) or 401 (Unauthorized)")
        print(f"    - JSON: {{'error': '{expected_error}'}}")
        print(f"    - Behavior: API should DENY access to primary users")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_data, indent=8) if actual_data else 'None'}")
        print(f"    - Behavior: API {'DENIES' if is_restricted else 'ALLOWS'} access")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Primary user can access secondary endpoints!")
            print("    RECOMMENDATION: Add role-based access control middleware.")
        else:
            print("    NOTE: Role-based access control is working correctly.")
        print("=" * 80)
        
        assert is_restricted, \
            f"Primary user can access secondary endpoint! Got status {actual_status}"

    # -------------------------------------------------------------------------
    # TEST 9: Secondary User Accessing Tertiary Endpoints
    # -------------------------------------------------------------------------
    def test_secondary_user_accessing_tertiary_endpoint(self, client, collector_token):
        """
        ================================================================================
        FAILURE TEST 9: Secondary User Access to Tertiary Endpoints
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: GET /api/tertiary/dashboard
        Description: Test that secondary users cannot access tertiary-only endpoints.
        Issue: Role-based access control must be enforced.
        """
        expected_status = 403  # Forbidden
        expected_error = "Access denied - requires tertiary user role"
        
        response = client.get('/api/tertiary/dashboard', 
                              headers=collector_token)
        actual_status = response.status_code
        actual_data = response.get_json()
        
        is_restricted = actual_status in [401, 403]
        result = "Success" if is_restricted else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: Tertiary Dashboard - Role-Based Access Control")
        print("=" * 80)
        print(f"Endpoint: GET /api/tertiary/dashboard")
        print(f"Issue Type: AUTHORIZATION - Cross-Role Access Control")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: GET")
        print(f"    - Authorization: Bearer <SECONDARY_USER_TOKEN> (Collector)")
        print(f"    - User Role: SECONDARY (attempting to access TERTIARY endpoint)")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Forbidden) or 401 (Unauthorized)")
        print(f"    - JSON: {{'error': '{expected_error}'}}")
        print(f"    - Behavior: API should DENY access to secondary users")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_data, indent=8) if actual_data else 'None'}")
        print(f"    - Behavior: API {'DENIES' if is_restricted else 'ALLOWS'} access")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Secondary user can access tertiary endpoints!")
            print("    RECOMMENDATION: Add role-based access control middleware.")
        else:
            print("    NOTE: Role-based access control is working correctly.")
        print("=" * 80)
        
        assert is_restricted, \
            f"Secondary user can access tertiary endpoint! Got status {actual_status}"


# =============================================================================
# ISSUE CATEGORY 4: RATE LIMITING / ABUSE PREVENTION
# =============================================================================

class TestAbusePrevention:
    """
    Test cases demonstrating missing rate limiting and abuse prevention.
    These tests FAIL because the API allows unlimited requests.
    """

    # -------------------------------------------------------------------------
    # TEST 10: No Rate Limiting on Quiz Submissions
    # -------------------------------------------------------------------------
    def test_quiz_no_rate_limiting(self, client, primary_user_token):
        """
        ================================================================================
        FAILURE TEST 10: No Rate Limiting on Quiz Submissions
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/primary/quiz/submit
        Description: Test that API has rate limiting for quiz submissions.
        Issue: Users can abuse rapid submissions to farm points.
        """
        input_data = {"answers": []}
        
        expected_status_after_limit = 429  # Too Many Requests
        
        # Submit quiz 5 times rapidly
        print("\n" + "=" * 80)
        print("API BEING TESTED: Quiz Submission - Rate Limiting")
        print("=" * 80)
        print(f"Endpoint: POST /api/primary/quiz/submit")
        print(f"Issue Type: SECURITY - Missing Rate Limiting")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST (5 rapid submissions)")
        print(f"    - Authorization: Bearer <primary_user_token>")
        print(f"    - JSON Body: {json.dumps(input_data)}")
        print("-" * 80)
        
        responses = []
        for i in range(5):
            response = client.post('/api/primary/quiz/submit', 
                                   json=input_data, headers=primary_user_token)
            responses.append(response.status_code)
        
        has_rate_limit = 429 in responses
        result = "Success" if has_rate_limit else "Fail"
        
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status_after_limit} (Too Many Requests)")
        print(f"    - At least one of the 5 rapid submissions should be rate-limited")
        print(f"    - Behavior: API should LIMIT rapid submissions")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - Status codes for 5 submissions: {responses}")
        print(f"    - Rate limiting triggered: {'YES' if has_rate_limit else 'NO'}")
        print(f"    - Behavior: API {'HAS' if has_rate_limit else 'LACKS'} rate limiting")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: No rate limiting - all 5 rapid submissions were accepted!")
            print("    RECOMMENDATION: Implement rate limiting (e.g., max 1 per minute).")
        print("=" * 80)
        
        assert has_rate_limit, \
            f"No rate limiting! All 5 rapid submissions succeeded: {responses}"


# =============================================================================
# ISSUE CATEGORY 5: CAMPAIGN & PICKUP OPERATION ISSUES
# =============================================================================

class TestCampaignAndPickupFailures:
    """
    Test cases demonstrating issues with campaign registration and pickup operations.
    These tests check for proper validation and error handling.
    """

    # -------------------------------------------------------------------------
    # TEST 11: Duplicate Campaign Registration Not Prevented
    # -------------------------------------------------------------------------
    def test_duplicate_campaign_registration(self, client, primary_user_token, rwa_manager_token):
        """
        ================================================================================
        FAILURE TEST 11: Duplicate Campaign Registration Not Prevented
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/primary/campaigns/{id}/register
        Description: Test that API prevents registering for same campaign twice.
        Issue: Users might register multiple times for the same campaign.
        """
        # First create a campaign
        campaign_data = {
            "name": "Duplicate Registration Test Campaign",
            "description": "Testing duplicate registration",
            "location": "Test Location",
            "event_datetime": "2025-12-31T10:00:00"
        }
        create_response = client.post('/api/secondary/campaigns/create', 
                                      json=campaign_data, 
                                      headers=rwa_manager_token)
        campaign_id = create_response.get_json().get("campaign", {}).get("id", 1)
        
        # Register once
        client.post(f'/api/primary/campaigns/{campaign_id}/register', 
                    headers=primary_user_token)
        
        # Try to register again
        response = client.post(f'/api/primary/campaigns/{campaign_id}/register', 
                               headers=primary_user_token)
        actual_json = response.get_json()
        actual_status = response.status_code
        
        expected_status = 400  # Should reject duplicate registration
        is_validated = actual_status == 400 or "already registered" in str(actual_json).lower()
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: Campaign Registration - Duplicate Prevention")
        print("=" * 80)
        print(f"Endpoint: POST /api/primary/campaigns/{campaign_id}/register")
        print(f"Issue Type: DATA INTEGRITY - Duplicate Prevention")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST (second registration attempt)")
        print(f"    - Authorization: Bearer <primary_user_token>")
        print(f"    - Campaign ID: {campaign_id}")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Bad Request)")
        print(f"    - JSON: {{'error': 'Already registered for this campaign'}}")
        print(f"    - Behavior: API should REJECT duplicate registration")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_json, indent=8) if actual_json else 'None'}")
        print(f"    - Behavior: API {'REJECTS' if is_validated else 'ACCEPTS'} duplicate registration")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: User can register for the same campaign multiple times!")
            print("    RECOMMENDATION: Check for existing registration before creating new one.")
        print("=" * 80)
        
        assert is_validated, \
            f"API allows duplicate campaign registration! Got status {actual_status}"

    # -------------------------------------------------------------------------
    # TEST 12: Campaign Update Without Ownership Check
    # -------------------------------------------------------------------------
    def test_campaign_update_ownership(self, client, rwa_manager_token, collector_token):
        """
        ================================================================================
        FAILURE TEST 12: Campaign Update Without Ownership Validation
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: PUT /api/secondary/campaigns/{id}
        Description: Test that only campaign creator can update the campaign.
        Issue: Any secondary user might update campaigns they didn't create.
        """
        # Create a campaign as RWA manager
        campaign_data = {
            "name": "Ownership Test Campaign",
            "description": "Testing ownership validation",
            "location": "Test Location",
            "event_datetime": "2025-12-28T10:00:00"
        }
        create_response = client.post('/api/secondary/campaigns/create', 
                                      json=campaign_data, 
                                      headers=rwa_manager_token)
        campaign_id = create_response.get_json().get("campaign", {}).get("id", 1)
        
        # Try to update as a different user (collector)
        update_data = {
            "name": "Malicious Update",
            "description": "This should not be allowed"
        }
        
        response = client.put(f'/api/secondary/campaigns/{campaign_id}', 
                              json=update_data, 
                              headers=collector_token)
        actual_json = response.get_json()
        actual_status = response.status_code
        
        expected_status = 403  # Forbidden - not the owner
        is_validated = actual_status in [403, 401]
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: Campaign Update - Ownership Validation")
        print("=" * 80)
        print(f"Endpoint: PUT /api/secondary/campaigns/{campaign_id}")
        print(f"Issue Type: AUTHORIZATION - Ownership Check Missing")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: PUT")
        print(f"    - Authorization: Bearer <collector_token> (NOT the creator)")
        print(f"    - Campaign ID: {campaign_id} (created by RWA manager)")
        print(f"    - JSON: {json.dumps(update_data)}")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Forbidden)")
        print(f"    - JSON: {{'error': 'Not authorized to update this campaign'}}")
        print(f"    - Behavior: API should REJECT updates from non-owners")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_json, indent=8) if actual_json else 'None'}")
        print(f"    - Behavior: API {'REJECTS' if is_validated else 'ALLOWS'} unauthorized update")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Non-owner can update campaigns created by others!")
            print("    RECOMMENDATION: Add ownership check before allowing updates.")
        print("=" * 80)
        
        assert is_validated, \
            f"API allows non-owner to update campaign! Got status {actual_status}"

    # -------------------------------------------------------------------------
    # TEST 13: Campaign Delete Without Ownership Check
    # -------------------------------------------------------------------------
    def test_campaign_delete_ownership(self, client, rwa_manager_token, collector_token):
        """
        ================================================================================
        FAILURE TEST 13: Campaign Delete Without Ownership Validation
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: DELETE /api/secondary/campaigns/{id}
        Description: Test that only campaign creator can delete the campaign.
        Issue: Any secondary user might delete campaigns they didn't create.
        """
        # Create a campaign as RWA manager
        campaign_data = {
            "name": "Delete Ownership Test",
            "description": "Testing delete ownership validation",
            "location": "Test Location",
            "event_datetime": "2025-12-27T10:00:00"
        }
        create_response = client.post('/api/secondary/campaigns/create', 
                                      json=campaign_data, 
                                      headers=rwa_manager_token)
        campaign_id = create_response.get_json().get("campaign", {}).get("id", 1)
        
        # Try to delete as a different user (collector)
        response = client.delete(f'/api/secondary/campaigns/{campaign_id}', 
                                 headers=collector_token)
        actual_json = response.get_json()
        actual_status = response.status_code
        
        expected_status = 403  # Forbidden - not the owner
        is_validated = actual_status in [403, 401]
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: Campaign Delete - Ownership Validation")
        print("=" * 80)
        print(f"Endpoint: DELETE /api/secondary/campaigns/{campaign_id}")
        print(f"Issue Type: AUTHORIZATION - Ownership Check Missing")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: DELETE")
        print(f"    - Authorization: Bearer <collector_token> (NOT the creator)")
        print(f"    - Campaign ID: {campaign_id} (created by RWA manager)")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Forbidden)")
        print(f"    - JSON: {{'error': 'Not authorized to delete this campaign'}}")
        print(f"    - Behavior: API should REJECT deletion by non-owners")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_json, indent=8) if actual_json else 'None'}")
        print(f"    - Behavior: API {'REJECTS' if is_validated else 'ALLOWS'} unauthorized deletion")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Non-owner can delete campaigns created by others!")
            print("    RECOMMENDATION: Add ownership check before allowing deletion.")
        print("=" * 80)
        
        assert is_validated, \
            f"API allows non-owner to delete campaign! Got status {actual_status}"

    # -------------------------------------------------------------------------
    # TEST 14: Pickup Accept Without Reason Field for Rejection
    # -------------------------------------------------------------------------
    def test_pickup_reject_missing_reason(self, client, primary_user_token, collector_token):
        """
        ================================================================================
        FAILURE TEST 14: Pickup Rejection Without Required Reason
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/secondary/pickup/{id}/reject
        Description: Test that rejection requires a reason.
        Issue: Collectors should provide reasons when rejecting pickups.
        """
        # Create a waste log first
        waste_data = {
            "wet_waste": 2.0,
            "dry_waste": 1.0,
            "hazardous_waste": 0.0,
            "separated": True,
            "recycled": False
        }
        waste_response = client.post('/api/primary/waste-log', 
                                     json=waste_data, 
                                     headers=primary_user_token)
        pickup_id = waste_response.get_json().get("pickup_request_id", 1) or 1
        
        # Try to reject without reason
        response = client.post(f'/api/secondary/pickup/{pickup_id}/reject', 
                               json={},  # No reason provided
                               headers=collector_token)
        actual_json = response.get_json()
        actual_status = response.status_code
        
        expected_status = 400  # Should require reason
        is_validated = actual_status == 400 or actual_status == 404  # 404 if no pending pickup
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: Pickup Rejection - Reason Validation")
        print("=" * 80)
        print(f"Endpoint: POST /api/secondary/pickup/{pickup_id}/reject")
        print(f"Issue Type: INPUT VALIDATION - Missing Required Field")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST")
        print(f"    - Authorization: Bearer <collector_token>")
        print(f"    - Pickup ID: {pickup_id}")
        print(f"    - JSON: {{}} (NO REASON PROVIDED)")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Bad Request)")
        print(f"    - JSON: {{'error': 'Rejection reason is required'}}")
        print(f"    - Behavior: API should REQUIRE reason for rejection")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_json, indent=8) if actual_json else 'None'}")
        print(f"    - Behavior: API {'REQUIRES' if is_validated else 'ACCEPTS'} rejection without reason")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Pickup can be rejected without providing a reason!")
            print("    RECOMMENDATION: Make reason field required for rejections.")
        print("=" * 80)
        
        # This test might pass if there's no pending pickup (404) or if reason is required (400)
        assert is_validated, \
            f"API allows rejection without reason! Got status {actual_status}"

    # -------------------------------------------------------------------------
    # TEST 15: Primary User Cannot Accept/Reject Pickups
    # -------------------------------------------------------------------------
    def test_primary_user_cannot_manage_pickups(self, client, primary_user_token):
        """
        ================================================================================
        FAILURE TEST 15: Primary User Managing Pickup Requests
        ================================================================================
        
        [ API being tested,
        Inputs,
        Expected output,
        Actual Output,
        Result- Success/Fail ]

        API: POST /api/secondary/pickup/{id}/accept
        Description: Test that primary users cannot accept pickup requests.
        Issue: Only collectors should manage pickup requests.
        """
        pickup_id = 1
        
        response = client.post(f'/api/secondary/pickup/{pickup_id}/accept', 
                               headers=primary_user_token)
        actual_json = response.get_json()
        actual_status = response.status_code
        
        expected_status = 403  # Forbidden for primary users
        is_validated = actual_status in [401, 403]
        result = "Success" if is_validated else "Fail"
        
        print("\n" + "=" * 80)
        print("API BEING TESTED: Pickup Accept - Role-Based Access Control")
        print("=" * 80)
        print(f"Endpoint: POST /api/secondary/pickup/{pickup_id}/accept")
        print(f"Issue Type: AUTHORIZATION - Cross-Role Access Control")
        print("-" * 80)
        print("\nInputs:")
        print(f"    - Request Method: POST")
        print(f"    - Authorization: Bearer <PRIMARY_USER_TOKEN>")
        print(f"    - User Role: PRIMARY (attempting to accept pickup)")
        print("-" * 80)
        print("\nExpected Output:")
        print(f"    - HTTP Status Code: {expected_status} (Forbidden)")
        print(f"    - JSON: {{'error': 'Only collectors can manage pickups'}}")
        print(f"    - Behavior: API should DENY pickup management to primary users")
        print("-" * 80)
        print("\nActual Output:")
        print(f"    - HTTP Status Code: {actual_status}")
        print(f"    - JSON: {json.dumps(actual_json, indent=8) if actual_json else 'None'}")
        print(f"    - Behavior: API {'DENIES' if is_validated else 'ALLOWS'} primary user")
        print("-" * 80)
        print(f"\nResult: {result}")
        if result == "Fail":
            print("    ISSUE: Primary user can access pickup management endpoints!")
            print("    RECOMMENDATION: Restrict pickup operations to collector role only.")
        else:
            print("    NOTE: Role-based access control is working correctly.")
        print("=" * 80)
        
        assert is_validated, \
            f"Primary user can manage pickups! Got status {actual_status}"


# =============================================================================
# SUMMARY SECTION
# =============================================================================

class TestFailureSummary:
    """
    Summary test that documents all failure categories.
    """

    def test_print_failure_summary(self, client):
        """
        ================================================================================
        FAILURE TEST SUMMARY
        ================================================================================
        
        This test prints a summary of all failure categories tested.
        """
        print("\n" + "=" * 80)
        print("FAILURE TESTS SUMMARY")
        print("=" * 80)
        print("""
These tests demonstrate issues in the API that need improvement:

CATEGORY 1: INPUT VALIDATION FAILURES (5 tests)
    1. Empty password accepted
    2. Short password (3 chars) accepted
    3. Invalid email format accepted
    4. Negative waste values accepted
    5. Invalid pincode format accepted

CATEGORY 2: DATA INTEGRITY FAILURES (2 tests)
    6. Campaign with past date accepted
    7. Zero family members accepted

CATEGORY 3: AUTHORIZATION FAILURES (2 tests)
    8. Primary user accessing secondary endpoints
    9. Secondary user accessing tertiary endpoints

CATEGORY 4: ABUSE PREVENTION FAILURES (1 test)
    10. No rate limiting on quiz submissions

CATEGORY 5: CAMPAIGN & PICKUP OPERATION FAILURES (5 tests)
    11. Duplicate campaign registration not prevented
    12. Campaign update without ownership check
    13. Campaign delete without ownership check
    14. Pickup rejection without required reason
    15. Primary user managing pickup requests

TOTAL: 15 Failure Tests
-------------------------------------------------------------------
HOW TESTING IMPROVES THE API:

These failures identify specific areas where the API needs improvement:

1. SECURITY: Password policies prevent unauthorized access
2. DATA QUALITY: Input validation ensures clean data
3. DATA INTEGRITY: Logical validation prevents impossible data
4. AUTHORIZATION: Role-based access protects sensitive endpoints
5. ABUSE PREVENTION: Rate limiting prevents system abuse
6. OWNERSHIP: Ownership checks protect user-created resources
7. DUPLICATE PREVENTION: Duplicate checks prevent data inconsistencies

Each failed test provides a clear recommendation for improvement.
        """)
        print("=" * 80)
        
        # This test always passes - it's just for documentation
        assert True


# =============================================================================
# RUN CONFIGURATION
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
