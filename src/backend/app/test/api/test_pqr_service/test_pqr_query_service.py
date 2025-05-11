import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.pqr_service.pqr_query_service import app as pqr_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.pqr import PQROut

test_app = FastAPI()
test_app.include_router(pqr_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
#def test_consultar_page():
"""Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    #response = client.get("/price/consultar",headers=headers)
    #assert response.status_code == 200
    #assert "Consultar Saldo" in response.text  # Verifica si la plantilla está presente

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los tipos de transporte."""
    response = client.get("/pqr/pqrs/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 41

def test_get_by_id():
    """Prueba que la ruta '/pqr/{id}' devuelve el pqr correcto."""
    response = client.get("/pqr/41", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 41

def test_get_by_userid():
    """Prueba que la ruta '/pqr/user/{iduser}' devuelve el pqr correcto."""
    response = client.get("/pqr/user/100001", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 41


def test_get_by_id_not_found():
    """Prueba que la ruta '/price/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/pqr/999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == "PQR no encontrado"

