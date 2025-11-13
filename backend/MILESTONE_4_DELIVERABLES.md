# Milestone 4 Deliverables

## WasteWise API Endpoints Documentation

This document provides all deliverables required for Milestone 4 submission.

---

## 1. List of APIs Integrated (from Libraries)

### Authentication & Security
- **python-jose**: JWT token generation and verification
- **Werkzeug**: Password hashing utilities

### Database ORM
- **SQLAlchemy/Flask-SQLAlchemy**: Database queries, relationships, and migrations

### Email
- **Flask-Mail**: Email sending functionality for notifications and reminders

### HTTP & CORS
- **Flask**: Web framework and routing
- **Flask-CORS**: Cross-Origin Resource Sharing support

---

## 2. List of APIs Created (by Development Team)

### Total APIs Created: **33 Endpoints**

#### Authentication APIs (3 endpoints)
1. `POST /api/auth/register` - Register new user
2. `POST /api/auth/login` - Login user
3. `GET /api/auth/me` - Get current user info

#### Primary User APIs (11 endpoints)
4. `GET /api/primary/dashboard` - Get dashboard data
5. `GET /api/primary/quiz/questions` - Get quiz questions
6. `POST /api/primary/quiz/submit` - Submit quiz answers
7. `GET /api/primary/quiz/performance` - Get quiz performance
8. `POST /api/primary/waste-log` - Log waste entry
9. `GET /api/primary/waste-logs` - Get waste log history
10. `GET /api/primary/waste-summary` - Get waste summary
11. `GET /api/primary/leaderboard` - Get ward leaderboard
12. `GET /api/primary/monthly-engagement` - Get monthly engagement
13. `GET /api/primary/campaigns` - Get available campaigns
14. `POST /api/primary/campaigns/{id}/register` - Register for campaign

#### Secondary User APIs (12 endpoints)
15. `GET /api/secondary/dashboard` - Get RWA dashboard
16. `GET /api/secondary/collector/dashboard` - Get collector dashboard
17. `GET /api/secondary/pickup-details` - Get daily pickup details
18. `POST /api/secondary/pickup/{id}/accept` - Accept pickup request
19. `POST /api/secondary/pickup/{id}/reject` - Reject pickup request
20. `GET /api/secondary/rwa-leaderboard` - Get RWA leaderboard
21. `GET /api/secondary/pickup-summary` - Get pickup summary
22. `GET /api/secondary/waste-summary` - Get area waste summary
23. `GET /api/secondary/campaigns` - Get managed campaigns
24. `POST /api/secondary/campaigns/create` - Create campaign
25. `PUT /api/secondary/campaigns/{id}` - Update campaign
26. `DELETE /api/secondary/campaigns/{id}` - Delete campaign

#### Tertiary User APIs (4 endpoints)
27. `GET /api/tertiary/dashboard` - Get government/NGO dashboard
28. `GET /api/tertiary/ward-performance` - Get ward performance overview
29. `GET /api/tertiary/ward/{id}/summary` - Get ward summary
30. `POST /api/tertiary/ward/{id}/update-summary` - Update ward summary

#### Common APIs (3 endpoints)
31. `GET /api/common/recyclers` - Get recyclers by pincode
32. `POST /api/common/pickup-request` - Create pickup request
33. `GET /api/common/wards` - Get all wards

---

## 3. Description of API Endpoints (As per Problem Statement)

### Problem Statement Overview
WasteWise is a comprehensive waste management application that serves three types of users:
- **Primary Users (Residents)**: Track waste, take quizzes, participate in campaigns, compete on leaderboards
- **Secondary Users (RWA/Collectors)**: Manage pickups, create campaigns, monitor area statistics
- **Tertiary Users (Government/NGO)**: Monitor ward performance, update summaries, analyze city-wide data

### API Categories

#### Authentication & User Management
APIs for user registration, login, and profile management. Supports role-based access control.

#### Quiz System
APIs for daily quiz functionality including question retrieval, answer submission, and performance tracking. Awards points based on correct answers.

#### Waste Logging
APIs for logging waste entries with category (wet/dry/hazardous), quantity, and segregation status. Creates pickup requests automatically.

#### Pickup Management
APIs for collectors to view, accept, and reject pickup requests. Manages points allocation based on pickup status.

#### Leaderboards & Gamification
APIs for ward-specific leaderboards and point systems to encourage participation.

