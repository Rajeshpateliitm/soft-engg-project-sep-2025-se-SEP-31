# How to Run the WasteWise Backend Application

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Step-by-Step Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- python-jose (for JWT)
- Werkzeug
- python-dotenv

### Step 4: Run the Application

**Note:** The database will be automatically initialized when you run the application for the first time. You don't need to run a separate initialization command.

```bash
python main.py
```

**Expected output:**
```
✅ Database initialized with sample data
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:8000
Press CTRL+C to quit
```

The API server is now running at: **http://localhost:8000**

**Note:** On first run, you'll see "✅ Database initialized with sample data" message. On subsequent runs, this message won't appear as the data already exists.

## Testing the Application

### 1. Check Health Endpoint

Open your browser or use curl:

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Test Registration

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "house_number": "123",
    "ward_number": "1",
    "family_members": 4,
    "pincode": "700001",
    "user_category": "PRIMARY"
  }'
```

### 3. Test Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

This will return an access token. Save it for authenticated requests.

### 4. Test Authenticated Endpoint

Replace `<access_token>` with the token from login:

```bash
curl -X GET http://localhost:8000/api/primary/dashboard \
  -H "Authorization: Bearer <access_token>"
```

## Common Issues and Solutions

### Issue 1: ModuleNotFoundError

**Problem:** `ModuleNotFoundError: No module named 'app'`

**Solution:** Make sure you're running commands from the `backend` directory:
```bash
cd backend
python main.py
```

### Issue 2: Port Already in Use

**Problem:** `Address already in use`

**Solution:** Either:
- Stop the other process using port 8000
- Or change the port in `main.py`:
  ```python
  app.run(host="0.0.0.0", port=8001, debug=True)
  ```

### Issue 3: Database Locked

**Problem:** `database is locked`

**Solution:** 
- Close any other connections to the database
- Delete `wastewise.db` and run `python init_db.py` again

### Issue 4: Import Errors

**Problem:** Import errors when running

**Solution:** Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Development Mode

The application runs in debug mode by default, which means:
- Auto-reloads when code changes
- Detailed error messages
- Debug toolbar (if configured)

## Production Deployment

For production:
1. Set `debug=False` in `main.py`
2. Use a production WSGI server (e.g., Gunicorn)
3. Set proper `SECRET_KEY` and `JWT_SECRET_KEY` in environment variables
4. Use a production database (PostgreSQL recommended)

## API Documentation

Once the server is running, you can test endpoints using:
- **Postman** (recommended for testing)
- **curl** (command line)
- **Browser** (for GET requests)
- **Your frontend application**

## Next Steps

1. **Integrate with Frontend:** Update your Vue.js frontend to call these API endpoints
2. **Configure CORS:** If frontend runs on different port, CORS is already configured
3. **Add More Data:** Use the API to create users, campaigns, etc.
4. **Test All Endpoints:** Test all endpoints to ensure they work correctly

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python main.py` | Start the Flask server (auto-initializes database on first run) |
| `curl http://localhost:8000/api/health` | Check if server is running |

## Support

If you encounter any issues:
1. Check that all dependencies are installed
2. Verify you're in the correct directory
3. Check the error messages for specific issues
4. Ensure Python 3.8+ is installed

