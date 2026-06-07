from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as api_router

def create_app() -> FastAPI:
    """Application Factory for EAIOS."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="Enterprise multi-agent orchestration platform."
    )

    # Configure CORS for Next.js frontend integration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # We will restrict this in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()