import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.rutaparada_cud_service import app
from backend.app.models.rutaparada import RutaParada
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture(autouse=True)
def limpiar_bd():
    """
    Limpia la base de datos antes y después de cada prueba.
    """
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_crear_rutaparada():
    """
    Prueba para crear una relación entre ruta y parada.
    """
    response = client.post("/rutaparada/create", data={
        "id": 1,
        "idruta": 2,
        "idparada": 3
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Relación ruta-parada creada exitosamente."

def test_actualizar_rutaparada():
    """
    Prueba para actualizar una relación entre ruta y parada existente.
    """
    controller.add(RutaParada(id=1, idruta=2, idparada=3))
    response = client.post("/rutaparada/update", data={
        "id": 1,
        "idruta": 4,
        "idparada": 5
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Relación ruta-parada actualizada exitosamente."

def test_eliminar_rutaparada():
    """
    Prueba para eliminar una relación entre ruta y parada existente.
    """
    controller.add(RutaParada(id=1, idruta=2, idparada=3))
    response = client.post("/rutaparada/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Relación ruta-parada eliminada exitosamente."

def test_eliminar_rutaparada_no_existente():
    """
    Prueba para eliminar una relación entre ruta y parada que no existe.
    """
    response = client.post("/rutaparada/delete", data={"id": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Relación ruta-parada no encontrada"