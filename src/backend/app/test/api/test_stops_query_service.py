import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.app.api.routes.stops_query_service import app as paradas_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.stops import Parada
from backend.app.core.conf import headers

app_for_test = FastAPI()
app_for_test.include_router(paradas_router)
client = TestClient(app_for_test)
controller = UniversalController()


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Limpia las tablas antes y después de cada prueba"""
    controller.clear_tables()
    yield
    controller.clear_tables()


def test_listar_paradas():
    """Prueba listar todas las paradas"""
    # Crear algunas paradas de prueba
    controller.add(Parada(id=1, name="Parada 1", ubication="Ubicación 1"))
    controller.add(Parada(id=2, name="Parada 2", ubication="Ubicación 2"))

    response = client.get("/paradas/", headers=headers)

    assert response.status_code == 200
    assert "Parada 1" in response.text
    assert "Ubicación 1" in response.text
    assert "Parada 2" in response.text
    assert "Ubicación 2" in response.text


def test_listar_sin_paradas():
    """Prueba listar cuando no hay paradas"""
    response = client.get("/paradas/", headers=headers)

    assert response.status_code == 200
    assert "No hay paradas registradas." in response.text


def test_detalle_parada_existente():
    """Prueba obtener detalles de una parada existente"""
    # Crear una parada de prueba
    controller.add(Parada(id=1, name="Parada Test", ubication="Ubicación Test"))

    response = client.get("/paradas/1", headers=headers)

    assert response.status_code == 200
    assert "Parada Test" in response.text
    assert "Ubicación Test" in response.text


