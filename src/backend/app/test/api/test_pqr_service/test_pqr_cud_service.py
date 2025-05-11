from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.api.routes.pqr_service import pqr_cud_service  # Importamos el módulo, no solo el `app`
from backend.app.core.conf import headers
from backend.app.models.pqr import PQRCreate, PQROut

# Crear instancia del controlador que se usará en pruebas
test_controller = pqr_cud_service.controller
# Limpiar base de datos
"""def setup_function():
    test_controller.clear_tables()

def teardown_function():
    test_controller.clear_tables()"""

# App de prueba
app_for_test = FastAPI()
app_for_test.include_router(pqr_cud_service.app)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_pqr():
    response = client.post("/pqr/create", data={"id": 44, "iduser": 100001, "type":"none","description":"aaa",
                                                 "fecha":"29-08-2024","codigogenerado":"PQR44"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 44
    assert response.json()["data"]["description"] == "aaa"

def test_update_pqr_existing():
    response = client.post("/pqr/update", data={"id": 44, "iduser": 100002, "type":"none", "description":"aaa",
                                                "fecha":"29-08-2024","codigogenerado":"PQR2"}, 
                           headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["type"] == "none"

def test_update_pqr_not_found():
    response = client.post("/pqr/update", data={"id": 999, "iduser": 100001, "type":"bb", "description":"aaa",
                                                "fecha":"29-08-2024","codigogenerado":"PQR1"}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "PQR not found"

def test_delete_pqr_existing():
    response = client.post("/pqr/delete", data={"id": 44}, headers=headers)
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

def test_delete_pqr_not_found():
    response = client.post("/pqr/delete", data={"id": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "PQR not found"

def test_index_create_form():
    response = client.get("/pqr/crear", headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/pqr/actualizar", headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/pqr/eliminar", headers=headers)
    assert response.status_code == 200
