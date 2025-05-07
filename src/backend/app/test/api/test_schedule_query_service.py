import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_query_service import app
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

def test_listar_horarios():
    """
    Prueba listar horarios cuando hay datos disponibles.
    """
    controller.add(Schedule(id=1, llegada="08:00:00", salida="10:00:00"))
    response = client.get("/schedules/", headers=headers)
    assert response.status_code == 200
    assert "08:00:00" in response.text
    assert "10:00:00" in response.text
    assert "1" in response.text

def test_listar_sin_horarios():
    """
    Prueba listar horarios cuando la tabla está vacía.
    """
    response = client.get("/schedules/", headers=headers)
    assert response.status_code == 200
    assert "No hay horarios disponibles." in response.text  # Suponiendo que el HTML lo indica.

def test_detalle_horario_existente():
    """
    Prueba obtener detalles de un horario existente.
    """
    controller.add(Schedule(id=1, llegada="08:00:00", salida="10:00:00"))
    response = client.get("/schedules/1", headers=headers)
    assert response.status_code == 200
    #assert "08:00:00" in response.text
    #assert "10:00:00" in response.text
    assert "1" in response.text

