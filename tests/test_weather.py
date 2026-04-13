import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport, Response
from src.main import app, get_http_client


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_mock_client(status_code: int, json_body: dict) -> AsyncMock:
    """
    Build a fake httpx.AsyncClient whose .get() returns a controlled response.

    We need AsyncMock because `client.get(...)` is awaited in `fetch_weather`.
    We use MagicMock for the response itself because Response attributes
    (status_code, .json()) are accessed synchronously after the await.
    """
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_body
    # raise_for_status() is called on non-error paths — make it a no-op
    mock_response.raise_for_status = MagicMock(return_value=None)

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    return mock_client


def override_http_client(mock_client: AsyncMock):
    """
    Return a FastAPI dependency override that yields our fake client.

    app.dependency_overrides replaces `get_http_client` for the duration
    of a test without touching the real httpx library at all.
    """
    async def _override():
        yield mock_client
    return _override


# ---------------------------------------------------------------------------
# The real OpenWeather JSON shape (trimmed to what fetch_weather reads)
# ---------------------------------------------------------------------------

TOKYO_PAYLOAD = {
    "name": "Tokyo",
    "sys": {"country": "JP"},
    "main": {"temp": 20.0, "feels_like": 19.0, "humidity": 80},
    "weather": [{"description": "clear sky"}],
    "wind": {"speed": 5.0},
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_weather_success():
    """Happy path: OpenWeather returns 200 with valid data."""
    mock_client = make_mock_client(200, TOKYO_PAYLOAD)
    app.dependency_overrides[get_http_client] = override_http_client(mock_client)

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/weather/Tokyo")
    finally:
        # Always clean up overrides so other tests aren't affected
        app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Tokyo"
    assert data["country"] == "JP"
    assert data["temperature"] == 20.0
    assert data["description"] == "clear sky"


@pytest.mark.asyncio
async def test_weather_city_not_found():
    """OpenWeather returns 404 → our app should also return 404."""
    mock_client = make_mock_client(404, {"message": "city not found"})
    app.dependency_overrides[get_http_client] = override_http_client(mock_client)

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/weather/FakeCityThatDoesNotExist")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_weather_invalid_api_key():
    """OpenWeather returns 401 → our app should return 401."""
    mock_client = make_mock_client(401, {"message": "Invalid API key"})
    app.dependency_overrides[get_http_client] = override_http_client(mock_client)

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/weather/Tokyo")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
    assert "api key" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_weather_city_name_too_short():
    """City name < 2 chars hits our validation before any HTTP call."""
    # No mock needed — the route rejects it before calling fetch_weather
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/weather/X")

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_weather_service_unavailable():
    """OpenWeather returns 500 → our app returns 503."""
    mock_client = make_mock_client(500, {"message": "internal error"})
    app.dependency_overrides[get_http_client] = override_http_client(mock_client)

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/weather/Tokyo")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
