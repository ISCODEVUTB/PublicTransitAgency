import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app
from backend.app.models.incidence import Incidence
from backend.app.logic.universal_controller_sqlserver import UniversalController

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    incidencia = Incidence(ID=9999, IDTicket=1, Descripcion="Prueba de incidencia", Tipo="Error", IDUnidad=1)
    # Asegurarse de que la incidencia no exista antes de crearla
    existing_incidencia = controller.get_by_id(Incidence, incidencia.ID)
    if existing_incidencia:
        controller.delete(existing_incidencia)

    # Crear la incidencia de prueba
    controller.add(incidencia)
    yield incidencia

    # Eliminar la incidencia de prueba
    controller.delete(incidencia)

def test_listar_incidencias(setup_and_teardown):
    """
    Prueba para listar todas las incidencias.
    """
    response = client.get("/incidences/")
    assert response.status_code == 200

def test_detalle_incidencia_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una incidencia existente.
    """
    incidencia = setup_and_teardown
    response = client.get(f"/incidences/{incidencia.ID}")
    assert response.status_code == 200

