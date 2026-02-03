"""FastAPI endpoints for weather predictions."""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging

from .schemas import (
    ForecastRequest,
    ForecastResponse,
    HistoricalRequest,
    HistoricalResponse
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["weather"])


@router.get("/forecast/{location}")
async def get_forecast(
    location: str,
    days: int = Query(default=7, ge=1, le=14),
    include_hourly: bool = False
) -> ForecastResponse:
    """Get weather forecast for a location."""
    logger.info(f"Forecast request for {location}, {days} days")
    
    if not location or len(location) < 2:
        raise HTTPException(400, "Invalid location")
    
    return ForecastResponse(
        location=location,
        forecasts=[],
        generated_at="2024-01-01T00:00:00Z"
    )


@router.post("/predict")
async def predict_weather(request: ForecastRequest) -> ForecastResponse:
    """Submit custom prediction request."""
    logger.info(f"Prediction request: {request.coordinates}")
    return ForecastResponse(
        location=f"{request.coordinates[0]},{request.coordinates[1]}",
        forecasts=[],
        generated_at="2024-01-01T00:00:00Z"
    )


@router.get("/historical/{location}")
async def get_historical(
    location: str,
    start_date: str,
    end_date: str
) -> HistoricalResponse:
    """Get historical weather data."""
    return HistoricalResponse(location=location, data=[])


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
