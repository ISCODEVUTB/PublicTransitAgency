import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.app.api.routes.transport_unit_cud_service import app as transport_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.transport import Transport
from backend.app.core.conf import headers  # Import headers for authentication
from unittest.mock import patch

# Setup the test application
app_for_test = FastAPI()
app_for_test.include_router(transport_router)
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

def test_crear_unidad():
    """Test that the '/transports/create' route creates a new transport unit."""
    response = client.post("/transports/create", data={
        "id": "1",
        "idtype": "1",
        "status": "bien",
        "ubication": "Garage",
        "capacity": "50",
        "idruta": "1"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Unidad creada exitosamente."

def test_actualizar_unidad():
    """Test that the '/transports/update' route updates an existing transport unit."""
    controller.add(Transport(id="1", idtype=1, status="bien", ubication="Garage", capacity=50, idruta=1))
    response = client.post("/transports/update", data={
        "id": "1",
        "idtype": "1",
        "status": "mantenimiento",
        "ubication": "Garage",
        "capacity": "50",
        "idruta": "1"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Unidad actualizada exitosamente."

def test_eliminar_unidad():
    """Test that the '/transports/delete' route deletes an existing transport unit."""
    controller.add(Transport(id="1", idtype=1, status="bien", ubication="Garage", capacity=50, idruta=1))
    response = client.post("/transports/delete", data={"id": "1"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Unidad eliminada exitosamente."
