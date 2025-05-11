import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_cud_service import app
from backend.app.models.routes import Route
from backend.app.logic.universal_controller_sqlserver import UniversalController

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    route = Route(ID=9999, IDHorario=1, Nombre="Ruta de prueba")
    # Asegurarse de que la ruta no exista antes de crearla
    existing_route = controller.get_by_id(Route, route.ID)
    if existing_route:
        controller.delete(existing_route)

    # Crear la ruta de prueba
    controller.add(route)
    yield route

    # Eliminar la ruta de prueba
    controller.delete(route)

def test_crear_ruta():
    """
    Prueba para crear una ruta.
    """
    route = Route(ID=9998, IDHorario=1, Nombre="Nueva ruta")
    try:
        response = client.post("/routes/create", data=route.to_dict())
        assert response.status_code == 200
        assert response.json()["message"] == "Ruta creada exitosamente."
    finally:
        # Teardown: Eliminar la ruta creada
        controller.delete(route)

def test_actualizar_ruta(setup_and_teardown):
    """
    Prueba para actualizar una ruta existente.
    """
    route = setup_and_teardown
    updated_data = {
        "ID": route.ID,
        "IDHorario": 2,
        "Nombre": "Ruta actualizada"
    }
    response = client.post("/routes/update", data=updated_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta actualizada exitosamente."

    # Verificar que los datos se hayan actualizado
    updated_route = controller.get_by_id(Route, route.ID)
    assert updated_route.IDHorario == 2
    assert updated_route.Nombre == "Ruta actualizada"

def test_eliminar_ruta(setup_and_teardown):
    """
    Prueba para eliminar una ruta existente.
    """
    route = setup_and_teardown
    response = client.post("/routes/delete", data={"ID": route.ID})
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta eliminada exitosamente."

    # Verificar que la ruta haya sido eliminada
    deleted_route = controller.get_by_id(Route, route.ID)
    assert deleted_route is None