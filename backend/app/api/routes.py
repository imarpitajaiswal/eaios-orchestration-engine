from fastapi import APIRouter
from app.api.endpoints import auth

router = APIRouter()

# Register the authentication endpoints to the main API router
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@router.get("/health")
def health_check():
    """Enterprise infrastructure validation endpoint."""
    return {
        "status": "active", 
        "system": "EAIOS Orchestration Engine", 
        "version": "1.0.0"
    }