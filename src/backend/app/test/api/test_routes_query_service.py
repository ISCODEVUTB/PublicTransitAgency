import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_query_service import app
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

def test_listar_rutas(setup_and_teardown):
    """
    Prueba para listar todas las rutas.
    """
    response = client.get("/routes/")
    assert response.status_code == 200
    assert "Ruta de prueba" in response.text

def test_detalle_ruta_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una ruta existente.
    """
    route = setup_and_teardown
    response = client.get(f"/routes/{route.ID}")
    assert response.status_code == 200
    assert "Ruta de prueba" in response.text

