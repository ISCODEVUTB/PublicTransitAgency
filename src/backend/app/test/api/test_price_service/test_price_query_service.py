import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.price_query_service import app as price_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.price import PriceOut

test_app = FastAPI()
test_app.include_router(price_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
#def test_consultar_page():
"""Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    #response = client.get("/price/consultar",headers=headers)
    #assert response.status_code == 200
    #assert "Consultar Saldo" in response.text  # Verifica si la plantilla está presente

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los tipos de transporte."""
    response = client.get("/price/prices/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ID"] == 44

def test_get_by_id():
    """Prueba que la ruta '/price/{id}' devuelve el precio correcto."""
    response = client.get("/price/44", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["ID"] == 44
    assert data["IDTipoTransporte"] == 2
    assert data["Monto"] == 1212

def test_get_by_id_not_found():
    """Prueba que la ruta '/price/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/price/999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == "Precio no encontrado"

