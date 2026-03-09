import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    """Tests the health endpoint returns 200 OK."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_validate_xml_success():
    """Tests a successful XML validation."""
    # Create a dummy valid XML content
    # Note: Ensure this matches what your standard.xsd expects!
    valid_xml = b"<root><data>Test</data></root>"
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        files = {"file": ("test.xml", valid_xml, "text/xml")}
        response = await ac.post("/api/v1/validate", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "total_errors" in data

@pytest.mark.asyncio
async def test_validate_xml_no_file():
    """Tests that the API rejects a request with no file."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/validate") # No file attached
    
    # FastAPI returns 422 Unprocessable Entity for missing required fields
    assert response.status_code == 422