import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.movement_service.movement_query_service import app as movement_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.movement import MovementOut

test_app = FastAPI()
test_app.include_router(movement_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
def test_consultar_page():
    """Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    response = client.get("/price/consultar",headers=headers)
    assert response.status_code == 200

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los movimientos."""
    response = client.get("/movement/movements/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ID"] == 2
    assert data[0]["IDTipoMovimiento"] == 2
    assert data[0]["Monto"] == 100

def test_get_by_id():
    """Prueba que la ruta '/movement/{ID}' devuelve el movimiento correcto."""
    response = client.get("/movement/2", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["ID"] == 2

def test_get_by_id_not_found():
    """Prueba que la ruta '/movement/{ID}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/movement/999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == "Movimiento no encontrado"

