import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_cud_service import app
from backend.app.models.schedule import Schedule
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture(scope="function", autouse=True)
def limpiar_tabla():
    """Limpia las tablas antes y después de cada prueba."""
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_crear_horario():
    response = client.post("/schedules/create", data={
        "id": 1,
        "llegada": "08:00:00",
        "salida": "10:00:00"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario creado exitosamente."
    assert response.json()["data"]["id"] == 1
    assert response.json()["data"]["llegada"] == "08:00:00"
    assert response.json()["data"]["salida"] == "10:00:00"

def test_actualizar_horario():
    controller.add(Schedule(id=1, llegada="08:00:00", salida="10:00:00"))
    response = client.post("/schedules/update", data={
        "id": 1,
        "llegada": "09:00:00",
        "salida": "11:00:00"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario actualizado exitosamente."
    assert response.json()["data"]["llegada"] == "09:00:00"
    assert response.json()["data"]["salida"] == "11:00:00"

def test_eliminar_horario():
    controller.add(Schedule(id=1, llegada="08:00:00", salida="10:00:00"))
    response = client.post("/schedules/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario eliminado exitosamente."
