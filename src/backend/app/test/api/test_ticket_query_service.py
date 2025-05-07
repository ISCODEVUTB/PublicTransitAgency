import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_query_service import app as tickets_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(tickets_router)
client = TestClient(app_for_test)
controller = UniversalController()

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Limpia las tablas antes y después de cada prueba"""
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_listar_tickets():
    """Prueba listar todos los tickets"""
    # Crear un ticket en la base de datos
    controller.add(Ticket(id=1, estadoincidencia="Abierto"))
    controller.add(Ticket(id=2, estadoincidencia="Cerrado"))

    # Hacer la llamada al endpoint
    response = client.get("/tickets/", headers=headers)
    assert response.status_code == 200
    assert "Abierto" in response.text
    assert "Cerrado" in response.text

def test_listar_sin_tickets():
    """Prueba listar cuando no hay tickets"""
    # No crear ningún dato previo
    response = client.get("/tickets/", headers=headers)

    # Validar que se muestra el mensaje esperado
    assert response.status_code == 200
    assert "No se encontraron tickets." in response.text

def test_detalle_ticket_existente():
    """Prueba ver detalles de un ticket existente"""
    # Agregar un ticket
    controller.add(Ticket(id=1, estadoincidencia="Abierto"))

    # Consultar los detalles
    response = client.get("/tickets/1", headers=headers)

    assert response.status_code == 200
    assert "Abierto" in response.text

t no encontrado"