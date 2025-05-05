import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_query_service import app as shifts_router
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.models.shift import Shift
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(shifts_router)
client = TestClient(app_for_test)
controller = UniversalController()

@pytest.fixture(autouse=True)
def setup_and_teardown():
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_listar_turnos():
    controller.add(Shift(id=999, tipoturno="Diurno"))
    response = client.get("/shifts/", headers=headers)
    assert response.status_code == 200
    assert "Diurno" in response.text

def test_detalle_turno_existente():
    controller.add(Shift(id=999, tipoturno="Diurno"))
    response = client.get("/shifts/999", headers=headers)
    assert response.status_code == 200
    assert "Diurno" in response.text

def test_detalle_turno_no_existente():
    response = client.get("/shifts/998", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Turno no encontrado"