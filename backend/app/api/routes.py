from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthCheckResponse(BaseModel):
    status: str
    system: str
    version: str

@router.get("/health", response_model=HealthCheckResponse, tags=["System"])
async def health_check():
    """
    Kubernetes-ready liveness probe.
    """
    from app.core.config import settings
    return HealthCheckResponse(
        status="active",
        system=settings.PROJECT_NAME,
        version=settings.VERSION
    )