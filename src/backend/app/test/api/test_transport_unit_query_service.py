import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.transport_unit_query_service import app
<<<<<<< HEAD
from backend.app.models.transport import Transport
from backend.app.logic.universal_controller_sqlserver import UniversalController
=======
from backend.app.models.transport import UnidadTransporte
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
>>>>>>> 50e6569 (changes because of rubiano)

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
<<<<<<< HEAD
    transport = Transport(Ubicacion="Estación Central", Capacidad=50, IDRuta=1, IDTipo=2)
    # Crear la unidad de prueba
    controller.add(transport)
    created_transport = controller.read_all(Transport)[-1]  # Obtener el último registro creado
    yield created_transport

    # Eliminar la unidad de prueba
    controller.delete(created_transport)

def test_listar_unidades(setup_and_teardown):
    """
    Prueba para listar todas las unidades de transporte.
    """
    response = client.get("/transports/")
    assert response.status_code == 200

def test_detalle_unidad_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una unidad de transporte existente.
    """
    transport = setup_and_teardown
    response = client.get(f"/transports/{transport.ID}")
    assert response.status_code == 200

def test_detalle_unidad_no_existente():
    """
    Prueba para obtener el detalle de una unidad de transporte que no existe.
    """
    response = client.get("/transports/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Unidad de transporte no encontrada"
=======
    unidad = UnidadTransporte(Ubicacion="Depósito Central", Capacidad=50, IDRuta=1, IDTipo=1, ID="TEST_UNIT")
    controller.add(unidad)
    yield unidad
    controller.delete(unidad)

def test_listar_unidades_transporte(setup_and_teardown):
    """
    Prueba para listar todas las unidades de transporte.
    """
    response = client.get("/transport_units/", headers=headers)
    assert response.status_code == 200

def test_detalle_unidad_transporte_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una unidad de transporte existente.
    """
    unidad = setup_and_teardown
    response = client.get(f"/transport_units/{unidad.ID}", headers=headers)
    assert response.status_code == 200
    assert "Depósito Central" in response.text

>>>>>>> 50e6569 (changes because of rubiano)
