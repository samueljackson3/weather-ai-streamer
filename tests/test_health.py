import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.config import settings


@pytest.mark.asyncio
async def test_health():
    """Test the /health endpoint returns 200 with correct response body."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    
    # Assert status code is 200
    assert response.status_code == 200
    
    # Assert response body has the expected structure
    data = response.json()
    assert "status" in data
    assert "version" in data
    
    # Assert the values are what we expect
    assert data["status"] == "ok"
    assert data["version"] == settings.app_version
