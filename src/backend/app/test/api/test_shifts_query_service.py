import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_query_service import app as shifts_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.shift import Shift
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(shifts_router)
client = TestClient(app_for_test)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    # Setup: Crear un turno de prueba
    turno_prueba = Shift(ID=99999, TipoTurno="Prueba")
    controller.add(turno_prueba)
    yield turno_prueba
    # Teardown: Eliminar el turno de prueba
    controller.delete(turno_prueba)

def test_listar_turnos(setup_and_teardown):
    response = client.get("/shifts/", headers=headers)
    assert response.status_code == 200

def test_detalle_turno_existente(setup_and_teardown):
    turno_prueba = setup_and_teardown
    response = client.get(f"/shifts/{turno_prueba.ID}", headers=headers)
    assert response.status_code == 200