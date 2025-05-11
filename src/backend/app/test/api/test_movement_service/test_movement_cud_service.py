from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.api.routes.movement_cud_service import app as movement_router  # Importa bien
from backend.app.core.conf import headers
# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(movement_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Cliente de prueba
client = TestClient(app_for_test)

def test_create_user():
    response = client.post("/movement/create", data={"ID":1,"IDTipoMovimiento":2,"Monto":100},headers=headers)
    assert response.status_code == 200

def test_update_user_existing():
    response = client.post("/movement/update", data={"ID":1,"IDTipoMovimiento":2,"Monto":90000},headers=headers)
    assert response.status_code == 200

def test_update_user_not_found():
    response = client.post("/movement/update", data={"ID":99,"IDTipoMovimiento":5,"Monto":2200},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Movement not found"

def test_delete_user_existing():
    response = client.post("/movement/delete", data={"ID": 1},headers=headers)
    assert response.status_code == 200

def test_delete_user_not_found():
    response = client.post("/movement/delete", data={"ID": 999},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Movement not found"

def test_index_create_form():
    response = client.get("/movement/crear",headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/movement/actualizar",headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/movement/eliminar",headers=headers)
    assert response.status_code == 200
