# Initialize the FastAPI application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app():
    app = FastAPI(
        title="Windsurf API",
        description="Backend API for the Windsurf application",
        version="0.1.0",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with your frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    from .api import router as api_router
    app.include_router(api_router, prefix="/api")

    @app.get("/")
    async def root():
        return {"message": "Welcome to the Windsurf API!"}

    return app
