from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.api.routes.asistance_service import asistance_cud_service  # Importamos el módulo, no solo el `app`
from backend.app.core.conf import headers
from backend.app.models.asistance import AsistanceCreate, AsistanceOut

# Crear instancia del controlador que se usará en pruebas
test_controller = asistance_cud_service.controller

# App de prueba
app_for_test = FastAPI()
app_for_test.include_router(asistance_cud_service.app)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_asistance():
    response = client.post("/asistance/create", data={"id": 44, "iduser": 99, "horainicio":"00:00","horafinal":"24:00",
                                                 "fecha":"29-08-2024"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 44
    assert response.json()["data"]["horafinal"] == "24:00"

def test_update_asistance_existing():
    response = client.post("/asistance/update", data={"id": 44, "iduser": 99, "horainicio":"12:00","horafinal":"10:00",
                                                 "fecha":"29-08-2024"}, 
                           headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["horainicio"] == "12:00"
    assert response.json()["data"]["horafinal"] == "10:00"

def test_update_asistance_not_found():
    response = client.post("/asistance/update",data={"id": 999, "iduser": 99, "horainicio":"00:00","horafinal":"24:00",
                                                 "fecha":"29-08-2024"}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Asistance not found"

def test_delete_asistance_existing():
    response = client.post("/asistance/delete", data={"id": 44}, headers=headers)
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

def test_delete_asistance_not_found():
    response = client.post("/asistance/delete", data={"id": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Asistance not found"

def test_index_create_form():
    response = client.get("/asistance/crear", headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/asistance/actualizar", headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/asistance/eliminar", headers=headers)
    assert response.status_code == 200
