import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_cud_service import app
from backend.app.models.incidence import Incidence
from backend.app.logic.universal_controller_sqlserver import UniversalController

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    incidencia = Incidence(ID=9999, IDTicket=1, Descripcion="Prueba de incidencia", Tipo="Error", IDUnidad="1")
    controller.add(incidencia)
    yield incidencia
    controller.delete(incidencia)

def test_crear_incidencia():
    """
    Prueba para crear una incidencia.
    """
    incidencia = Incidence(ID=9998, IDTicket=1, Descripcion="Nueva incidencia", Tipo="Advertencia", IDUnidad="1")
    try:
        response = client.post("/incidences/create", data=incidencia.to_dict(), headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Incidencia creada exitosamente."
    finally:
        controller.delete(incidencia)

def test_actualizar_incidencia(setup_and_teardown):
    """
    Prueba para actualizar una incidencia existente.
    """
    incidencia = setup_and_teardown
    incidencia.Descripcion = "Incidencia actualizada"
    incidencia.Tipo = "Advertencia"
    response = client.post(
        "/incidences/update",
        data=incidencia.to_dict(),
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Incidencia actualizada exitosamente."

<<<<<<< HEAD
# def test_eliminar_incidencia(setup_and_teardown):
#     """
#     Prueba para eliminar una incidencia existente.
#     """
#     incidencia = setup_and_teardown
#     response = client.post("/incidences/delete", data={"ID": incidencia.ID}, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Incidencia eliminada exitosamente."
=======
def test_eliminar_incidencia(setup_and_teardown):
    """
    Prueba para eliminar una incidencia existente.
    """
    incidencia = setup_and_teardown
    response = client.post("/incidences/delete", data={"ID": incidencia.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Incidencia eliminada exitosamente."
>>>>>>> d4828dc (incidence and transport fix)
