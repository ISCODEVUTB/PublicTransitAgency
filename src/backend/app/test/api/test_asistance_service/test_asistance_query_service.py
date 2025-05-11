import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.asistance_service.asistance_query_service import app as asistance_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.asistance import AsistanceOut

test_app = FastAPI()
test_app.include_router(asistance_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
#def test_consultar_page():
"""Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    #response = client.get("/asistance/consultar",headers=headers)
    #assert response.status_code == 200
    #assert "Consultar Saldo" in response.text  # Verifica si la plantilla está presente

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los tipos de transporte."""
    response = client.get("/asistance/asistencias/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 44

def test_get_by_id():
    """Prueba que la ruta '/asistance/{id}' devuelve el asistance correcto."""
    response = client.get("/asistance/44", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 44

def test_get_by_userid():
    """Prueba que la ruta '/asistance/user/{iduser}' devuelve las asistencias correctas para un iduser."""
    response = client.get("/asistance/user/99", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["id"] == 44
    assert data[0]["iduser"] == 99

def test_get_by_id_not_found():
    """Prueba que la ruta '/asistance/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/asistance/999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

