from fastapi import APIRouter
from app.schemas.health import HealthResponse
router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")
