from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/health", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    message: str


@router.get("", response_model=HealthResponse)
async def get_health():
    """Get application health status"""
    return HealthResponse(
        status="healthy",
        message="Signal Refinery API is running"
    )
