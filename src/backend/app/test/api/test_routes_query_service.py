import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_query_service import app
from backend.app.models.routes import Route
from backend.app.logic.universal_controller_sql import UniversalController

client = TestClient(app)
controller = UniversalController()

@pytest.fixture(autouse=True)
def setup():
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_listar_rutas():
    controller.add(Route(id=1, idhorario=10, name="Ruta 1"))
    response = client.get("/routes/")
    assert response.status_code == 200
    assert "Ruta 1" in response.text

def test_detalle_ruta_existente():
    controller.add(Route(id=1, idhorario=10, name="Ruta 1"))
    response = client.get("/routes/1")
    assert response.status_code == 200
    assert "Ruta 1" in response.text

def test_detalle_ruta_no_existente():
    response = client.get("/routes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ruta no encontrada" 