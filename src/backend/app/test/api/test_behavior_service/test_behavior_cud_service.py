from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.api.routes import behavior_cud_service  # Importamos el módulo, no solo el `app`
from backend.app.core.conf import headers
from backend.app.models.behavior import BehaviorCreate, BehaviorOut

# Crear instancia del controlador que se usará en pruebas
test_controller = behavior_cud_service.controller

# App de prueba
app_for_test = FastAPI()
app_for_test.include_router(behavior_cud_service.app)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_behavior():
    response = client.post("/behavior/create", data={"id": 44, "iduser": 99, "cantidadrutas": 2,"horastrabajadas":12,
                                                "observaciones":"none",
                                                 "fecha":"29-08-2024"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 44
    assert response.json()["data"]["observaciones"] == "none"

def test_update_behavior_existing():
    response = client.post("/behavior/update", data={"id": 44, "iduser": 99, "cantidadrutas": 3,"horastrabajadas":12,
                                                "observaciones":"milei",
                                                 "fecha":"29-08-2024"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["observaciones"] == "milei"
    assert response.json()["data"]["cantidadrutas"] == 3

def test_update_behavior_not_found():
    response = client.post("/behavior/update",data={"id": 999, "iduser": 99, "cantidadrutas": 3,"horastrabajadas":12,
                                                "observaciones":"milei",
                                                 "fecha":"29-08-2024"}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Behavior not found"

def test_delete_behavior_existing():
    response = client.post("/behavior/delete", data={"id": 44}, headers=headers)
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

def test_delete_behavior_not_found():
    response = client.post("/behavior/delete", data={"id": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Behavior not found"

def test_index_create_form():
    response = client.get("/behavior/crear", headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/behavior/actualizar", headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/behavior/eliminar", headers=headers)
    assert response.status_code == 200
