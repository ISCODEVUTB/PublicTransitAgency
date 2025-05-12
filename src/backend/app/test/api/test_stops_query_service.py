import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_query_service import app
from backend.app.models.stops import Parada
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    parada = Parada(ID=9999, Nombre="Parada de Prueba", Ubicacion="Ubicación de Prueba")
    # Asegurarse de que la parada no exista antes de crearla
    existing_parada = controller.get_by_id(Parada, parada.ID)
    if existing_parada:
        controller.delete(existing_parada)

    # Crear la parada de prueba
    controller.add(parada)
    yield parada

    # Eliminar la parada de prueba
    controller.delete(parada)

def test_listar_paradas(setup_and_teardown):
    """
    Prueba para listar todas las paradas.
    """
    response = client.get("/stops/", headers=headers)
    assert response.status_code == 200


def test_detalle_parada_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una parada existente.
    """
    parada = setup_and_teardown
    response = client.get(f"/stops/{parada.ID}", headers=headers)
    assert response.status_code == 200





