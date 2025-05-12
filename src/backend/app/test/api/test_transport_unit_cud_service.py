# import pytest
# from fastapi.testclient import TestClient
# from backend.app.api.routes.transport_unit_cud_service import app
# from backend.app.models.transport import UnidadTransporte
# from backend.app.logic.universal_controller_sqlserver import UniversalController
# from backend.app.core.conf import headers

# client = TestClient(app)
# controller = UniversalController()

<<<<<<< HEAD
# @pytest.fixture
# def setup_and_teardown():
#     """
#     Fixture para configurar y limpiar los datos de prueba.
#     """
#     unidad = UnidadTransporte(Ubicacion="Depósito Central", Capacidad=50, IDRuta=1, IDTipo=1, ID="TEST_UNIT")
#     controller.add(unidad)
#     yield unidad
#     controller.delete(unidad)
=======
<<<<<<< HEAD
@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    unidad = UnidadTransporte(Ubicacion="Depósito Central", Capacidad=50, IDRuta=1, IDTipo=2, ID="TEST_UNIT")
    controller.add(unidad)
    yield unidad
    controller.delete(unidad)
>>>>>>> 52e45f5 (Corrections on test)

# def test_crear_unidad_transporte():
#     """
#     Prueba para crear una unidad de transporte.
#     """
#     unidad = UnidadTransporte(Ubicacion="Depósito Secundario", Capacidad=30, IDRuta=1, IDTipo=1, ID="NEW_UNIT")
#     try:
#         response = client.post("/transport_units/create", data=unidad.to_dict(), headers=headers)
#         assert response.status_code == 200
#         assert response.json()["message"] == "Unidad de transporte creada exitosamente."
#     finally:
#         controller.delete(unidad)

<<<<<<< HEAD
# def test_actualizar_unidad_transporte(setup_and_teardown):
#     """
#     Prueba para actualizar una unidad de transporte existente.
#     """
#     unidad = setup_and_teardown
#     unidad.Ubicacion = "Depósito Actualizado"
#     response = client.post("/transport_units/update", data=unidad.to_dict(), headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Unidad de transporte actualizada exitosamente."

=======
def test_crear_unidad_transporte():
    """
    Prueba para crear una unidad de transporte.
    """
    unidad = UnidadTransporte(Ubicacion="Depósito Secundario", Capacidad=30, IDRuta=1, IDTipo=2, ID="NEW_UNIT")
    try:
        response = client.post("/transport_units/create", data=unidad.to_dict(), headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Unidad de transporte creada exitosamente."
    finally:
        controller.delete(unidad)
=======
# @pytest.fixture
# def setup_and_teardown():
#     """
#     Fixture para configurar y limpiar los datos de prueba.
#     """
#     unidad = UnidadTransporte(Ubicacion="Depósito Central", Capacidad=50, IDRuta=1, IDTipo=1, ID="TEST_UNIT")
#     controller.add(unidad)
#     yield unidad
#     controller.delete(unidad)

# def test_crear_unidad_transporte():
#     """
#     Prueba para crear una unidad de transporte.
#     """
#     unidad = UnidadTransporte(Ubicacion="Depósito Secundario", Capacidad=30, IDRuta=1, IDTipo=1, ID="NEW_UNIT")
#     try:
#         response = client.post("/transport_units/create", data=unidad.to_dict(), headers=headers)
#         assert response.status_code == 200
#         assert response.json()["message"] == "Unidad de transporte creada exitosamente."
#     finally:
#         controller.delete(unidad)
>>>>>>> a8980fb (Corrections on test)

# def test_actualizar_unidad_transporte(setup_and_teardown):
#     """
#     Prueba para actualizar una unidad de transporte existente.
#     """
#     unidad = setup_and_teardown
#     unidad.Ubicacion = "Depósito Actualizado"
#     response = client.post("/transport_units/update", data=unidad.to_dict(), headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Unidad de transporte actualizada exitosamente."

<<<<<<< HEAD
def test_eliminar_unidad_transporte(setup_and_teardown):
    """
    Prueba para eliminar una unidad de transporte existente.
    """
    unidad = setup_and_teardown
    response = client.post("/transport_units/delete", data={"ID": unidad.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Unidad de transporte eliminada exitosamente."
=======
>>>>>>> 52e45f5 (Corrections on test)
# def test_eliminar_unidad_transporte(setup_and_teardown):
#     """
#     Prueba para eliminar una unidad de transporte existente.
#     """
#     unidad = setup_and_teardown
#     response = client.post("/transport_units/delete", data={"ID": unidad.ID}, headers=headers)
#     assert response.status_code == 200
<<<<<<< HEAD
#     assert response.json()["message"] == "Unidad de transporte eliminada exitosamente."
=======
#     assert response.json()["message"] == "Unidad de transporte eliminada exitosamente."
>>>>>>> a8980fb (Corrections on test)
>>>>>>> 52e45f5 (Corrections on test)
