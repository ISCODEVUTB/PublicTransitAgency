import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_query_service import app as shifts_router
from backend.app.logic.universal_controller_sql import UniversalController  # Usamos el controlador correcto
from backend.app.models.shift import Shift
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(shifts_router)
client = TestClient(app_for_test)
controller = UniversalController()  # Controller usado en el microservicio


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Limpia las tablas antes y después de cada prueba
    controller.clear_tables()
    yield
    controller.clear_tables()


def test_listar_turnos():
    """
    Test que valida la obtención de la lista de turnos.
    """
    # Agregamos un turno a la base de datos
    controller.add(Shift(id=1, tipoturno="Diurno"))

    # Realizamos un GET para listar los turnos
    response = client.get("/shifts/", headers=headers)

    # Verificamos el código de respuesta
    assert response.status_code == 200
    # Verificamos que el turno agregado aparece en la respuesta
    assert "Diurno" in response.text


def test_detalle_turno_existente():
    """
    Test que valida el detalle de un turno existente.
    """
    # Agregamos un turno a la base de datos
    controller.add(Shift(id=1, tipoturno="Diurno"))

    # Realizamos un GET para obtener el detalle del turno por ID
    response = client.get("/shifts/1", headers=headers)

    # Verificamos el código de respuesta
    assert response.status_code == 200
    # Verificamos que el detalle incluye el turno agregado
    assert "Diurno" in response.text


def test_detalle_turno_no_existente():
    """
    Test que valida el manejo del caso de un turno no existente.
    """
    # Realizamos un GET para un ID que no existe
    response = client.get("/shifts/999", headers=headers)

    # Verificamos que el código de respuesta es 404
    assert response.status_code == 404
    # Verificamos que se muestra el mensaje de error apropiado
    assert response.json()["detail"] == "Turno no encontrado"


def test_listar_turnos_sin_datos():
    """
    Test que valida la obtención de una lista vacía de turnos.
    """
    # Realizamos un GET para listar turnos sin haber agregado datos
    response = client.get("/shifts/", headers=headers)

    # Verificamos que el código de respuesta es 200
    assert response.status_code == 200
    # Verificamos que no hay turnos en la respuesta
    assert "Diurno" not in response.text