"""
Pydantic models define the shape and validation rules for request/response data.

Think of them like Rails strong parameters + a typed object that validates at
the boundary between the HTTP world (untyped JSON) and your Python code (typed).
"""

from pydantic import BaseModel
from enum import Enum


class Units(str, Enum):
    """Valid temperature units. FastAPI validates query params against this."""
    metric = "metric"
    imperial = "imperial"
    standard = "standard"


class HealthResponse(BaseModel):
    """
    Response shape for the health check endpoint.
    
    Pydantic will:
    - Validate that incoming data has exactly these fields
    - Coerce types if possible (e.g., "123" → 123 if field is int)
    - Raise ValueError if data doesn't match
    - Auto-generate JSON schema for OpenAPI /docs
    - Serialize to JSON with this exact structure
    """
    status: str
    version: str


class WeatherResponse(BaseModel):
    """
    Response shape for weather data. Maps OpenWeather API response to our schema.
    
    Fields correspond to what we extract from OpenWeatherMap API:
    https://openweathermap.org/current
    """
    city: str
    country: str
    temperature: float
    feels_like: float
    description: str
    humidity: int
    wind_speed: float
    units: Units
