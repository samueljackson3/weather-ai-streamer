"""
FastAPI app for Session 2.
Step A: Minimal app with health check.
Step B: Pydantic models for type-safe responses.
Step C: Configuration from environment.
Step D: Weather endpoint (hardcoded for now).
Step E: Real API integration with httpx.
"""

from fastapi import FastAPI, Query, HTTPException
import httpx
from src.config import settings
from src.models import HealthResponse, WeatherResponse, Units

# Create the FastAPI application instance
app = FastAPI(
    title="Weather AI Streamer",
    version=settings.app_version,
    description="Learn async Python by building a weather AI app"
)


# Business logic: fetch weather from OpenWeather API
# This is separate from route handlers so it's testable in isolation
async def fetch_weather(
    city: str,
    units: Units,
    client: httpx.AsyncClient,
) -> WeatherResponse:
    """
    Fetch weather data from OpenWeatherMap API.
    
    This is business logic, not a route handler.
    Separated so:
    1. It's testable without spinning up a full FastAPI app
    2. Session 3 can reuse it (pass different client for Ollama integration)
    3. It's clear what data flows in/out
    
    Args:
        city: City name (e.g., "Seattle")
        units: Temperature units (metric, imperial, standard)
        client: httpx.AsyncClient for making HTTP requests
        
    Returns:
        WeatherResponse with parsed weather data
        
    Raises:
        HTTPException(404): City not found
        HTTPException(401): Invalid API key
        HTTPException(503): API unavailable
    """
    
    # Build the API request
    params = {
        "q": city,
        "units": units.value,
        "appid": settings.openweather_api_key,
    }
    
    try:
        # Make the request
        response = await client.get(
            f"{settings.openweather_base_url}/weather",
            params=params,
            timeout=10.0,
        )
        
        # Handle error status codes
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"City '{city}' not found. Please check the spelling and try again."
            )
        elif response.status_code == 401:
            raise HTTPException(
                status_code=401,
                detail="Invalid OpenWeather API key. Check your configuration."
            )
        elif response.status_code >= 500:
            raise HTTPException(
                status_code=503,
                detail="Weather service is temporarily unavailable. Please try again later."
            )
        
        response.raise_for_status()  # Raise for other 4xx/5xx errors
        
        # Parse the response
        data = response.json()
        
        # Extract fields and create WeatherResponse
        # (Pydantic will validate the types)
        return WeatherResponse(
            city=data["name"],
            country=data["sys"]["country"],
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            description=data["weather"][0]["description"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"],
            units=units,
        )
    
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=503,
            detail="Request to weather service timed out. The service may be slow or unavailable."
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Network error: Unable to reach weather service."
        )
    except KeyError as e:
        # OpenWeather response missing expected field
        raise HTTPException(
            status_code=503,
            detail=f"Unexpected weather service response. Missing field: {e.args[0]}"
        )


# Define a route: GET /health
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        version=settings.app_version
    )


# Define a route: GET /weather/{city}
@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(
    city: str,
    units: Units = Query(default=Units.metric)
) -> WeatherResponse:
    """
    Get weather for a city.
    
    Path parameters:
    - city: City name (e.g., "Seattle"). Must be 2-50 characters.
    
    Query parameters:
    - units: Temperature units (metric, imperial, standard). Default: metric
    
    Errors:
    - 400: City name is empty or invalid
    - 404: City not found in OpenWeather database
    - 401: Invalid or missing API key
    - 503: Weather service unavailable or timeout
    """
    
    # Validate city name
    city_clean = city.strip()
    if not city_clean or len(city_clean) < 2:
        raise HTTPException(
            status_code=400,
            detail="City name must be at least 2 characters"
        )
    if len(city_clean) > 50:
        raise HTTPException(
            status_code=400,
            detail="City name must be 50 characters or less"
        )
    
    # Make the API call
    async with httpx.AsyncClient(verify=settings.verify_ssl) as client:
        return await fetch_weather(city_clean, units, client)


# This is all we need to start!
# To run: uvicorn src.main:app --reload
