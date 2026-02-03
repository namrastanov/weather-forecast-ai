"""Input validation and sanitization for API endpoints."""

import re
from typing import Optional
from pydantic import BaseModel, field_validator, Field
import logging

logger = logging.getLogger(__name__)

COORDINATE_PATTERN = re.compile(r"^-?\d{1,3}\.?\d*$")
LOCATION_PATTERN = re.compile(r"^[a-zA-Z0-9\s,.\-']+$")
SQL_INJECTION_PATTERNS = [
    r"("|')\s*(OR|AND)\s*("|')",
    r";\s*(DROP|DELETE|INSERT|UPDATE)",
    r"UNION\s+SELECT",
    r"--",
    r"/\*.*\*/"
]


class LocationQuery(BaseModel):
    """Validated location query parameters."""
    
    name: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    @field_validator("name")
    @classmethod
    def sanitize_location_name(cls, v: Optional[str]) -> Optional[str]:
        """Sanitize location name to prevent injection."""
        if v is None:
            return v
        
        v = v.strip()
        
        if not LOCATION_PATTERN.match(v):
            raise ValueError("Invalid characters in location name")
        
        for pattern in SQL_INJECTION_PATTERNS:
            if re.search(pattern, v, re.IGNORECASE):
                logger.warning(f"Potential injection attempt: {v[:50]}")
                raise ValueError("Invalid location name")
        
        return v


class CoordinateValidator:
    """Validator for geographic coordinates."""

    @staticmethod
    def validate_latitude(lat: float) -> float:
        """Validate latitude value."""
        if not -90 <= lat <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return round(lat, 6)

    @staticmethod
    def validate_longitude(lon: float) -> float:
        """Validate longitude value."""
        if not -180 <= lon <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return round(lon, 6)

    @classmethod
    def validate_coordinates(cls, lat: float, lon: float) -> tuple[float, float]:
        """Validate coordinate pair."""
        return cls.validate_latitude(lat), cls.validate_longitude(lon)


def sanitize_string(value: str, max_length: int = 255) -> str:
    """General string sanitization."""
    if not isinstance(value, str):
        raise TypeError("Expected string value")
    
    value = value.strip()[:max_length]
    value = re.sub(r"[<>"';&]", "", value)
    
    return value
