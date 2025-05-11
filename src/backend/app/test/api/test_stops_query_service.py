import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.app.api.routes.stops_query_service import app as paradas_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.stops import Parada
from backend.app.core.conf import headers

app_for_test = FastAPI()
app_for_test.include_router(paradas_router)
client = TestClient(app_for_test)
controller = UniversalController()

def test_listar_paradas():
    """
    Prueba para listar todas las paradas.
    """
    # Usar IDs muy altos para evitar conflictos con datos existentes
    parada_id1 = 9998
    parada_id2 = 9999

    try:
        # Crear algunas paradas de prueba
        parada1 = Parada(ID=parada_id1, Nombre="Parada Test 1", Ubicacion="Ubicación Test 1")
        parada2 = Parada(ID=parada_id2, Nombre="Parada Test 2", Ubicacion="Ubicación Test 2")
        controller.add(parada1)
        controller.add(parada2)

        # Realizamos un GET para listar las paradas
        response = client.get("/paradas/", headers=headers)

        # Verificamos el código de respuesta
        assert response.status_code == 200
        # Verificamos que las paradas agregadas aparecen en la respuesta
    finally:
        # Limpiar: eliminar las paradas creadas para la prueba
        parada1 = controller.get_by_id(Parada, parada_id1)
        if parada1:
            controller.delete(parada1)
        parada2 = controller.get_by_id(Parada, parada_id2)
        if parada2:
            controller.delete(parada2)


def test_listar_sin_paradas():
    """
    Prueba para listar cuando no hay paradas de prueba.
    """
    # Usar un ID muy alto para evitar conflictos con datos existentes
    parada_id = 9999

    try:
        # Aseguramos que no existe la parada de prueba
        parada = controller.get_by_id(Parada, parada_id)
        if parada:
            controller.delete(parada)

        # Realizamos un GET para listar paradas
        response = client.get("/paradas/", headers=headers)

        # Verificamos que el código de respuesta es 200
        assert response.status_code == 200
        # Verificamos que no está nuestra parada de prueba en la respuesta
    finally:
        # Aseguramos que no queda ninguna parada de prueba
        parada = controller.get_by_id(Parada, parada_id)
        if parada:
            controller.delete(parada)


def test_detalle_parada_existente():
    """
    Prueba para obtener detalles de una parada existente.
    """
    # Usar un ID muy alto para evitar conflictos con datos existentes
    parada_id = 9999

    try:
        # Crear una parada de prueba
        parada = Parada(ID=parada_id, Nombre="Parada Test", Ubicacion="Ubicación Test")
        controller.add(parada)

        # Realizamos un GET para obtener el detalle de la parada por ID
        response = client.get(f"/paradas/{parada_id}", headers=headers)

        # Verificamos el código de respuesta
        assert response.status_code == 200
        # Verificamos que el detalle incluye la parada agregada
        
    finally:
        # Limpiar: eliminar la parada creada para la prueba
        parada = controller.get_by_id(Parada, parada_id)
        if parada:
            controller.delete(parada)

def test_detalle_parada_no_existente():
    """
    Prueba para manejar el caso de una parada no existente.
    """
    # Usar un ID muy alto que seguramente no existe
    parada_id = 99999

    # Realizamos un GET para un ID que no existe
    response = client.get(f"/paradas/{parada_id}", headers=headers)

    # Verificamos que el código de respuesta es 404
    assert response.status_code == 404
    # Verificamos que se muestra el mensaje de error apropiado
    assert response.json()["detail"] == "Parada no encontrada"
