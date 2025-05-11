import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.type_movement_service.type_movement_query_service import app as typemovement_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.type_movement import TypeMovementOut

test_app = FastAPI()
test_app.include_router(typemovement_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
def test_consultar_page():
    """Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    response = client.get("/typemovement/consultar",headers=headers)
    assert response.status_code == 200

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los tipos de transporte."""
    response = client.get("/typemovement/typemovements/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 2
    assert data[0]["type"] == "Recarga"

def test_get_by_id():
    """Prueba que la ruta '/user/{id}' devuelve el usuario correcto."""
    response = client.get("/typemovement/2", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["type"] == "Recarga"

def test_get_by_id_not_found():
    """Prueba que la ruta '/user/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/typemovement/999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == "Tipo de Movimientos no encontrado"

