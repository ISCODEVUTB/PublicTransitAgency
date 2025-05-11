import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_cud_service import app
from backend.app.models.incidence import Incidence
from backend.app.logic.universal_controller_sqlserver import UniversalController

client = TestClient(app)
controller = UniversalController()

<<<<<<< HEAD
@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    incidencia = Incidence(ID=9999, IDTicket=1, Descripcion="Prueba de incidencia", Tipo="Error", IDUnidad=1)
    # Asegurarse de que la incidencia no exista antes de crearla
    existing_incidencia = controller.get_by_id(Incidence, incidencia.ID)
    if existing_incidencia:
        controller.delete(existing_incidencia)

    # Crear la incidencia de prueba
    controller.add(incidencia)
    yield incidencia

    # Eliminar la incidencia de prueba
    controller.delete(incidencia)

def test_crear_incidencia():
    """
    Prueba para crear una incidencia.
    """
    incidencia = Incidence(ID=9998, IDTicket=1, Descripcion="Nueva incidencia", Tipo="Advertencia", IDUnidad=1)
    try:
        response = client.post("/incidences/create", data=incidencia.to_dict())
        assert response.status_code == 200
        assert response.json()["message"] == "Incidencia creada exitosamente."
    finally:
        # Teardown: Eliminar la incidencia creada
        controller.delete(incidencia)

def test_actualizar_incidencia(setup_and_teardown):
    """
    Prueba para actualizar una incidencia existente.
    """
    incidencia = setup_and_teardown
    updated_data = {
        "ID": incidencia.ID,
        "IDTicket": 1,
        "Descripcion": "Incidencia actualizada",
        "Tipo": "Advertencia",
        "IDUnidad": 1
    }
    response = client.post("/incidences/update", data=updated_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Incidencia actualizada exitosamente."

    # Verificar que los datos se hayan actualizado
    updated_incidencia = controller.get_by_id(Incidence, incidencia.ID)
    assert updated_incidencia.Descripcion == "Incidencia actualizada"
    assert updated_incidencia.Tipo == "Advertencia"

def test_eliminar_incidencia(setup_and_teardown):
    """
    Prueba para eliminar una incidencia existente.
    """
    incidencia = setup_and_teardown
    response = client.post("/incidences/delete", data={"ID": incidencia.ID})
    assert response.status_code == 200
    assert response.json()["message"] == "Incidencia eliminada exitosamente."

    # Verificar que la incidencia haya sido eliminada
    deleted_incidencia = controller.get_by_id(Incidence, incidencia.ID)
    assert deleted_incidencia is None

=======
# @pytest.fixture
# def setup_and_teardown():
#     """
#     Fixture para configurar y limpiar los datos de prueba.
#     """
#     incidencia = Incidence(ID=9999, IDTicket=1, Descripcion="Prueba de incidencia", Tipo="Error", IDUnidad="TEST_UNIT")
#     controller.add(incidencia)
#     yield incidencia
#     controller.delete(incidencia)

# def test_crear_incidencia():
#     """
#     Prueba para crear una incidencia.
#     """
#     incidencia = Incidence(ID=9998, IDTicket=1, Descripcion="Nueva incidencia", Tipo="Advertencia", IDUnidad="NEW_UNIT")
#     try:
#         response = client.post("/incidences/create", data=incidencia.to_dict(), headers=headers)
#         assert response.status_code == 200
#         assert response.json()["message"] == "Incidencia creada exitosamente."
#     finally:
#         controller.delete(incidencia)

# def test_actualizar_incidencia(setup_and_teardown):
#     """
#     Prueba para actualizar una incidencia existente.
#     """
#     incidencia = setup_and_teardown
#     incidencia.Descripcion = "Incidencia actualizada"
#     incidencia.Tipo = "Advertencia"
#     response = client.post(
#         "/incidences/update",
#         data=incidencia.to_dict(),
#         headers=headers
#     )
#     assert response.status_code == 200
#     assert response.json()["message"] == "Incidencia actualizada exitosamente."

# def test_eliminar_incidencia(setup_and_teardown):
#     """
#     Prueba para eliminar una incidencia existente.
#     """
#     incidencia = setup_and_teardown
#     response = client.post("/incidences/delete", data={"ID": incidencia.ID}, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Incidencia eliminada exitosamente."
>>>>>>> 50e6569 (changes because of rubiano)
