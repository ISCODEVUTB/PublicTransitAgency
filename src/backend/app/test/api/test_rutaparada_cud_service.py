# import pytest
# from fastapi.testclient import TestClient
# from backend.app.api.routes.rutaparada_cud_service import app
# from backend.app.models.rutaparada import RutaParada
# from backend.app.logic.universal_controller_sqlserver import UniversalController

# client = TestClient(app)
# controller = UniversalController()

# @pytest.fixture
# def setup_and_teardown():
#     """
#     Fixture para configurar y limpiar los datos de prueba.
#     """
#     rutaparada = RutaParada(IDParada=9999, IDRuta=8888)
#     # Asegurarse de que la relación no exista antes de crearla
#     existing_rutaparada = controller.get_by_id(RutaParada, rutaparada.IDParada)
#     if existing_rutaparada:
#         controller.delete(existing_rutaparada)

#     # Crear la relación de prueba
#     controller.add(rutaparada)
#     yield rutaparada

#     # Eliminar la relación de prueba
#     controller.delete(rutaparada)

# def test_crear_rutaparada():
#     """
#     Prueba para crear una relación Ruta-Parada.
#     """
#     rutaparada = RutaParada(IDParada=9998, IDRuta=8887)
#     try:
#         response = client.post("/rutaparada/create", data={"IDParada": rutaparada.IDParada, "IDRuta": rutaparada.IDRuta})
#         assert response.status_code == 200
#         assert response.json()["message"] == "Relación Ruta-Parada creada exitosamente."
#     finally:
#         # Teardown: Eliminar la relación creada
#         controller.delete(rutaparada)

# def test_actualizar_rutaparada(setup_and_teardown):
#     """
#     Prueba para actualizar una relación Ruta-Parada existente.
#     """
#     rutaparada = setup_and_teardown
#     response = client.post("/rutaparada/update", data={"IDParada": rutaparada.IDParada, "IDRuta": 7777})
#     assert response.status_code == 200
#     assert response.json()["message"] == "Relación Ruta-Parada actualizada exitosamente."

#     # Verificar que la relación fue actualizada
#     updated_rutaparada = controller.get_by_id(RutaParada, rutaparada.IDParada)
#     assert updated_rutaparada.IDRuta == 7777

# def test_eliminar_rutaparada(setup_and_teardown):
#     """
#     Prueba para eliminar una relación Ruta-Parada existente.
#     """
#     rutaparada = setup_and_teardown
#     response = client.post("/rutaparada/delete", data={"IDParada": rutaparada.IDParada})
#     assert response.status_code == 200
#     assert response.json()["message"] == "Relación Ruta-Parada eliminada exitosamente."

#     # Verificar que la relación fue eliminada
#     deleted_rutaparada = controller.get_by_id(RutaParada, rutaparada.IDParada)
#     assert deleted_rutaparada is None