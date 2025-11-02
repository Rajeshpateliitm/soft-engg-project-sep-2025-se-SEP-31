# Windsurf - Full Stack Application

A modern full-stack application(Waste Management) built with Vue 3 (Frontend) and FastAPI (Backend).



## 🚀 Features

- **Frontend**:
  - Vue 3 with Composition API
  - Vue Router for navigation
  - Pinia for state management
  - Tailwind CSS for styling
  - Responsive design

- **Backend**:
  - FastAPI framework
  - JWT Authentication
  - SQLAlchemy ORM with PostgreSQL
  - Pydantic for data validation
  - CORS middleware

## 🛠️ Prerequisites

- Node.js (v16+)
- Python (3.8+)
- PostgreSQL (v12+)
- npm or yarn
- pip (Python package manager)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/windsurf-project.git
cd windsurf-project
```

### 2. Backend Setup

1. Create and activate a virtual environment:
   ```bash
   # Linux/macOS
   python -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Set up the database:
   ```bash
   # Install PostgreSQL and create a database
   # Update DATABASE_URL in .env with your credentials
   # Example: postgresql://username:password@localhost:5432/windsurf_db
   ```

5. Run database migrations:
   ```bash
   # Install Alembic if not installed
   pip install alembic
   
   # Run migrations
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Interactive API Docs: `http://localhost:8000/redoc`

### 3. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## 📁 Project Structure

```
windsurf-project/
├── backend/               # FastAPI Backend
│   ├── app/               # Application package
│   │   ├── api/           # API routes
│   │   ├── core/          # Core functionality
│   │   ├── db/            # Database configuration
│   │   ├── models/        # Database models
│   │   └── schemas/       # Pydantic models
│   ├── alembic/           # Database migrations
│   ├── tests/             # Test files
│   ├── main.py            # Application entry point
│   └── requirements.txt   # Python dependencies
│
└── frontend/              # Vue 3 Frontend
    ├── public/            # Static files
    ├── src/               # Source files
    │   ├── assets/        # Static assets
    │   ├── components/    # Vue components
    │   ├── router/        # Vue Router configuration
    │   ├── stores/        # Pinia stores
    │   ├── views/         # Page components
    │   ├── App.vue        # Root component
    │   └── main.js        # Application entry point
    └── package.json       # Frontend dependencies
```

## 🌐 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info (protected)

### Users
- `GET /api/v1/users/` - List all users (admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user (owner or admin)
- `DELETE /api/v1/users/{user_id}` - Delete user (owner or admin)

## 🔒 Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
# Backend
DATABASE_URL=postgresql://username:password@localhost:5432/windsurf_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# Frontend (if needed)
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test:unit
```

## 🛠️ Development

### Code Style
- Backend: Follows PEP 8 with Black formatter and isort
- Frontend: Follows Vue 3 style guide with ESLint and Prettier

### Git Workflow
1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes and commit: `git commit -m "Add your feature"`
3. Push to the branch: `git push origin feature/your-feature-name`
4. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Vue.js Team
- FastAPI Team
- All contributors and open-source maintainers
