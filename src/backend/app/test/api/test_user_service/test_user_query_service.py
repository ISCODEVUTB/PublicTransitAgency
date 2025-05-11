import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.user_service.user_query_service import app as user_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.user import UserOut

test_app = FastAPI()
test_app.include_router(user_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
def test_consultar_page():
    response = client.get("/user/consultar",headers=headers)
    assert response.status_code == 200

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los tipos de transporte."""
    response = client.get("/user/users", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ID"] == 42
    assert data[0]["Identificacion"] == 99

def test_get_by_id():
    """Prueba que la ruta '/user/{id}' devuelve el usuario correcto."""
    response = client.get("/user/42", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["Nombre"] == "aa"
    assert data["Apellido"] == "bb"

def test_get_by_id_not_found():
    """Prueba que la ruta '/user/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/user/999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == "Usuario no encontrado"

