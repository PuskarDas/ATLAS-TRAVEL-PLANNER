"""Main FastAPI application."""

from contextlib import asynccontextmanager
import logging

from config import get_settings
from database.connection import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import (
    auth,
    budget,
    chatbot,
    itinerary,
    recommendations,
    services,
    trips,
    websocket,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup logic
    try:
        logger.info("Initializing database tables...")
        init_db()
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

    try:
        from database.store import store
        from utils.auth_utils import hash_password

        if not any(
            user["email"] == "planner@example.com" for user in store.users.values()
        ):
            store.insert(
                "users",
                {
                    "username": "planner",
                    "email": "planner@example.com",
                    "hashed_password": hash_password("password123"),
                    "is_active": True,
                },
            )
    except Exception as e:
        logger.error(f"Failed to seed demo user: {e}")
    
    yield
    
    # Shutdown logic
    logger.info("Shutting down the application")

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Group Travel Planner API",
    description="Intelligent travel planning system for groups",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Get settings
settings = get_settings()

# Configure CORS
cors_kwargs = {
    "allow_origins": settings.cors_origins,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
# Allow typical LAN dev URLs (e.g. http://192.168.x.x:3000) when not using the Vite proxy.
if settings.environment == "development":
    cors_kwargs["allow_origin_regex"] = (
        r"https?://(localhost|127\.0\.0\.1|\[::1\]|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)?$"
    )

app.add_middleware(CORSMiddleware, **cors_kwargs)

app.include_router(auth.router)
app.include_router(trips.router)
app.include_router(recommendations.router)
app.include_router(itinerary.router)
app.include_router(budget.router)
app.include_router(chatbot.router)
app.include_router(services.router)
app.include_router(websocket.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AI-Powered Group Travel Planner",
        "version": settings.app_version,
        "docs": "/api/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/api/version")
async def get_version():
    """Get API version."""
    return {
        "version": settings.app_version,
        "app_name": settings.app_name
    }