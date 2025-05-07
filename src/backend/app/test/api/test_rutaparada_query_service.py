import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.rutaparada_query_service import app
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

def test_listar_rutaparadas():
    """
    Prueba para listar todas las relaciones entre rutas y paradas.
    """
    controller.add(RutaParada(id=1, idruta=2, idparada=3))
    controller.add(RutaParada(id=2, idruta=4, idparada=5))

    response = client.get("/rutaparada/", headers=headers)

    assert response.status_code == 200
    assert "2" in response.text  # idruta del primer registro
    assert "3" in response.text  # idparada del primer registro
    assert "4" in response.text  # idruta del segundo registro
    assert "5" in response.text  # idparada del segundo registro

def test_listar_sin_rutaparadas():
    """
    Prueba para listar cuando no hay relaciones entre rutas y paradas registradas.
    """
    response = client.get("/rutaparada/", headers=headers)

    assert response.status_code == 200

def test_detalle_rutaparada_existente():
    """
    Prueba para obtener el detalle de una relación entre ruta y parada existente.
    """
    controller.add(RutaParada(id=1, idruta=2, idparada=3))

    response = client.get("/rutaparada/1", headers=headers)

    assert response.status_code == 200
    assert "2" in response.text  # idruta
    assert "3" in response.text  # idparada