import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.type_transport_service.type_transport_query_service import app as typetransport_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.type_transport import TypeTransportOut

test_app = FastAPI()
test_app.include_router(typetransport_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
def test_consultar_page():
    response = client.get("/typetransport/consultar",headers=headers)
    assert response.status_code == 200

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los tipos de transporte."""
    response = client.get("/typetransport/typetransports/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6

def test_get_by_id():
    """Prueba que la ruta '/user/{id}' devuelve el usuario correcto."""
    response = client.get("/typetransport/6", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 6
    assert data["type"] == "bus"

def test_get_by_id_not_found():
    """Prueba que la ruta '/user/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/typetransport/999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == "Tipo de Transporte no encontrado"

