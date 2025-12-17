"""
Health check endpoint.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_db
from app.core.logging import get_logger
from app.schemas.farm import HealthResponse

logger = get_logger(__name__)
router = APIRouter()
settings = get_settings()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    teste de conexão com banco de dados.

    Returns:
        Health status including database connection status
    """
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "connected"
        logger.info("Health check passed")
    except Exception as err:
        logger.error("Health check failed", exc_info=err)
        raise HTTPException(status_code=503, detail="Database connection failed") from None

    return HealthResponse(status="healthy", database=db_status, version=settings.app_version)
