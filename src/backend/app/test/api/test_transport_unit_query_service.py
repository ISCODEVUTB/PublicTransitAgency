# import pytest
# from fastapi.testclient import TestClient
# from backend.app.api.routes.transport_unit_query_service import app
# from backend.app.models.transport import UnidadTransporte
# from backend.app.logic.universal_controller_sqlserver import UniversalController
# from backend.app.core.conf import headers

# client = TestClient(app)
# controller = UniversalController()

# @pytest.fixture
# def setup_and_teardown():
#     """
#     Fixture para configurar y limpiar los datos de prueba.
#     """
#     unidad = UnidadTransporte(Ubicacion="Depósito Central", Capacidad=50, IDRuta=1, IDTipo=1, ID="TEST_UNIT")
#     controller.add(unidad)
#     yield unidad
#     controller.delete(unidad)

# def test_listar_unidades_transporte(setup_and_teardown):
#     """
#     Prueba para listar todas las unidades de transporte.
#     """
#     response = client.get("/transport_units/", headers=headers)
#     assert response.status_code == 200

# def test_detalle_unidad_transporte_existente(setup_and_teardown):
#     """
#     Prueba para obtener el detalle de una unidad de transporte existente.
#     """
#     unidad = setup_and_teardown
#     response = client.get(f"/transport_units/{unidad.ID}", headers=headers)
#     assert response.status_code == 200
#     assert "Depósito Central" in response.text