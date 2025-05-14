import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app
from backend.app.models.incidence import Incidence
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    incidencia = Incidence(ID=9998, IDTicket=1, Descripcion="Nueva incidencia", Tipo="Advertencia", IDUnidad="1")
    controller.add(incidencia)
    yield incidencia
    controller.delete(incidencia)

def test_listar_incidencias(setup_and_teardown):
    """
    Prueba para listar todas las incidencias.
    """
    response = client.get("/incidences/", headers=headers)
    assert response.status_code == 200

def test_detalle_incidencia_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una incidencia existente.
    """
    incidencia = setup_and_teardown
    response = client.get(f"/incidences/{incidencia.ID}", headers=headers)
    assert response.status_code == 200

