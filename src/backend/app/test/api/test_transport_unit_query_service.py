import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.transport_unit_query_service import app as transports_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.transport import Transport
from backend.app.core.conf import headers  # Import headers for authentication
from fastapi import FastAPI
from unittest.mock import patch

# Setup the test application
app_for_test = FastAPI()
app_for_test.include_router(transports_router)
client = TestClient(app_for_test)
controller = UniversalController()

# Mock authentication globally
@pytest.fixture(autouse=True)
def mock_get_current_user():
    with patch("backend.app.core.auth.get_current_user") as mock_user:
        mock_user.return_value = {"user_id": 1, "scopes": ["system", "administrador", "supervisor"]}
        yield mock_user

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_listar_unidades():
    """Test that the '/transports/' route lists all transport units."""
    controller.add(Transport(id="1", idtype=1, status="bien", ubication="Garage", capacity=50, idruta=1))
    response = client.get("/transports/", headers=headers)
    assert response.status_code == 200
    assert "bien" in response.text

def test_detalle_unidad_existente():
    """Test that the '/transports/{id}' route retrieves an existing transport unit."""
    controller.add(Transport(id="1", idtype=1, status="bien", ubication="Garage", capacity=50, idruta=1))
    response = client.get("/transports/1", headers=headers)
    assert response.status_code == 200
    assert "bien" in response.text

def test_detalle_unidad_no_existente():
    """Test that the '/transports/{id}' route returns 404 for a non-existent transport unit."""
    response = client.get("/transports/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Unidad de transporte no encontrada"
