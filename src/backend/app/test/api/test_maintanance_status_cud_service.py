import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_cud_service import app
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    estado_prueba = MaintainanceStatus(ID=9999, TipoEstado="Prueba")
    # Asegurarse de que el estado no exista antes de crearlo
    existing_estado = controller.get_by_id(MaintainanceStatus, estado_prueba.ID)
    if existing_estado:
        controller.delete(existing_estado)

    # Crear el estado de prueba
    controller.add(estado_prueba)
    yield estado_prueba

    # Eliminar el estado de prueba
    controller.delete(estado_prueba)

def test_crear_estado():
    """
    Prueba para crear un estado de mantenimiento.
    """
    estado_prueba = MaintainanceStatus(ID=9998, TipoEstado="Nuevo Estado")
    try:
        response = client.post("/maintainance_status/create", data={"id": estado_prueba.ID, "TipoEstado": estado_prueba.TipoEstado}, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Estado de mantenimiento creado exitosamente."
    finally:
        # Teardown: Eliminar el estado creado
        controller.delete(estado_prueba)

def test_actualizar_estado(setup_and_teardown):
    """
    Prueba para actualizar un estado de mantenimiento existente.
    """
    estado_prueba = setup_and_teardown
    response = client.post("/maintainance_status/update", data={"id": estado_prueba.ID, "TipoEstado": "Estado Actualizado"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento actualizado exitosamente."

    # Verificar que el estado fue actualizado
    estado_actualizado = controller.get_by_id(MaintainanceStatus, estado_prueba.ID)
    assert estado_actualizado.TipoEstado == "Estado Actualizado"

def test_eliminar_estado(setup_and_teardown):
    """
    Prueba para eliminar un estado de mantenimiento existente.
    """
    estado_prueba = setup_and_teardown
    response = client.post("/maintainance_status/delete", data={"id": estado_prueba.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento eliminado exitosamente."

    # Verificar que el estado fue eliminado
    estado_eliminado = controller.get_by_id(MaintainanceStatus, estado_prueba.ID)
    assert estado_eliminado is None


