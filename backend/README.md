# WasteWise Backend API

Flask-based REST API backend for the WasteWise application.

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Application

**Note:** The database will be automatically initialized when you run the application for the first time. You don't need to run a separate initialization command.

```bash
python main.py
```

**Expected output:**
```
✅ Database initialized with sample data
 * Running on http://0.0.0.0:8000
 * Debug mode: on
```

The API will be available at `http://localhost:8000`

**Note:** On first run, the database will be automatically created and seeded with sample data. On subsequent runs, this initialization step is skipped.

## API Endpoints

### Authentication (`/api/auth`)

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/me` - Get current user information (requires authentication)

### Primary User Endpoints (`/api/primary`)

All endpoints require authentication via Bearer token.

- `GET /api/primary/dashboard` - Get dashboard data
- `GET /api/primary/quiz/questions` - Get quiz questions
- `POST /api/primary/quiz/submit` - Submit quiz answers
- `GET /api/primary/quiz/performance` - Get quiz performance details
- `POST /api/primary/waste-log` - Log waste entry
- `GET /api/primary/waste-summary` - Get waste summary
- `GET /api/primary/leaderboard` - Get community leaderboard
- `GET /api/primary/monthly-engagement` - Get monthly engagement analytics
- `GET /api/primary/campaigns` - Get available campaigns
- `POST /api/primary/campaigns/<id>/register` - Register for a campaign

### Secondary User Endpoints (`/api/secondary`)

- `GET /api/secondary/dashboard` - Get RWA/Collector dashboard
- `GET /api/secondary/rwa-leaderboard` - Get RWA leaderboard
- `GET /api/secondary/pickup-summary` - Get monthly pickup summary
- `GET /api/secondary/pickup-details` - Get daily pickup details
- `POST /api/secondary/pickup/<id>/accept` - Accept pickup request
- `POST /api/secondary/pickup/<id>/reject` - Reject pickup request
- `GET /api/secondary/waste-summary` - Get household performance summary
- `GET /api/secondary/campaigns` - Get all campaigns
- `POST /api/secondary/campaigns/create` - Create a new campaign

### Tertiary User Endpoints (`/api/tertiary`)

- `GET /api/tertiary/ward-performance` - Get ward-wise performance summary
- `GET /api/tertiary/ward/<id>/summary` - Get detailed ward summary
- `POST /api/tertiary/ward/<id>/update-summary` - Update ward monthly summary

### Common Endpoints (`/api/common`)

- `GET /api/common/recyclers?pincode=<pincode>` - Get recycler locations by pincode
- `POST /api/common/pickup-request` - Create a pickup request (requires auth)
- `GET /api/common/wards` - Get all wards

## Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Database

The application uses SQLite by default. The database file will be created at `backend/wastewise.db`.

To use a different database, set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="sqlite:///path/to/database.db"
```

## User Categories

- **PRIMARY**: Regular household users
- **SECONDARY**: RWA managers and waste collectors
- **TERTIARY**: Government bodies and NGOs

## Sample Request Examples

### Register User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "house_number": "123",
    "ward_number": "1",
    "family_members": 4,
    "pincode": "700001",
    "user_category": "PRIMARY"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Get Dashboard (with auth)

```bash
curl -X GET http://localhost:8000/api/primary/dashboard \
  -H "Authorization: Bearer <access_token>"
```

### Log Waste

```bash
curl -X POST http://localhost:8000/api/primary/waste-log \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "wet_waste": 2.5,
    "dry_waste": 1.8,
    "hazardous_waste": 0.5,
    "separated": true,
    "recycled": true,
    "log_date": "2025-01-15"
  }'
```

## Notes

- All timestamps are in UTC
- Date formats should be `YYYY-MM-DD`
- DateTime formats should be ISO 8601 format
- Points are awarded for:
  - Quiz answers: 10 points per correct answer
  - Waste segregation: 5 points
  - Recycling/reusing: 10 points

