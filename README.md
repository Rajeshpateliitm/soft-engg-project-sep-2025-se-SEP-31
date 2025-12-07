# How to Run the WasteWise Project

## Prerequisites

Before running the project, make sure you have:

1. **Python 3.8+** installed
2. **Node.js 16+** and **npm** installed
3. **Virtual environment** (optional but recommended)

---

## Step 1: Setup Backend (Flask)

### 1.1 Navigate to backend directory

```bash
cd backend
```

### 1.2 Create and activate virtual environment (if not already done)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 1.3 Install Python dependencies

```bash
pip install -r requirements.txt
```

### 1.4 Run the backend server

```bash
python main.py
```

**Expected output:**
```
 Database initialized with sample data
 * Running on http://0.0.0.0:8000
 * Debug mode: on
```

**Note:** The database will be automatically initialized with sample data on first run. You don't need to run a separate initialization command.

**Keep this terminal window open!** The backend server must be running.

---

## Step 2: Setup Frontend (Vue.js)

### 2.1 Open a NEW terminal window

**Important:** Keep the backend terminal running, open a new terminal for the frontend.

### 2.2 Navigate to frontend directory

```bash
cd frontend
```

### 2.3 Install Node.js dependencies (only needed first time)

```bash
npm install
```

This will install all required packages including:
- Vue 3
- Vue Router
- Pinia (state management)
- Axios (API calls)
- Chart.js (charts)
- Bootstrap (UI components)

### 2.4 Run the frontend development server

```bash
npm run dev
```

**Expected output:**
```
  VITE v7.x.x  ready in xxx ms

    Local:   http://localhost:5173/
    Network: use --host to expose
```

**Keep this terminal window open too!**

---

## Step 3: Access the Application

### Open your web browser and navigate to:

```
http://localhost:5173
```

**Important Notes:**
-  **Use `http://localhost:5173`** - This is your frontend application
-  **Don't use `http://localhost:8000`** - That's just the API backend

---

## Quick Reference

### Terminal 1 (Backend - Flask):

```bash
cd backend
source venv/bin/activate  # If using virtual environment
venv\Scripts\activate # If using virtual environment in terminal
python main.py
# Server runs on http://localhost:8000
# Database is automatically initialized on first run
```

### Terminal 2 (Frontend - Vue.js):

```bash
cd frontend
npm install              # First time only
npm run dev
# App runs on http://localhost:5173
```

### Browser:

```
http://localhost:5173  ← Open this URL!
```

---

## First Time Setup Checklist

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Backend dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Frontend dependencies installed (`npm install` in frontend directory)
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] Browser opened to `http://localhost:5173`

---

## Troubleshooting

### Backend Issues

#### Port 8000 already in use?

```bash
# Find and kill the process using port 8000
# On macOS/Linux:
lsof -ti:8000 | xargs kill -9

# On Windows:
# netstat -ano | findstr :8000
# taskkill /PID <PID> /F
```

#### Database not found?

The SQLite database (`wastewise.db`) will be automatically created when you run `python main.py` for the first time. Sample data will also be seeded automatically.

#### Module not found errors?

```bash
cd backend
pip install -r requirements.txt
```

### Frontend Issues

#### Port 5173 already in use?

Vite will automatically use the next available port (5174, 5175, etc.). Check the terminal output for the actual port.

#### npm install fails?

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Frontend can't connect to backend?

1. Make sure backend is running on `http://localhost:8000`
2. Check browser console for errors
3. Verify `frontend/vite.config.js` has proxy configuration (already configured)

#### Module not found errors?

```bash
cd frontend
npm install
```

### General Issues

#### Virtual environment not activating?

```bash
# Make sure you're in the backend directory
cd backend

# Try with python3 explicitly
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

#### Permission errors?

```bash
# On macOS/Linux, you might need sudo for global npm packages
# But try without sudo first for local project packages
```

---

## Project Structure

```
soft-engg-project-sep-2025-se-SEP-31-dev/
├── backend/              # Flask backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models.py     # Database models
│   │   └── core/         # Core utilities
│   ├── main.py           # Backend entry point
│   ├── init_db.py        # Database initialization
│   ├── requirements.txt  # Python dependencies
│   └── wastewise.db     # SQLite database (auto-created)

## Test User Credentials

### Secondary User (Collector)
```json
{
  "email": "collector1@wastewise.com",
  "password": "Collector@123"
}
```

### Tertiary User
```json
{
  "email": "tertiary@wastewise.com",
  "password": "Tertiary@123"
}
```

## Gemini API Configuration

The application uses Google's Gemini API for AI-powered features. To set it up:

1. Get a Google API key with access to the Gemini API from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Configure the API key in your environment variables or in the Flask configuration:

### Option 1: Environment Variable (Recommended)
```bash
export GEMINI_API_KEY='your-api-key-here'
```

### Option 2: Flask Config
Add the following to your Flask configuration (e.g., in `config.py` or `main.py`):
```python
app.config['GEMINI_API_KEY'] = 'your-api-key-here'
app.config['GEMINI_API_MODEL'] = 'gemini-1.5-flash'  # or your preferred model
```

### Optional Configuration
You can also configure the base URL if needed (default is Google's API endpoint):
```python
app.config['GEMINI_API_BASE_URL'] = 'https://generativelanguage.googleapis.com/v1beta/models'
```

After setting up the API key, restart your Flask application for the changes to take effect.
│
└── frontend/             # Vue.js frontend
    ├── src/
    │   ├── components/   # Vue components
    │   ├── views/        # Page views
    │   ├── stores/       # Pinia stores
    │   └── router/       # Vue Router
    ├── package.json      # Node.js dependencies
    └── vite.config.js    # Vite configuration
```

---

## What Each Server Does

- **Backend (Port 8000)**: 
  - Provides REST API endpoints (`/api/*`)
  - Handles authentication (JWT tokens)
  - Manages database (SQLite)
  - Processes business logic

- **Frontend (Port 5173)**: 
  - Serves the Vue.js application
  - Makes API calls to backend
  - Handles user interface and routing
  - Manages client-side state

The frontend communicates with the backend via HTTP requests through the Vite proxy.

---

## Stopping the Servers

To stop the servers:

1. Go to each terminal window
2. Press `Ctrl + C` (or `Cmd + C` on Mac)
3. Confirm if prompted

---

## Next Steps After Running

1. **Register a new user** at `http://localhost:5173/register`
2. **Login** with your credentials
3. **Explore the dashboard** based on your user type:
   - Primary User: Quiz, Waste Log, Leaderboard
   - Secondary User: RWA Dashboard, Campaigns
   - Tertiary User: Ward Performance, Analytics

---

## Need Help?

If you encounter any issues:

1. Check the terminal output for error messages
2. Check browser console (F12) for frontend errors
3. Verify both servers are running
4. Ensure all dependencies are installed
5. Check that ports 8000 and 5173 are available
