import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_cud_service import app
from backend.app.models.stops import Parada
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers  # Importar los headers de configuración

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    parada_prueba = Parada(ID=9999, Nombre="Parada de prueba", Ubicacion="Ubicación de prueba")
    # Asegurarse de que la parada no exista antes de crearla
    existing_parada = controller.get_by_id(Parada, parada_prueba.ID)
    if existing_parada:
        controller.delete(existing_parada)

    # Crear la parada de prueba
    controller.add(parada_prueba)
    yield parada_prueba

    # Eliminar la parada de prueba
    controller.delete(parada_prueba)

def test_crear_parada():
    """
    Prueba para crear una parada.
    """
    parada_prueba = Parada(ID=9998, Nombre="Nueva Parada", Ubicacion="Ubicación Nueva")
    try:
        response = client.post(
            "/stops/create",
            data={"id": parada_prueba.ID, "Nombre": parada_prueba.Nombre, "Ubicacion": parada_prueba.Ubicacion},
            headers=headers  # Añadir los headers
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Parada creada exitosamente."
    finally:
        # Teardown: Eliminar la parada creada
        controller.delete(parada_prueba)

def test_actualizar_parada(setup_and_teardown):
    """
    Prueba para actualizar una parada existente.
    """
    parada_prueba = setup_and_teardown
    response = client.post(
        "/stops/update",
        data={"id": parada_prueba.ID, "Nombre": "Parada Actualizada", "Ubicacion": "Ubicación Actualizada"},
        headers=headers  # Añadir los headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Parada actualizada exitosamente."

    # Verificar que la parada fue actualizada
    parada_actualizada = controller.get_by_id(Parada, parada_prueba.ID)
    assert parada_actualizada.Nombre == "Parada Actualizada"
    assert parada_actualizada.Ubicacion == "Ubicación Actualizada"

def test_eliminar_parada(setup_and_teardown):
    """
    Prueba para eliminar una parada existente.
    """
    parada_prueba = setup_and_teardown
    response = client.post(
        "/stops/delete",
        data={"id": parada_prueba.ID},
        headers=headers  # Añadir los headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Parada eliminada exitosamente."

    # Verificar que la parada fue eliminada
    parada_eliminada = controller.get_by_id(Parada, parada_prueba.ID)
    assert parada_eliminada is None

def test_renderizar_formulario_crear():
    """
    Prueba para verificar que el formulario de creación se renderiza correctamente.
    """
    response = client.get("/stops/create", headers=headers)  # Añadir los headers
    assert response.status_code == 200

def test_renderizar_formulario_actualizar():
    """
    Prueba para verificar que el formulario de actualización se renderiza correctamente.
    """
    response = client.get("/stops/update", headers=headers)  # Añadir los headers
    assert response.status_code == 200

def test_renderizar_formulario_eliminar():
    """
    Prueba para verificar que el formulario de eliminación se renderiza correctamente.
    """
    response = client.get("/stops/delete", headers=headers)  # Añadir los headers
    assert response.status_code == 200


