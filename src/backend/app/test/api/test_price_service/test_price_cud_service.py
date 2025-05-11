from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.api.routes.price_cud_service import app as price_router  # Importa bien
from backend.app.core.conf import headers
# Limpieza de base de datos antes y después de cada test
app_for_test = FastAPI()
app_for_test.include_router(price_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Cliente de prueba
client = TestClient(app_for_test)

def test_create_price():
    response = client.post("/price/create", data={"ID":2,"IDTipoTransporte":2,"Monto":100},headers=headers)
    assert response.status_code == 200

def test_update_price_existing():
    response = client.post("/price/update", data={"ID":2,"IDTipoTransporte":2,"Monto":100},headers=headers)
    assert response.status_code == 200

def test_update_price_not_found():
    response = client.post("/price/update", data={"ID":99,"IDTipoTransporte":5,"Monto":2200},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Price not found"

def test_delete_price_existing():
    response = client.post("/price/delete", data={"ID": 2},headers=headers)
    assert response.status_code == 200

def test_delete_price_not_found():
    response = client.post("/price/delete", data={"ID": 999},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Price not found"

def test_index_create_form():
    response = client.get("/price/crear",headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/price/actualizar",headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/price/eliminar",headers=headers)
    assert response.status_code == 200
