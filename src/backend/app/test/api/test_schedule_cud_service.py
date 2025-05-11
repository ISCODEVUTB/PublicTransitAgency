import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_cud_service import app
from backend.app.models.schedule import Schedule
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    schedule = Schedule(ID=9999, Llegada="08:00:00", Salida="17:00:00")
    # Asegurarse de que el horario no exista antes de crearlo
    existing_schedule = controller.get_by_id(Schedule, schedule.ID)
    if existing_schedule:
        controller.delete(existing_schedule)

    # Crear el horario de prueba
    controller.add(schedule)
    yield schedule

    # Eliminar el horario de prueba
    controller.delete(schedule)

def test_crear_horario():
    """
    Prueba para crear un horario.
    """
    schedule = Schedule(ID=9998, Llegada="09:00:00", Salida="18:00:00")
    try:
        response = client.post("/schedules/create", data={"id": schedule.ID, "Llegada": schedule.Llegada, "Salida": schedule.Salida}, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Horario creado exitosamente."
    finally:
        # Teardown: Eliminar el horario creado
        controller.delete(schedule)

def test_actualizar_horario(setup_and_teardown):
    """
    Prueba para actualizar un horario existente.
    """
    schedule = setup_and_teardown
    response = client.post("/schedules/update", data={"id": schedule.ID, "Llegada": "10:00:00", "Salida": "19:00:00"})
    assert response.status_code == 200
    assert response.json()["message"] == "Horario actualizado exitosamente."

    # Verificar que el horario fue actualizado
    updated_schedule = controller.get_by_id(Schedule, schedule.ID)

    # Normalizar los valores para comparar solo hora, minutos y segundos
    assert updated_schedule.Llegada.split(".")[0] == "10:00:00"
    assert updated_schedule.Salida.split(".")[0] == "19:00:00"

def test_eliminar_horario(setup_and_teardown):
    """
    Prueba para eliminar un horario existente.
    """
    schedule = setup_and_teardown
    response = client.post("/schedules/delete", data={"id": schedule.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario eliminado exitosamente."

    # Verificar que el horario fue eliminado
    deleted_schedule = controller.get_by_id(Schedule, schedule.ID)
    assert deleted_schedule is None


