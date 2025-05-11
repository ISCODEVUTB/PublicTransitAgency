# import pytest
# from fastapi.testclient import TestClient
# from backend.app.api.routes.payment_query_service import app
# from backend.app.models.payment import Payment
# from backend.app.logic.universal_controller_sqlserver import UniversalController

# client = TestClient(app)
# controller = UniversalController()

# @pytest.fixture
# def setup_and_teardown():
#     """
#     Fixture para configurar y limpiar los datos de prueba.
#     """
#     pago = Payment(IDMovimiento=9999, IDPago=1, IDTarjeta=1, IDTransporte=1)
#     # Asegurarse de que el pago no exista antes de crearlo
#     existing_pago = controller.get_by_id(Payment, pago.IDMovimiento)
#     if existing_pago:
#         controller.delete(existing_pago)

#     # Crear el pago de prueba
#     controller.add(pago)
#     yield pago

#     # Eliminar el pago de prueba
#     controller.delete(pago)

# def test_listar_pagos(setup_and_teardown):
#     """
#     Prueba para listar todos los pagos.
#     """
#     response = client.get("/payments/")
#     assert response.status_code == 200

# def test_detalle_pago_existente(setup_and_teardown):
#     """
#     Prueba para obtener el detalle de un pago existente.
#     """
#     pago = setup_and_teardown
#     response = client.get(f"/payments/{pago.IDMovimiento}")
#     assert response.status_code == 200

# def test_detalle_pago_no_existente():
#     """
#     Prueba para obtener el detalle de un pago que no existe.
#     """
#     response = client.get("/payments/99999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Pago no encontrado"