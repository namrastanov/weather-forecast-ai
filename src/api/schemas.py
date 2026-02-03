"""Pydantic schemas for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ForecastRequest(BaseModel):
    """Request schema for weather prediction."""
    coordinates: tuple[float, float] = Field(..., description="Lat/lon coordinates")
    days: int = Field(default=7, ge=1, le=14)
    include_hourly: bool = False
    
    model_config = {"json_schema_extra": {"example": {"coordinates": [51.5074, -0.1278], "days": 7}}}


class DailyForecast(BaseModel):
    """Single day forecast."""
    date: str
    temp_high: float
    temp_low: float
    precipitation_chance: float = Field(ge=0, le=100)
    conditions: str
    wind_speed: float
    humidity: float


class ForecastResponse(BaseModel):
    """Response schema for weather forecast."""
    location: str
    forecasts: List[DailyForecast]
    generated_at: str
    model_version: str = "1.0.0"


class HistoricalDataPoint(BaseModel):
    """Single historical data point."""
    timestamp: str
    temperature: float
    humidity: float
    pressure: float
    precipitation: float


class HistoricalResponse(BaseModel):
    """Response for historical data request."""
    location: str
    data: List[HistoricalDataPoint]
    start_date: Optional[str] = None
    end_date: Optional[str] = None
