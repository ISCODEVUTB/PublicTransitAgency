import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_query_service import app
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

def test_listar_horarios(setup_and_teardown):
    """
    Prueba para listar todos los horarios.
    """
    response = client.get("/schedules/", headers=headers)
    assert response.status_code == 200

def test_detalle_horario_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de un horario existente.
    """
    schedule = setup_and_teardown
    response = client.get(f"/schedules/{schedule.ID}", headers=headers)
    assert response.status_code == 200


