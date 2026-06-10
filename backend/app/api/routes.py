from fastapi import APIRouter
from app.api.endpoints import auth, chat

router = APIRouter()

# Register the authentication endpoints
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Register the autonomous agent endpoints
router.include_router(chat.router, prefix="/chat", tags=["Agent Orchestration"])

@router.get("/health")
def health_check():
    """Enterprise infrastructure validation endpoint."""
    return {
        "status": "active", 
        "system": "EAIOS Orchestration Engine", 
        "version": "1.0.0"
    }