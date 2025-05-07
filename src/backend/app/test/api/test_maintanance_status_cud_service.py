import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_cud_service import app
from backend.app.models.maintainance_status import MaintainanceStatus
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

def test_crear_estado():
    """
    Prueba para crear un estado de mantenimiento.
    """
    response = client.post("/maintainance_status/create", data={
        "id": 1,
        "type": "Preventivo",
        "status": "Activo"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento creado exitosamente."

def test_actualizar_estado():
    """
    Prueba para actualizar un estado de mantenimiento existente.
    """
    controller.add(MaintainanceStatus(id=1, type="Preventivo", status="Activo"))
    response = client.post("/maintainance_status/update", data={
        "id": 1,
        "type": "Correctivo",
        "status": "Inactivo"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento actualizado exitosamente."

def test_eliminar_estado():
    """
    Prueba para eliminar un estado de mantenimiento existente.
    """
    controller.add(MaintainanceStatus(id=1, type="Preventivo", status="Activo"))
    response = client.post("/maintainance_status/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento eliminado exitosamente."

def test_eliminar_estado_no_existente():
    """
    Prueba para eliminar un estado de mantenimiento que no existe.
    """
    response = client.post("/maintainance_status/delete", data={"id": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Estado de mantenimiento no encontrado"