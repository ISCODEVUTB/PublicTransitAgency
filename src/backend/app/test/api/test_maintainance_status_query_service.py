import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app
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


def test_listar_estados():
    """
    Prueba para listar todos los estados de mantenimiento.
    """
    controller.add(MaintainanceStatus(id=1, type="Preventivo", status="Activo"))
    controller.add(MaintainanceStatus(id=2, type="Correctivo", status="Inactivo"))

    response = client.get("/maintainance_status/", headers=headers)

    assert response.status_code == 200
    assert "Preventivo" in response.text
    assert "Activo" in response.text
    assert "Correctivo" in response.text
    assert "Inactivo" in response.text


def test_listar_sin_estados():
    """
    Prueba para listar cuando no hay estados registrados.
    """
    response = client.get("/maintainance_status/", headers=headers)

    assert response.status_code == 200
    #assert "No hay estados registrados." in response.text


def test_detalle_estado_existente():
    """
    Prueba para obtener el detalle de un estado existente.
    """
    controller.add(MaintainanceStatus(id=1, type="Preventivo", status="Activo"))

    response = client.get("/maintainance_status/1", headers=headers)

    assert response.status_code == 200
    assert "Preventivo" in response.text
    assert "Activo" in response.text


