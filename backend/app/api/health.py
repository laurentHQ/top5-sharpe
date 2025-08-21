"""
Health Check API Endpoint

Provides health status and version information for the application.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.core.config import settings


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    version: str


router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint
    
    Returns the application status and version information.
    
    Returns:
        HealthResponse: Status and version information
    """
    return HealthResponse(
        status="ok",
        version=settings.VERSION
    )