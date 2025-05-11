import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app as maintainance_status_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(maintainance_status_router)
client = TestClient(app_for_test)
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

def test_listar_estados(setup_and_teardown):
    """
    Prueba para listar todos los estados de mantenimiento.
    """
    response = client.get("/maintainance_status/", headers=headers)
    assert response.status_code == 200

def test_detalle_estado_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de un estado de mantenimiento existente.
    """
    estado_prueba = setup_and_teardown
    response = client.get(f"/maintainance_status/{estado_prueba.ID}", headers=headers)
    assert response.status_code == 200

def test_detalle_estado_no_existente():
    """
    Prueba para obtener el detalle de un estado de mantenimiento que no existe.
    """
    response = client.get("/maintainance_status/99999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Estado de mantenimiento no encontrado"


