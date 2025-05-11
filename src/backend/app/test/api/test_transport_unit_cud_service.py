import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.transport_unit_cud_service import app
from backend.app.models.transport import Transport
from backend.app.logic.universal_controller_sqlserver import UniversalController

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    transport = Transport(Ubicacion="Estación Central", Capacidad=50, IDRuta=1, IDTipo=2)
    # Crear la unidad de prueba
    controller.add(transport)
    created_transport = controller.read_all(Transport)[-1]  # Obtener el último registro creado
    yield created_transport

    # Eliminar la unidad de prueba
    controller.delete(created_transport)

def test_crear_unidad():
    """
    Prueba para crear una unidad de transporte.
    """
    transport = Transport(Ubicacion="Estación Norte", Capacidad=40, IDRuta=1, IDTipo=2)
    try:
        response = client.post("/transports/create", data=transport.to_dict())
        assert response.status_code == 200
        assert response.json()["message"] == "Unidad de transporte creada exitosamente."
    finally:
        # Teardown: Eliminar la unidad creada
        created_transport = controller.read_all(Transport)[-1]  # Obtener el último registro creado
        controller.delete(created_transport)

def test_actualizar_unidad(setup_and_teardown):
    """
    Prueba para actualizar una unidad de transporte existente.
    """
    transport = setup_and_teardown
    response = client.post("/transports/update", data={"ID": transport.ID, "Ubicacion": "Estación Sur", "Capacidad": 60, "IDRuta": 2, "IDTipo": 3})
    assert response.status_code == 200
    assert response.json()["message"] == "Unidad de transporte actualizada exitosamente."

def test_eliminar_unidad(setup_and_teardown):
    """
    Prueba para eliminar una unidad de transporte existente.
    """
    transport = setup_and_teardown
    response = client.post("/transports/delete", data={"ID": transport.ID})
    assert response.status_code == 200
    assert response.json()["message"] == "Unidad de transporte eliminada exitosamente."
