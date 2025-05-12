import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_cud_service import app
from backend.app.models.stops import Parada
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    parada = Parada(ID=9999, Nombre="Parada de Prueba", Ubicacion="Ubicación de Prueba")
    # Asegurarse de que la parada no exista antes de crearla
    existing_parada = controller.get_by_id(Parada, parada.ID)
    if existing_parada:
        controller.delete(existing_parada)

    # Crear la parada de prueba
    controller.add(parada)
    yield parada

    # Eliminar la parada de prueba
    controller.delete(parada)

def test_crear_parada():
    """
    Prueba para crear una nueva parada.
    """
    parada_data = {"ID": 10000, "Nombre": "Nueva Parada", "Ubicacion": "Nueva Ubicación"}
    response = client.post("/stops/create", data=parada_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parada creada exitosamente."

    # Verificar que la parada se haya creado en la base de datos
    parada = controller.get_by_id(Parada, parada_data["ID"])
    assert parada is not None
    assert parada.Nombre == parada_data["Nombre"]
    assert parada.Ubicacion == parada_data["Ubicacion"]

    # Limpiar la base de datos
    controller.delete(parada)

def test_actualizar_parada(setup_and_teardown):
    """
    Prueba para actualizar una parada existente.
    """
    parada = setup_and_teardown
    updated_data = {"ID": parada.ID, "Nombre": "Parada Actualizada", "Ubicacion": "Ubicación Actualizada"}
    response = client.post("/stops/update", data=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parada actualizada exitosamente."

    # Verificar que la parada se haya actualizado en la base de datos
    updated_parada = controller.get_by_id(Parada, updated_data["ID"])
    assert updated_parada is not None
    assert updated_parada.Nombre == updated_data["Nombre"]
    assert updated_parada.Ubicacion == updated_data["Ubicacion"]

def test_eliminar_parada(setup_and_teardown):
    """
    Prueba para eliminar una parada existente.
    """
    parada = setup_and_teardown
    response = client.post("/stops/delete", data={"ID": parada.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parada eliminada exitosamente."

    # Verificar que la parada ya no exista en la base de datos
    deleted_parada = controller.get_by_id(Parada, parada.ID)
    assert deleted_parada is None


