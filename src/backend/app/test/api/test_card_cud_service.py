from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.api.routes import card_cud_service  # Importamos el módulo, no solo el `app`
from backend.app.core.conf import headers
from backend.app.models.user import UserCreate
from backend.app.models.shift import Shift
from backend.app.models.type_card import TypeCardCreate
from backend.app.models.card import CardCreate

# Crear instancia del controlador que se usará en pruebas
test_controller = UniversalController()

# Sobrescribir el controlador usado en el módulo de rutas
card_cud_service.controller = test_controller

# Limpiar base de datos
def setup_function():
    test_controller.clear_tables()

def teardown_function():
    test_controller.clear_tables()

# App de prueba
app_for_test = FastAPI()
app_for_test.include_router(card_cud_service.app)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_card():
    test_controller.add(TypeCardCreate(id=1, type="Estandar"))
    test_controller.add(Shift(ID=1, TipoTurno="No Aplica"))
    test_controller.add(UserCreate(
        ID=1,
        Identificacion=11022311,
        Nombre="Kenan",
        Apellido="Jarrus",
        Correo="msjedi@yoda.com",
        Contrasena="hera",
        IDRolUsuario=1,
        IDTurno=1,
        IDTarjeta=1
    ))
    response = client.post("/card/create", data={"id": 15, "iduser": 1, "idtype": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 15
    assert response.json()["data"]["balance"] == 0

def test_update_card_existing():
    test_controller.add(TypeCardCreate(id=1, type="Estandar"))
    test_controller.add(Shift(ID=1, TipoTurno="No Aplica"))
    test_controller.add(UserCreate(
        ID=1,
        Identificacion=11022311,
        Nombre="Kenan",
        Apellido="Jarrus",
        Correo="msjedi@yoda.com",
        Contrasena="hera",
        IDRolUsuario=1,
        IDTurno=1,
        IDTarjeta=1
    ))
    test_controller.add(CardCreate(id=20, iduser=1, idtype=1, balance=10))

    response = client.post("/card/update", data={"id": 20, "iduser": 1, "idtype": 2}, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["idtype"] == 2

def test_update_card_not_found():
    response = client.post("/card/update", data={"id": 999, "iduser": 1, "idtype": 1}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"

def test_delete_card_existing():
    test_controller.add(TypeCardCreate(id=1, type="Estandar"))
    test_controller.add(Shift(ID=1, TipoTurno="No Aplica"))
    test_controller.add(UserCreate(
        ID=1,
        Identificacion=11022311,
        Nombre="Kenan",
        Apellido="Jarrus",
        Correo="msjedi@yoda.com",
        Contrasena="hera",
        IDRolUsuario=1,
        IDTurno=1,
        IDTarjeta=1
    ))
    test_controller.add(CardCreate(id=30, iduser=1, idtype=1, balance=0))

    response = client.post("/card/delete", data={"id": 30}, headers=headers)
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

def test_delete_card_not_found():
    response = client.post("/card/delete", data={"id": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"

def test_index_create_form():
    response = client.get("/card/crear", headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/card/actualizar", headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/card/eliminar", headers=headers)
    assert response.status_code == 200
