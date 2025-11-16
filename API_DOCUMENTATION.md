# WasteWise API Documentation

## Milestone 4 Deliverables

This document provides comprehensive documentation for all APIs implemented in the WasteWise application, including integrated third-party APIs, custom API endpoints, user story mappings, and error handling.

---

## Table of Contents

1. [List of APIs Integrated](#list-of-apis-integrated)
2. [List of APIs Created](#list-of-apis-created)
3. [API Endpoints Description](#api-endpoints-description)
4. [User Stories Mapping](#user-stories-mapping)
5. [Error Handling](#error-handling)
6. [Authentication & Security](#authentication--security)

---

## List of APIs Integrated

The following third-party APIs and libraries are integrated into the WasteWise application:

### 1. Google Gemini API
- **Purpose**: Generative AI chatbot functionality for waste management assistance
- **Integration**: REST API calls to Google's Generative Language API
- **Base URL**: `https://generativelanguage.googleapis.com/v1beta/models`
- **Model**: `gemini-1.5-flash`
- **Endpoints Used**:
  - `POST /v1beta/models/{model}:generateContent`
- **Authentication**: API Key (Bearer token)
- **Use Case**: Provides AI-powered responses to user queries about waste segregation, recycling, and disposal
- **Documentation**: [Google Gemini API Documentation](https://ai.google.dev/docs)

### 2. JWT (JSON Web Tokens)
- **Library**: PyJWT
- **Purpose**: User authentication and authorization
- **Algorithm**: HS256 (HMAC-SHA256)
- **Token Expiration**: 7 days
- **Use Case**: Secure token-based authentication for all protected endpoints
- **Implementation**: Custom JWT token generation and validation in `app/core/security.py`

---

## List of APIs Created

The following custom API endpoints have been created for the WasteWise application:

### Authentication APIs (`/api/auth`)
1. `POST /api/auth/register` - User registration
2. `POST /api/auth/login` - User login
3. `GET /api/auth/me` - Get current user information

### Primary User APIs (`/api/primary`)
4. `GET /api/primary/dashboard` - Get dashboard data
5. `GET /api/primary/quiz/questions` - Get quiz questions
6. `POST /api/primary/quiz/submit` - Submit quiz answers
7. `GET /api/primary/quiz/performance` - Get quiz performance details
8. `POST /api/primary/waste-log` - Log waste entry
9. `GET /api/primary/waste-logs` - Get waste logs
10. `GET /api/primary/waste-summary` - Get waste summary
11. `GET /api/primary/leaderboard` - Get community leaderboard
12. `GET /api/primary/monthly-engagement` - Get monthly engagement analytics
13. `GET /api/primary/campaigns` - Get available campaigns
14. `POST /api/primary/campaigns/<id>/register` - Register for a campaign

### Secondary User APIs (`/api/secondary`)
15. `GET /api/secondary/dashboard` - Get RWA manager dashboard
16. `GET /api/secondary/collector/dashboard` - Get collector dashboard
17. `GET /api/secondary/rwa-leaderboard` - Get RWA leaderboard
18. `GET /api/secondary/pickup-summary` - Get monthly pickup summary
19. `GET /api/secondary/pickup-details` - Get daily pickup details
20. `POST /api/secondary/pickup/<id>/accept` - Accept pickup request
21. `POST /api/secondary/pickup/<id>/reject` - Reject pickup request
22. `GET /api/secondary/waste-summary` - Get household performance summary
23. `GET /api/secondary/campaigns` - Get all campaigns
24. `POST /api/secondary/campaigns/create` - Create a new campaign
25. `PUT /api/secondary/campaigns/<id>` - Update campaign
26. `DELETE /api/secondary/campaigns/<id>` - Delete campaign
27. `GET /api/secondary/waste-logs` - Get waste logs by date

### Tertiary User APIs (`/api/tertiary`)
28. `GET /api/tertiary/dashboard` - Get tertiary user dashboard
29. `GET /api/tertiary/ward-performance` - Get ward-wise performance summary
30. `GET /api/tertiary/ward/<id>/summary` - Get detailed ward summary
31. `POST /api/tertiary/ward/<id>/update-summary` - Update ward monthly summary

### Common APIs (`/api/common`)
32. `GET /api/common/recyclers` - Get recycler locations by pincode
33. `POST /api/common/pickup-request` - Create a pickup request
34. `GET /api/common/wards` - Get all wards

### GenAI APIs (`/api/genai`)
35. `POST /api/genai/chat` - Chat with WasteWise AI Assistant
36. `POST /api/genai/chat/clear` - Clear chat history

**Total Custom APIs Created**: 36 endpoints

---

## API Endpoints Description

### Authentication Endpoints

#### 1. POST /api/auth/register
- **Description**: Register a new PRIMARY user account
- **Request Body**: email, password, house_number, ward_number, family_members, pincode, username (optional)
- **Response**: User object and JWT access token
- **Status Codes**: 201 (Created), 400 (Bad Request), 500 (Internal Server Error)
- **Special Notes**: Only PRIMARY users can register. Secondary and Tertiary users are provisioned by administrators.

#### 2. POST /api/auth/login
- **Description**: Authenticate user and receive JWT access token
- **Request Body**: email, password
- **Response**: JWT access token, token type, and user information
- **Status Codes**: 200 (OK), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden)
- **Special Notes**: Returns RWA role for secondary users (admin, collector, or null)

#### 3. GET /api/auth/me
- **Description**: Get authenticated user's profile information
- **Headers**: Authorization: Bearer <token>
- **Response**: Complete user profile including points, category, and RWA role
- **Status Codes**: 200 (OK), 401 (Unauthorized)

### Primary User Endpoints

#### 4. GET /api/primary/dashboard
- **Description**: Get comprehensive dashboard data including quiz performance, leaderboard rank, monthly engagement, and waste summary
- **Response**: Aggregated dashboard statistics
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 5. GET /api/primary/quiz/questions
- **Description**: Retrieve quiz questions for a quiz session
- **Query Parameters**: limit (default: 10), category (optional)
- **Response**: Array of questions with options
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 6. POST /api/primary/quiz/submit
- **Description**: Submit quiz answers and calculate score
- **Request Body**: answers (array of question_id and option_id pairs)
- **Response**: Score, percentage, and points earned
- **Status Codes**: 200 (OK), 400 (Bad Request), 401 (Unauthorized)

#### 7. GET /api/primary/quiz/performance
- **Description**: Get detailed quiz performance history
- **Response**: Total attempts, average score, best score, and recent attempts
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 8. POST /api/primary/waste-log
- **Description**: Create a new waste log entry
- **Request Body**: category (wet/dry/hazardous), quantity_kg, log_date, separated, recycled, questions_doubts, feedback
- **Response**: Created waste log object
- **Status Codes**: 201 (Created), 400 (Bad Request), 401 (Unauthorized)

#### 9. GET /api/primary/waste-logs
- **Description**: Retrieve waste log entries with optional date filtering
- **Query Parameters**: start_date, end_date (optional)
- **Response**: Array of waste log entries
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 10. GET /api/primary/waste-summary
- **Description**: Get waste summary statistics for the last 30 days
- **Response**: Total waste by category, segregation rate, recycling rate
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 11. GET /api/primary/leaderboard
- **Description**: Get leaderboard of PRIMARY users in the same ward
- **Response**: Ranked list of users with points
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 12. GET /api/primary/monthly-engagement
- **Description**: Get monthly engagement statistics
- **Query Parameters**: month, year (optional, defaults to current)
- **Response**: Quizzes taken, waste logs created, campaigns participated
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 13. GET /api/primary/campaigns
- **Description**: Get list of active campaigns
- **Response**: Array of campaign objects with registration status
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 14. POST /api/primary/campaigns/<id>/register
- **Description**: Register for a specific campaign
- **Path Parameters**: campaign_id
- **Response**: Registration confirmation
- **Status Codes**: 201 (Created), 400 (Bad Request), 401 (Unauthorized)

### Secondary User Endpoints

#### 15. GET /api/secondary/dashboard
- **Description**: Get RWA manager dashboard (admin role only)
- **Response**: RWA leaderboard rank and household count
- **Status Codes**: 200 (OK), 403 (Forbidden), 401 (Unauthorized)

#### 16. GET /api/secondary/collector/dashboard
- **Description**: Get waste collector dashboard
- **Response**: Today's pickup summary, ward information, household count
- **Status Codes**: 200 (OK), 403 (Forbidden), 401 (Unauthorized)

#### 17. GET /api/secondary/rwa-leaderboard
- **Description**: Get leaderboard of all RWA groups
- **Response**: Ranked list of RWAs with points and remarks
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 18. GET /api/secondary/pickup-summary
- **Description**: Get monthly pickup statistics
- **Query Parameters**: months (default: 1)
- **Response**: Completion rates, waste distribution, daily breakdown
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 19. GET /api/secondary/pickup-details
- **Description**: Get detailed pickup requests for a specific date
- **Query Parameters**: date (YYYY-MM-DD, defaults to today)
- **Response**: List of pickup requests with user and location details
- **Status Codes**: 200 (OK), 400 (Bad Request), 401 (Unauthorized)

#### 20. POST /api/secondary/pickup/<id>/accept
- **Description**: Accept a pending pickup request (collectors only)
- **Path Parameters**: pickup_id
- **Response**: Acceptance confirmation and points awarded
- **Status Codes**: 200 (OK), 400 (Bad Request), 403 (Forbidden), 404 (Not Found), 401 (Unauthorized)

#### 21. POST /api/secondary/pickup/<id>/reject
- **Description**: Reject a pending pickup request (collectors only)
- **Path Parameters**: pickup_id
- **Response**: Rejection confirmation and points deducted
- **Status Codes**: 200 (OK), 400 (Bad Request), 403 (Forbidden), 404 (Not Found), 401 (Unauthorized)

#### 22. GET /api/secondary/waste-summary
- **Description**: Get household performance summary for all PRIMARY users in ward
- **Response**: Segregation rates, per capita waste, engagement scores
- **Status Codes**: 200 (OK), 400 (Bad Request), 401 (Unauthorized)

#### 23. GET /api/secondary/campaigns
- **Description**: Get all campaigns (secondary users can view all)
- **Response**: Array of all campaign objects
- **Status Codes**: 200 (OK), 401 (Unauthorized)

#### 24. POST /api/secondary/campaigns/create
- **Description**: Create a new waste management campaign
- **Request Body**: name, description, location, event_datetime, pincode, ward_id, image_url
- **Response**: Created campaign object
- **Status Codes**: 201 (Created), 400 (Bad Request), 401 (Unauthorized)

#### 25. PUT /api/secondary/campaigns/<id>
- **Description**: Update an existing campaign
- **Path Parameters**: campaign_id
- **Request Body**: Partial campaign data (all fields optional)
- **Response**: Updated campaign object
- **Status Codes**: 200 (OK), 400 (Bad Request), 404 (Not Found), 401 (Unauthorized)

#### 26. DELETE /api/secondary/campaigns/<id>
- **Description**: Soft delete (deactivate) a campaign
- **Path Parameters**: campaign_id
- **Response**: Deletion confirmation
- **Status Codes**: 200 (OK), 404 (Not Found), 401 (Unauthorized)

#### 27. GET /api/secondary/waste-logs
- **Description**: Get waste logs from PRIMARY users in ward for a specific date
- **Query Parameters**: date (YYYY-MM-DD, defaults to today)
- **Response**: Summary statistics and household waste details
- **Status Codes**: 200 (OK), 400 (Bad Request), 401 (Unauthorized)

### Tertiary User Endpoints

#### 28. GET /api/tertiary/dashboard
- **Description**: Get comprehensive city-wide dashboard
- **Response**: All ward data, city-wide statistics, priority actions
- **Status Codes**: 200 (OK), 403 (Forbidden), 401 (Unauthorized)

#### 29. GET /api/tertiary/ward-performance
- **Description**: Get performance summary for all wards
- **Response**: Ward-wise waste generation, segregation compliance, remarks
- **Status Codes**: 200 (OK), 403 (Forbidden), 401 (Unauthorized)

#### 30. GET /api/tertiary/ward/<id>/summary
- **Description**: Get detailed monthly summary for a specific ward
- **Path Parameters**: ward_id
- **Query Parameters**: months (default: 12)
- **Response**: Historical monthly summaries
- **Status Codes**: 200 (OK), 404 (Not Found), 401 (Unauthorized)

#### 31. POST /api/tertiary/ward/<id>/update-summary
- **Description**: Create or update monthly summary for a ward
- **Path Parameters**: ward_id
- **Request Body**: year, month, total_households, avg_wet_kg_per_day, avg_dry_kg_per_day, avg_hazardous_kg_per_day, segregation_compliance_pct, remarks
- **Response**: Summary confirmation
- **Status Codes**: 200 (OK), 400 (Bad Request), 404 (Not Found), 401 (Unauthorized)

### Common Endpoints

#### 32. GET /api/common/recyclers
- **Description**: Get recycler locations by pincode (public endpoint)
- **Query Parameters**: pincode (required)
- **Response**: Array of recycler locations with coordinates and materials accepted
- **Status Codes**: 200 (OK), 400 (Bad Request)
- **Special Notes**: No authentication required

#### 33. POST /api/common/pickup-request
- **Description**: Create a waste pickup request
- **Request Body**: scheduled_at, pickup_location, pincode, quantity, notes
- **Response**: Created pickup request with request code
- **Status Codes**: 201 (Created), 400 (Bad Request), 401 (Unauthorized)

#### 34. GET /api/common/wards
- **Description**: Get list of all active wards (public endpoint)
- **Response**: Array of ward objects
- **Status Codes**: 200 (OK)
- **Special Notes**: No authentication required

### GenAI Endpoints

#### 35. POST /api/genai/chat
- **Description**: Send message to WasteWise AI Assistant powered by Google Gemini
- **Request Body**: message (string)
- **Response**: AI-generated response
- **Status Codes**: 200 (OK), 400 (Bad Request), 401 (Unauthorized), 500 (Internal Server Error)
- **Special Notes**: Maintains conversation history (last 5 messages)

#### 36. POST /api/genai/chat/clear
- **Description**: Clear conversation history for current user
- **Response**: Confirmation message
- **Status Codes**: 200 (OK), 401 (Unauthorized)

---

## User Stories Mapping

### Primary User Stories

| User Story | API Endpoints | Description |
|------------|---------------|-------------|
| As a household user, I want to register for an account | `POST /api/auth/register` | User registration |
| As a user, I want to login to my account | `POST /api/auth/login` | User authentication |
| As a user, I want to view my profile | `GET /api/auth/me` | Get user information |
| As a household user, I want to see my dashboard | `GET /api/primary/dashboard` | Dashboard overview |
| As a household user, I want to take daily quizzes | `GET /api/primary/quiz/questions`, `POST /api/primary/quiz/submit` | Quiz functionality |
| As a household user, I want to view my quiz performance | `GET /api/primary/quiz/performance` | Quiz analytics |
| As a household user, I want to log my daily waste | `POST /api/primary/waste-log` | Waste logging |
| As a household user, I want to view my waste history | `GET /api/primary/waste-logs` | Waste log history |
| As a household user, I want to see my waste summary | `GET /api/primary/waste-summary` | Waste statistics |
| As a household user, I want to see the leaderboard | `GET /api/primary/leaderboard` | Community ranking |
| As a household user, I want to see my monthly engagement | `GET /api/primary/monthly-engagement` | Engagement analytics |
| As a household user, I want to see available campaigns | `GET /api/primary/campaigns` | Campaign listing |
| As a household user, I want to register for campaigns | `POST /api/primary/campaigns/<id>/register` | Campaign registration |
| As a user, I want to find nearby recyclers | `GET /api/common/recyclers` | Recycler search |
| As a household user, I want to request waste pickup | `POST /api/common/pickup-request` | Pickup scheduling |
| As a household user, I want to chat with an AI assistant | `POST /api/genai/chat` | AI chatbot |
| As a user, I want to see available wards | `GET /api/common/wards` | Ward listing |

### Secondary User Stories (RWA Managers)

| User Story | API Endpoints | Description |
|------------|---------------|-------------|
| As an RWA manager, I want to see my dashboard | `GET /api/secondary/dashboard` | RWA dashboard |
| As an RWA manager, I want to see the RWA leaderboard | `GET /api/secondary/rwa-leaderboard` | RWA ranking |
| As an RWA manager, I want to see household performance | `GET /api/secondary/waste-summary` | Performance monitoring |
| As an RWA manager, I want to see pickup summary | `GET /api/secondary/pickup-summary` | Pickup analytics |
| As an RWA manager, I want to see all campaigns | `GET /api/secondary/campaigns` | Campaign management |
| As an RWA manager, I want to create campaigns | `POST /api/secondary/campaigns/create` | Campaign creation |
| As an RWA manager, I want to update campaigns | `PUT /api/secondary/campaigns/<id>` | Campaign updates |
| As an RWA manager, I want to delete campaigns | `DELETE /api/secondary/campaigns/<id>` | Campaign deletion |
| As an RWA manager, I want to see daily waste logs | `GET /api/secondary/waste-logs` | Waste monitoring |

### Secondary User Stories (Waste Collectors)

| User Story | API Endpoints | Description |
|------------|---------------|-------------|
| As a waste collector, I want to see my dashboard | `GET /api/secondary/collector/dashboard` | Collector dashboard |
| As a waste collector, I want to see pickup summary | `GET /api/secondary/pickup-summary` | Pickup statistics |
| As a waste collector, I want to see daily pickup details | `GET /api/secondary/pickup-details` | Daily pickup list |
| As a waste collector, I want to accept pickup requests | `POST /api/secondary/pickup/<id>/accept` | Accept pickups |
| As a waste collector, I want to reject pickup requests | `POST /api/secondary/pickup/<id>/reject` | Reject pickups |

### Tertiary User Stories (Government/NGO)

| User Story | API Endpoints | Description |
|------------|---------------|-------------|
| As a government/NGO representative, I want to see city-wide dashboard | `GET /api/tertiary/dashboard` | City dashboard |
| As a government/NGO representative, I want to see ward performance | `GET /api/tertiary/ward-performance` | Ward analytics |
| As a government/NGO representative, I want to see detailed ward summaries | `GET /api/tertiary/ward/<id>/summary` | Historical data |
| As a government/NGO representative, I want to update ward summaries | `POST /api/tertiary/ward/<id>/update-summary` | Summary management |

---

## Error Handling

### Standard HTTP Status Codes

The API uses standard HTTP status codes to indicate the result of API requests:

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request parameters or missing required fields
- **401 Unauthorized**: Missing or invalid authentication token
- **403 Forbidden**: Authenticated but insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side error

### Error Response Format

All error responses follow a consistent format:

```json
{
  "error": "Error message describing what went wrong",
  "error_details": {
    // Optional additional error details
  }
}
```

### Common Error Scenarios

#### 1. Authentication Errors

**401 Unauthorized - Missing Token**
```json
{
  "error": "Token is missing or invalid"
}
```

**401 Unauthorized - Invalid Token**
```json
{
  "error": "Invalid or expired token"
}
```

**403 Forbidden - Insufficient Permissions**
```json
{
  "error": "This dashboard is for RWA managers only. Collectors should use the collector dashboard.",
  "user_role": "collector",
  "redirect_to": "collector-dashboard"
}
```

#### 2. Validation Errors

**400 Bad Request - Missing Required Fields**
```json
{
  "error": "Missing required field: email"
}
```

**400 Bad Request - Invalid Data Format**
```json
{
  "error": "Invalid date format. Use YYYY-MM-DD"
}
```

**400 Bad Request - Invalid Email**
```json
{
  "error": "Email already registered"
}
```

#### 3. Resource Errors

**404 Not Found - Resource Not Found**
```json
{
  "error": "Campaign not found"
}
```

**400 Bad Request - Resource Conflict**
```json
{
  "error": "Pickup request is not pending"
}
```

#### 4. Business Logic Errors

**400 Bad Request - Invalid Operation**
```json
{
  "error": "Only primary users can register through public sign-up. Secondary and Tertiary users are provisioned by administrators."
}
```

**400 Bad Request - Already Registered**
```json
{
  "error": "User already registered for this campaign"
}
```

#### 5. External API Errors

**500 Internal Server Error - Gemini API Error**
```json
{
  "error": "API error: 429",
  "error_details": {
    "status": "RESOURCE_EXHAUSTED",
    "message": "Quota exceeded"
  }
}
```

**500 Internal Server Error - Network Error**
```json
{
  "error": "Network error: Connection timeout"
}
```

### Error Handling Implementation

All endpoints implement comprehensive error handling:

1. **Input Validation**: All required fields are validated before processing
2. **Authentication Checks**: Protected endpoints verify JWT tokens
3. **Authorization Checks**: Role-based access control for secondary/tertiary endpoints
4. **Database Errors**: SQLAlchemy exceptions are caught and returned as user-friendly errors
5. **External API Errors**: Google Gemini API errors are caught and handled gracefully
6. **Exception Handling**: All unexpected errors are caught and logged with appropriate error messages

### Error Logging

- All errors are logged server-side for debugging
- Sensitive information (passwords, tokens) is never included in error responses
- Stack traces are logged but not exposed to clients in production

---

## Authentication & Security

### JWT Token Authentication

- **Algorithm**: HS256 (HMAC-SHA256)
- **Token Expiration**: 7 days
- **Token Format**: Bearer token in Authorization header
- **Header Format**: `Authorization: Bearer <access_token>`

### Password Security

- **Hashing Algorithm**: PBKDF2-SHA256
- **Iterations**: 100,000
- **Salt Length**: 16 bytes
- **Implementation**: Werkzeug's `generate_password_hash` and `check_password_hash`

### Role-Based Access Control (RBAC)

- **PRIMARY Users**: Can access primary endpoints, common endpoints, and GenAI endpoints
- **SECONDARY Users (RWA Managers)**: Can access secondary endpoints with admin role
- **SECONDARY Users (Collectors)**: Can access collector-specific endpoints
- **TERTIARY Users**: Can access tertiary endpoints for city-wide monitoring

### Security Best Practices

1. **Password Hashing**: All passwords are hashed using PBKDF2 with 100,000 iterations
2. **Token Validation**: All protected endpoints validate JWT tokens
3. **SQL Injection Prevention**: All database queries use SQLAlchemy ORM (parameterized queries)
4. **CORS Configuration**: CORS is configured to allow requests from frontend origin
5. **Input Validation**: All user inputs are validated before processing
6. **Error Message Sanitization**: Error messages don't expose sensitive system information

---

## API Base URL

- **Development**: `http://localhost:8000/api`
- **Production**: `https://api.wastewise.com/api` (example)

---

## Swagger Documentation

A complete Swagger-compatible YAML file is available at:
- **File**: `backend/api_swagger.yaml`
- **Format**: OpenAPI 3.0.3
- **View Online**: Import the YAML file into Swagger UI or Postman for interactive API documentation

---

## Backend Code Implementation

All API endpoints are implemented in the following files:

- **Authentication**: `backend/app/api/auth.py`
- **Primary User**: `backend/app/api/primary.py`
- **Secondary User**: `backend/app/api/secondary.py`
- **Tertiary User**: `backend/app/api/tertiary.py`
- **Common**: `backend/app/api/common.py`
- **GenAI**: `backend/app/api/genai.py`
- **Security**: `backend/app/core/security.py`
- **Models**: `backend/app/models.py`

---

## Conclusion

This API documentation provides a comprehensive overview of all APIs implemented in the WasteWise application, including third-party integrations, custom endpoints, user story mappings, and error handling. The Swagger-compatible YAML file (`api_swagger.yaml`) provides detailed technical specifications for each endpoint, including request/response schemas, status codes, and examples.

