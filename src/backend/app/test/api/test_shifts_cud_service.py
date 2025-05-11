from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_cud_service import app
from backend.app.models.shift import Shift
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

def test_crear_turno():
    """
    Prueba para crear un turno.
    """
    turno_id = 9999
    turno_prueba = Shift(ID=turno_id, TipoTurno="Nocturno Test")

    # Asegurarse de que el turno no exista antes de crearlo
    existing_turno = controller.get_by_id(Shift, turno_id)
    if existing_turno:
        controller.delete(existing_turno)

    try:
        response = client.post("/shifts/create", data={"id": turno_id, "TipoTurno": "Nocturno Test"}, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Turno creado exitosamente."
    finally:
        # Teardown: Eliminar el turno creado
        controller.delete(turno_prueba)

def test_actualizar_turno():
    """
    Prueba para actualizar un turno existente.
    """
    turno_id = 9999
    turno_prueba = Shift(ID=turno_id, TipoTurno="Original")

    # Asegurarse de que el turno no exista antes de crearlo
    existing_turno = controller.get_by_id(Shift, turno_id)
    if existing_turno:
        controller.delete(existing_turno)

    # Crear el turno de prueba
    controller.add(turno_prueba)

    try:
        # Actualizar el turno
        response = client.post("/shifts/update", data={"id": turno_id, "TipoTurno": "Vespertino Test"}, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Turno actualizado exitosamente."

        # Verificar que el turno fue actualizado
        turno_actualizado = controller.get_by_id(Shift, turno_id)
        assert turno_actualizado.TipoTurno == "Vespertino Test"
    finally:
        # Teardown: Eliminar el turno actualizado
        controller.delete(turno_prueba)

def test_eliminar_turno():
    """
    Prueba para eliminar un turno existente.
    """
    turno_id = 9999
    turno_prueba = Shift(ID=turno_id, TipoTurno="Eliminar Test")
    controller.add(turno_prueba)

    response = client.post("/shifts/delete", data={"id": turno_id}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Turno eliminado exitosamente."

