import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_cud_service import app
from backend.app.models.routes import Route
from backend.app.logic.universal_controller_sql import UniversalController

client = TestClient(app)
controller = UniversalController()

@pytest.fixture(autouse=True)
def setup():
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_crear_ruta():
    response = client.post("/routes/create", data={"id": 1, "idhorario": 10, "name": "Ruta 1"})
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta creada exitosamente."

def test_actualizar_ruta():
    controller.add(Route(id=1, idhorario=10, name="Ruta 1"))
    response = client.post("/routes/update", data={"id": 1, "idhorario": 20, "name": "Ruta Actualizada"})
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta actualizada exitosamente."

def test_eliminar_ruta():
    controller.add(Route(id=1, idhorario=10, name="Ruta 1"))
    response = client.post("/routes/delete", data={"id": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta eliminada exitosamente."