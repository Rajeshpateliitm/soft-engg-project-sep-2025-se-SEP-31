# API Documentation - Milestone 4

## WasteWise Application API Endpoints

This document provides a comprehensive list of all API endpoints implemented in the WasteWise application, organized by user category and functionality.

---

## Table of Contents

1. [APIs Integrated from Libraries](#apis-integrated-from-libraries)
2. [APIs Created by Development Team](#apis-created-by-development-team)
3. [API Endpoints by Category](#api-endpoints-by-category)
4. [Error Handling](#error-handling)
5. [User Stories Mapping](#user-stories-mapping)

---

## APIs Integrated from Libraries

### Authentication & Security (python-jose)

- **JWT Token Generation**: Used for creating access tokens during login/registration
- **Token Verification**: Used for authenticating API requests via `@token_required` decorator
- **Password Hashing**: Using Werkzeug's password hashing utilities

### Database ORM (SQLAlchemy/Flask-SQLAlchemy)

- **Database Query Operations**: All CRUD operations on database models
- **Database Migrations**: Schema management and migrations
- **Relationship Management**: Foreign key relationships and joins

### Email (Flask-Mail)

- **Email Sending**: Sending email notifications and reminders
- **SMTP Integration**: MailHog for development, SMTP for production

---

## APIs Created by Development Team

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

### API Version
- **Current Version**: v1
- **API Prefix**: `/api`

---

## API Endpoints by Category

### 1. Authentication APIs (`/api/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register a new primary user | No |
| POST | `/api/auth/login` | Login user and get access token | No |
| GET | `/api/auth/me` | Get current authenticated user information | Yes |

### 2. Primary User APIs (`/api/primary`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/primary/dashboard` | Get primary user dashboard data | Yes |
| GET | `/api/primary/quiz/questions` | Get quiz questions for daily quiz | Yes |
| POST | `/api/primary/quiz/submit` | Submit quiz answers and get results | Yes |
| GET | `/api/primary/quiz/performance` | Get quiz performance history | Yes |
| POST | `/api/primary/waste-log` | Log waste entry | Yes |
| GET | `/api/primary/waste-logs` | Get waste log history | Yes |
| GET | `/api/primary/waste-summary` | Get waste summary statistics | Yes |
| GET | `/api/primary/leaderboard` | Get ward-specific leaderboard | Yes |
| GET | `/api/primary/monthly-engagement` | Get monthly engagement analytics | Yes |
| GET | `/api/primary/campaigns` | Get available campaigns | Yes |
| POST | `/api/primary/campaigns/<id>/register` | Register for a campaign | Yes |

### 3. Secondary User APIs (`/api/secondary`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/secondary/dashboard` | Get RWA manager dashboard | Yes |
| GET | `/api/secondary/collector/dashboard` | Get collector dashboard | Yes |
| GET | `/api/secondary/rwa-leaderboard` | Get RWA leaderboard | Yes |
| GET | `/api/secondary/pickup-summary` | Get monthly pickup summary | Yes |
| GET | `/api/secondary/pickup-details` | Get daily pickup details | Yes |
| POST | `/api/secondary/pickup/<id>/accept` | Accept pickup request | Yes |
| POST | `/api/secondary/pickup/<id>/reject` | Reject pickup request | Yes |
| GET | `/api/secondary/waste-summary` | Get waste summary for area | Yes |
| GET | `/api/secondary/campaigns` | Get campaigns managed by user | Yes |
| POST | `/api/secondary/campaigns/create` | Create new campaign | Yes |
| PUT | `/api/secondary/campaigns/<id>` | Update campaign | Yes |
| DELETE | `/api/secondary/campaigns/<id>` | Delete campaign | Yes |
| GET | `/api/secondary/waste-logs` | Get waste logs for area | Yes |

### 4. Tertiary User APIs (`/api/tertiary`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tertiary/dashboard` | Get government/NGO dashboard | Yes |
| GET | `/api/tertiary/ward-performance` | Get ward performance overview | Yes |
| GET | `/api/tertiary/ward/<id>/summary` | Get detailed ward summary | Yes |
| POST | `/api/tertiary/ward/<id>/update-summary` | Update ward monthly summary | Yes |

### 5. Common APIs (`/api/common`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/common/recyclers` | Get recycler locations by pincode | No |
| POST | `/api/common/pickup-request` | Create pickup request | Yes |
| GET | `/api/common/wards` | Get list of all wards | No |

---

## Error Handling

All APIs follow a consistent error handling pattern:

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET/PUT request |
| 201 | Created | Successful POST request (resource created) |
| 400 | Bad Request | Invalid input data, missing required fields |
| 401 | Unauthorized | Invalid or missing authentication token |
| 403 | Forbidden | Authenticated but insufficient permissions |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server-side error |

### Error Response Format

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Error Scenarios

1. **Missing Required Fields** (400)
   - All required fields must be provided
   - Example: `{"error": "Missing required field: email"}`

2. **Authentication Required** (401)
   - Token missing or invalid
   - Example: `{"error": "Authentication required"}`

3. **Invalid Credentials** (401)
   - Wrong email/password combination
   - Example: `{"error": "Invalid email or password"}`

4. **Resource Not Found** (404)
   - Requested resource doesn't exist
   - Example: `{"error": "Campaign not found"}`

5. **Duplicate Resource** (400)
   - Resource already exists
   - Example: `{"error": "Email already registered"}`

6. **Insufficient Permissions** (403)
   - User doesn't have required permissions
   - Example: `{"error": "Only RWA admins can create campaigns"}`

---

## User Stories Mapping

### Primary User Stories

#### US-1: User Registration and Authentication
- **API**: `POST /api/auth/register`
- **API**: `POST /api/auth/login`
- **API**: `GET /api/auth/me`
- **Description**: Primary users can register, login, and view their profile

#### US-2: Daily Quiz System
- **API**: `GET /api/primary/quiz/questions`
- **API**: `POST /api/primary/quiz/submit`
- **API**: `GET /api/primary/quiz/performance`
- **Description**: Users can take daily quizzes, get immediate feedback, and view performance history

#### US-3: Waste Logging
- **API**: `POST /api/primary/waste-log`
- **API**: `GET /api/primary/waste-logs`
- **API**: `GET /api/primary/waste-summary`
- **Description**: Users can log daily waste, view history, and see summary statistics

#### US-4: Leaderboard and Gamification
- **API**: `GET /api/primary/leaderboard`
- **API**: `GET /api/primary/dashboard`
- **Description**: Users can view their rank and points in ward-specific leaderboard

#### US-5: Monthly Engagement Tracking
- **API**: `GET /api/primary/monthly-engagement`
- **Description**: Users can view their monthly activity (quizzes, waste logs, campaigns)

#### US-6: Campaign Participation
- **API**: `GET /api/primary/campaigns`
- **API**: `POST /api/primary/campaigns/<id>/register`
- **Description**: Users can browse and register for community campaigns

#### US-7: Local Recycler Information
- **API**: `GET /api/common/recyclers`
- **Description**: Users can find local recyclers by pincode

### Secondary User (RWA/Collector) Stories

#### US-8: RWA Dashboard
- **API**: `GET /api/secondary/dashboard`
- **Description**: RWA managers can view overall statistics for their area

#### US-9: Collector Dashboard
- **API**: `GET /api/secondary/collector/dashboard`
- **Description**: Collectors can view pickup requests and daily pickup details

#### US-10: Pickup Request Management
- **API**: `GET /api/secondary/pickup-details`
- **API**: `POST /api/secondary/pickup/<id>/accept`
- **API**: `POST /api/secondary/pickup/<id>/reject`
- **Description**: Collectors can view, accept, or reject pickup requests

#### US-11: RWA Leaderboard
- **API**: `GET /api/secondary/rwa-leaderboard`
- **Description**: RWA managers can view leaderboard comparing different RWAs

#### US-12: Campaign Management
- **API**: `GET /api/secondary/campaigns`
- **API**: `POST /api/secondary/campaigns/create`
- **API**: `PUT /api/secondary/campaigns/<id>`
- **API**: `DELETE /api/secondary/campaigns/<id>`
- **Description**: RWA managers can create, update, and delete campaigns

#### US-13: Waste Summary for Area
- **API**: `GET /api/secondary/waste-summary`
- **API**: `GET /api/secondary/pickup-summary`
- **Description**: RWA managers and collectors can view waste statistics for their area

### Tertiary User (Government/NGO) Stories

#### US-14: Ward Performance Overview
- **API**: `GET /api/tertiary/ward-performance`
- **API**: `GET /api/tertiary/dashboard`
- **Description**: Government/NGO users can view performance metrics across all wards

#### US-15: Ward Summary Management
- **API**: `GET /api/tertiary/ward/<id>/summary`
- **API**: `POST /api/tertiary/ward/<id>/update-summary`
- **Description**: Government/NGO users can view and update ward monthly summaries

### Common User Stories

#### US-16: Pickup Request Creation
- **API**: `POST /api/common/pickup-request`
- **Description**: Users can create pickup requests for logged waste

#### US-17: Ward Information
- **API**: `GET /api/common/wards`
- **Description**: Users can get list of all available wards

---

## API Request/Response Examples

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "house_number": "123",
  "ward_number": "1",
  "family_members": 4,
  "pincode": "560001"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

### Primary User APIs

#### Get Dashboard
```http
GET /api/primary/dashboard
Authorization: Bearer <access_token>
```

#### Submit Quiz
```http
POST /api/primary/quiz/submit
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "answers": [
    {"question_id": 1, "option_id": 3},
    {"question_id": 2, "option_id": 5}
  ]
}
```

#### Log Waste
```http
POST /api/primary/waste-log
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "category": "wet",
  "quantity_kg": 2.5,
  "log_date": "2025-01-13",
  "separated": true,
  "recycled": false
}
```

### Secondary User APIs

#### Accept Pickup Request
```http
POST /api/secondary/pickup/123/accept
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "scheduled_at": "2025-01-14T10:00:00"
}
```

#### Create Campaign
```http
POST /api/secondary/campaigns/create
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Clean Ward Drive",
  "description": "Join us for a clean ward drive",
  "start_date": "2025-01-20",
  "end_date": "2025-01-25",
  "ward_id": 1
}
```

---

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```http
Authorization: Bearer <access_token>
```

The access token is obtained from the login or registration endpoint and is valid for 7 days.

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider implementing rate limiting to prevent abuse.

---

## Versioning

Current API version: v1

API endpoints are prefixed with `/api`. Future versions may use `/api/v2`, etc.

---

## Swagger Documentation

For interactive API documentation, see the Swagger-compatible YAML file: `api_swagger.yaml`

---

## Support

For API-related questions or issues, please refer to:
- Backend code: `backend/app/api/`
- API implementation files by category:
  - Authentication: `backend/app/api/auth.py`
  - Primary users: `backend/app/api/primary.py`
  - Secondary users: `backend/app/api/secondary.py`
  - Tertiary users: `backend/app/api/tertiary.py`
  - Common: `backend/app/api/common.py`

