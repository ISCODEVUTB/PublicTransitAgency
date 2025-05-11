from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.api.routes.type_transport_cud_service import app as typetransport_router  # Importa bien
from backend.app.core.conf import headers

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(typetransport_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Cliente de prueba
client = TestClient(app_for_test)

def test_create_transport():
    response = client.post("/typetransport/create", data={"id":1,"type":"aaaaa"},headers=headers)
    assert response.status_code == 200

def test_update_transport_existing():
    # Luego actualizarlo
    response = client.post("/typetransport/update", data={"id":2,"type":"railway"},headers=headers)
    assert response.status_code == 200

def test_update_transport_not_found():
    response = client.post("/typetransport/update", data={"id": 99, "type":"ninguno"},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "TypeTransport not found"

def test_delete_transport_existing():
    response = client.post("/typetransport/delete", data={"id": 1},headers=headers)
    assert response.status_code == 200

def test_delete_transport_not_found():
    response = client.post("/typetransport/delete", data={"id": 999},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "TypeTransport not found"

def test_index_create_form():
    response = client.get("/typetransport/crear",headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/typetransport/actualizar",headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/typetransport/eliminar",headers=headers)
    assert response.status_code == 200
