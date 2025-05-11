# import pytest
# from fastapi.testclient import TestClient
# from backend.app.api.routes.rutaparada_query_service import app
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

# def test_listar_rutaparada(setup_and_teardown):
#     """
#     Prueba para listar todas las relaciones Ruta-Parada.
#     """
#     response = client.get("/rutaparada/")
#     assert response.status_code == 200

# def test_detalle_rutaparada_existente(setup_and_teardown):
#     """
#     Prueba para obtener el detalle de una relación Ruta-Parada existente.
#     """
#     rutaparada = setup_and_teardown
#     response = client.get(f"/rutaparada/{rutaparada.IDParada}")
#     assert response.status_code == 200

# def test_detalle_rutaparada_no_existente():
#     """
#     Prueba para obtener el detalle de una relación Ruta-Parada que no existe.
#     """
#     response = client.get("/rutaparada/99999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Relación Ruta-Parada no encontrada"