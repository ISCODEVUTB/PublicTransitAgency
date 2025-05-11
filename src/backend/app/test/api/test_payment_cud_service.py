# import pytest
# from fastapi.testclient import TestClient
# from backend.app.api.routes.payment_cud_service import app
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

# def test_crear_pago():
#     """
#     Prueba para crear un pago.
#     """
#     pago = Payment(IDMovimiento=9998, IDPago=1, IDTarjeta=1, IDTransporte=1)
#     try:
#         response = client.post("/payments/create", data=pago.to_dict())
#         assert response.status_code == 200
#         assert response.json()["message"] == "Pago creado exitosamente."
#     finally:
#         # Teardown: Eliminar el pago creado
#         controller.delete(pago)

# def test_eliminar_pago(setup_and_teardown):
#     """
#     Prueba para eliminar un pago existente.
#     """
#     pago = setup_and_teardown
#     response = client.post("/payments/delete", data={"IDMovimiento": pago.IDMovimiento})
#     assert response.status_code == 200
#     assert response.json()["message"] == "Pago eliminado exitosamente."

#     # Verificar que el pago haya sido eliminado
#     deleted_pago = controller.get_by_id(Payment, pago.IDMovimiento)
#     assert deleted_pago is None