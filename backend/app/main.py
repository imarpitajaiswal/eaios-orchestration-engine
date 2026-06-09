from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as api_router
from app.db.database import Base, engine
from app.models import user  # Strictly required to register schema on startup

# Initialize database tables inside the containerized PostgreSQL engine
Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    """Enterprise Application Factory pattern for FastAPI."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    
    # Cross-Origin Resource Sharing (CORS) Configuration
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict to trusted origins in cloud deployment
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount the unified API router configuration
    application.include_router(api_router, prefix=settings.API_V1_STR)
    
    return application

# Expose the ASGI application executable for Uvicorn
app = create_app()