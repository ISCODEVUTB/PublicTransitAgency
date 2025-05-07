from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_cud_service import app as incidences_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence
from fastapi import FastAPI
from unittest.mock import patch
import pytest
from backend.app.core.conf import headers  # Import headers for authentication

# Setup the test application
app_for_test = FastAPI()
app_for_test.include_router(incidences_router)
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

def test_crear_incidencia():
    """Test that the '/incidences/create' route creates a new incidence."""
    response = client.post("/incidences/create", data={
        "id": 1,
        "idticket": 1,
        "description": "Test",
        "type": "Tipo1",
        "idunit": 1
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Incidencia creada exitosamente."

def test_actualizar_incidencia():
    """Test that the '/incidences/update' route updates an existing incidence."""
    controller.add(Incidence(id=1, idticket=1, description="Old", type="Tipo1", idunit=1))
    response = client.post("/incidences/update", data={
        "id": 1,
        "idticket": 1,
        "description": "Updated",
        "type": "Tipo2",
        "idunit": 2
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Incidencia actualizada exitosamente."

def test_actualizar_incidencia_no_existente():
    """Test that the '/incidences/update' route returns 404 for a non-existent incidence."""
    response = client.post("/incidences/update", data={
        "ID": 999,
        "IDTicket": 1,
        "Descripcion": "Non-existent",
        "Tipo": "Tipo1",
        "IDUnidad": 1
    }, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"

def test_eliminar_incidencia():
    """Test that the '/incidences/delete' route deletes an existing incidence."""
    controller.add(Incidence(ID=1, IDTicket=1, Descripcion="Test", Tipo="Tipo1", IDUnidad=1))
    response = client.post("/incidences/delete", data={"ID": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Incidencia eliminada exitosamente."

def test_eliminar_incidencia_no_existente():
    """Test that the '/incidences/delete' route returns 404 for a non-existent incidence."""
    response = client.post("/incidences/delete", data={"ID": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"
