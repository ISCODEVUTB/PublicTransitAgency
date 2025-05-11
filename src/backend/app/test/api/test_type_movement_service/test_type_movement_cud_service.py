from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.api.routes.type_movement_service.type_movement_cud_service import app as typemovement_router  # Importa bien
from backend.app.core.conf import headers   

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(typemovement_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Cliente de prueba
client = TestClient(app_for_test)

def test_create_user():
    response = client.post("/typemovement/create", data={"id":1,"type":"ingreso_sistema"},headers=headers)
    assert response.status_code == 200

def test_update_user_existing():
    response = client.post("/typemovement/update", data={"id":1,"type":"recarga"},headers=headers)
    assert response.status_code == 200

def test_update_user_not_found():
    response = client.post("/typemovement/update", data={"id": 99, "type":"ninguno"},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "TypeMovement not found"

def test_delete_user_existing():
    response = client.post("/typemovement/delete", data={"id": 1},headers=headers)
    assert response.status_code == 200

def test_delete_user_not_found():
    response = client.post("/typemovement/delete", data={"id": 999},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "TypeMovement not found"

def test_index_create_form():
    response = client.get("/typemovement/crear",headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/typemovement/actualizar",headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/typemovement/eliminar",headers=headers)
    assert response.status_code == 200