#### Campaign Management
APIs for creating, managing, and participating in community campaigns.

#### Analytics & Reporting
APIs for monthly engagement tracking, waste summaries, and ward performance analytics.

#### Recycler & Ward Information
APIs for finding local recyclers and accessing ward information.

---

## 4. Swagger-Compatible YAML File

**File**: `api_swagger.yaml`

This file contains:
- Complete OpenAPI 3.0.3 specification
- All 33 API endpoints documented
- Request/response schemas
- Error handling documentation
- User stories mapping
- Authentication specifications
- Example requests and responses

**Location**: `/backend/api_swagger.yaml`

**Validation**: The YAML file is compatible with:
- Swagger UI
- Swagger Editor
- OpenAPI Generator
- Postman (can import OpenAPI spec)

---

## 5. Backend Code (Implementation)

### File Structure
```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py          # Authentication APIs (3 endpoints)
│   │   ├── primary.py       # Primary user APIs (11 endpoints)
│   │   ├── secondary.py     # Secondary user APIs (12 endpoints)
│   │   ├── tertiary.py      # Tertiary user APIs (4 endpoints)
│   │   └── common.py        # Common APIs (3 endpoints)
│   ├── core/
│   │   ├── config.py        # Application configuration
│   │   └── security.py      # JWT authentication & authorization
│   ├── models.py            # Database models
│   └── __init__.py          # Flask app factory
└── api_swagger.yaml         # Swagger/OpenAPI documentation
```

### Key Implementation Details
- **Flask Blueprints**: Organized API endpoints by user category
- **JWT Authentication**: Token-based authentication using python-jose
- **SQLAlchemy ORM**: Database operations using Flask-SQLAlchemy
- **Error Handling**: Consistent error responses with appropriate HTTP status codes
- **Role-Based Access**: User category-based endpoint access control
- **Data Validation**: Input validation and error handling for all endpoints

---

## 6. Error Handling Documentation

All APIs implement consistent error handling:

### HTTP Status Codes
- **200 OK**: Successful GET/PUT request
- **201 Created**: Successful POST request (resource created)
- **400 Bad Request**: Invalid input, missing required fields
- **401 Unauthorized**: Missing/invalid authentication token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server-side error

### Error Response Format
```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Error Scenarios
1. **Missing Required Fields** (400)
2. **Authentication Required** (401)
3. **Invalid Credentials** (401)
4. **Resource Not Found** (404)
5. **Duplicate Resource** (400)
6. **Insufficient Permissions** (403)

### Error Handling Implementation
- Input validation for all request bodies
- Authentication checks via `@token_required` decorator
- Role-based authorization checks
- Database error handling (IntegrityError, etc.)
- Try-catch blocks for unexpected errors

---

## 7. User Stories Mapping

### Primary User Stories

| User Story | API Endpoints |
|------------|---------------|
| **US-1**: User Registration and Authentication | `POST /api/auth/register`<br>`POST /api/auth/login`<br>`GET /api/auth/me` |
| **US-2**: Daily Quiz System | `GET /api/primary/quiz/questions`<br>`POST /api/primary/quiz/submit`<br>`GET /api/primary/quiz/performance` |
| **US-3**: Waste Logging | `POST /api/primary/waste-log`<br>`GET /api/primary/waste-logs`<br>`GET /api/primary/waste-summary` |
| **US-4**: Leaderboard and Gamification | `GET /api/primary/leaderboard`<br>`GET /api/primary/dashboard` |
| **US-5**: Monthly Engagement Tracking | `GET /api/primary/monthly-engagement` |
| **US-6**: Campaign Participation | `GET /api/primary/campaigns`<br>`POST /api/primary/campaigns/{id}/register` |
| **US-7**: Local Recycler Information | `GET /api/common/recyclers` |

### Secondary User Stories

| User Story | API Endpoints |
|------------|---------------|
| **US-8**: RWA Dashboard | `GET /api/secondary/dashboard` |
| **US-9**: Collector Dashboard | `GET /api/secondary/collector/dashboard` |
| **US-10**: Pickup Request Management | `GET /api/secondary/pickup-details`<br>`POST /api/secondary/pickup/{id}/accept`<br>`POST /api/secondary/pickup/{id}/reject` |
| **US-11**: RWA Leaderboard | `GET /api/secondary/rwa-leaderboard` |
| **US-12**: Campaign Management | `GET /api/secondary/campaigns`<br>`POST /api/secondary/campaigns/create`<br>`PUT /api/secondary/campaigns/{id}`<br>`DELETE /api/secondary/campaigns/{id}` |
| **US-13**: Waste Summary for Area | `GET /api/secondary/waste-summary`<br>`GET /api/secondary/pickup-summary` |

### Tertiary User Stories

| User Story | API Endpoints |
|------------|---------------|
| **US-14**: Ward Performance Overview | `GET /api/tertiary/dashboard`<br>`GET /api/tertiary/ward-performance` |
| **US-15**: Ward Summary Management | `GET /api/tertiary/ward/{id}/summary`<br>`POST /api/tertiary/ward/{id}/update-summary` |

### Common User Stories

| User Story | API Endpoints |
|------------|---------------|
| **US-16**: Pickup Request Creation | `POST /api/common/pickup-request` |
| **US-17**: Ward Information | `GET /api/common/wards` |

---

## 8. Submission Checklist

### Required Deliverables

- [x] **Documentation of API's in Swagger-compatible YAML file**
  - File: `api_swagger.yaml`
  - Format: OpenAPI 3.0.3
  - Contains: All endpoints, schemas, error handling, user stories mapping

- [x] **Backend code of implemented API's**
  - Location: `backend/app/api/`
  - Files: `auth.py`, `primary.py`, `secondary.py`, `tertiary.py`, `common.py`
  - Total: 33 endpoints implemented

- [x] **Error Handling Documentation**
  - Documented in `API_DOCUMENTATION.md`
  - Documented in `api_swagger.yaml`
  - Implemented in code with consistent error responses

- [x] **User Stories Mapping**
  - Documented in `API_DOCUMENTATION.md`
  - Documented in `api_swagger.yaml`
  - Mapped to 17 user stories across 33 endpoints

- [x] **API Descriptions**
  - Detailed descriptions in `API_DOCUMENTATION.md`
  - Summary descriptions in `api_swagger.yaml`
  - Inline documentation in code (docstrings)

### Additional Documentation Files

1. **API_DOCUMENTATION.md**: Comprehensive API documentation with examples
2. **MILESTONE_4_DELIVERABLES.md**: This file - complete milestone deliverables
3. **api_swagger.yaml**: Swagger-compatible OpenAPI specification

---

## 9. How to Validate YAML File

### Using Swagger Editor (Online)
1. Go to https://editor.swagger.io/
2. Click "File" → "Import file"
3. Select `api_swagger.yaml`
4. View interactive API documentation

### Using Swagger UI (Local)
```bash
# Install Swagger UI
npm install -g swagger-ui-serve

# Run Swagger UI
swagger-ui-serve api_swagger.yaml
```

### Using OpenAPI Validator
```bash
# Install validator
npm install -g @apidevtools/swagger-cli

# Validate YAML
swagger-cli validate api_swagger.yaml
```

### Import to Postman
1. Open Postman
2. Click "Import"
3. Select "File" → Choose `api_swagger.yaml`
4. All endpoints will be imported as a collection

---

## 10. Summary

### Statistics
- **Total APIs Created**: 33 endpoints
- **APIs from Libraries**: 4 (JWT, ORM, Email, HTTP)
- **User Categories**: 3 (Primary, Secondary, Tertiary)
- **User Stories Covered**: 17 stories
- **Error Handling**: Comprehensive error responses for all endpoints
- **Documentation**: Complete Swagger-compatible YAML with descriptions

### Key Features
- RESTful API design
- JWT-based authentication
- Role-based access control
- Comprehensive error handling
- User story mapping
- Swagger-compatible documentation
- Clean code structure with Flask Blueprints

---

## Files for Submission

1. **api_swagger.yaml** - Swagger-compatible API documentation
2. **API_DOCUMENTATION.md** - Comprehensive API documentation
3. **MILESTONE_4_DELIVERABLES.md** - This file (deliverables overview)
4. **backend/app/api/** - All API implementation code
   - `auth.py`
   - `primary.py`
   - `secondary.py`
   - `tertiary.py`
   - `common.py`

---

## Contact

For questions or issues regarding the API documentation or implementation, please refer to the code or contact the development team.

---

**Note**: All APIs have been tested and validated. The Swagger YAML file is compatible with standard OpenAPI 3.0.3 tools and can be imported into Swagger UI, Postman, or any OpenAPI-compatible tool.

