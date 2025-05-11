import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_cud_service import app as stops_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.stops import Parada
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(stops_router)
client = TestClient(app_for_test)
controller = UniversalController()

def test_crear_parada():
    """
    Prueba para crear una parada.
    """
    # Usar un ID muy alto para evitar conflictos con datos existentes
    parada_id = 9999

    try:
        response = client.post("/paradas/create", data={
            "id": parada_id,
            "Nombre": "Parada Test",
            "Ubicacion": "Ubicación Test"
        }, headers=headers)

        assert response.status_code == 200
        assert response.json()["message"] == "Parada creada exitosamente."

        # Verificar que la parada se creó correctamente
        parada = controller.get_by_id(Parada, parada_id)
        assert parada is not None
        assert parada.Nombre == "Parada Test"
        assert parada.Ubicacion == "Ubicación Test"
    finally:
        # Limpiar: eliminar la parada creada para la prueba
        parada = controller.get_by_id(Parada, parada_id)
        if parada:
            controller.delete(parada)

def test_actualizar_parada():
    """
    Prueba para actualizar una parada existente.
    """
    # Usar un ID muy alto para evitar conflictos con datos existentes
    parada_id = 9999

    try:
        # Crear una parada para la prueba
        parada = Parada(ID=parada_id, Nombre="Parada Original", Ubicacion="Ubicación Original")
        controller.add(parada)

        # Actualizar la parada
        response = client.post("/paradas/update", data={
            "id": parada_id,
            "Nombre": "Parada Actualizada",
            "Ubicacion": "Ubicación Actualizada"
        }, headers=headers)

        assert response.status_code == 200
        assert response.json()["message"] == "Parada actualizada exitosamente."

        # Verificar que la parada se actualizó correctamente
        parada_actualizada = controller.get_by_id(Parada, parada_id)
        assert parada_actualizada is not None
        assert parada_actualizada.Nombre == "Parada Actualizada"
        assert parada_actualizada.Ubicacion == "Ubicación Actualizada"
    finally:
        # Limpiar: eliminar la parada creada para la prueba
        parada = controller.get_by_id(Parada, parada_id)
        if parada:
            controller.delete(parada)

def test_eliminar_parada():
    """
    Prueba para eliminar una parada existente.
    """
    # Usar un ID muy alto para evitar conflictos con datos existentes
    parada_id = 9999

    # Crear una parada para la prueba
    parada = Parada(ID=parada_id, Nombre="Parada Test", Ubicacion="Ubicación Test")
    controller.add(parada)

    # Eliminar la parada
    response = client.post("/paradas/delete", data={"id": parada_id}, headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Parada eliminada exitosamente."

    # Verificar que la parada se eliminó correctamente
    parada_eliminada = controller.get_by_id(Parada, parada_id)
    assert parada_eliminada is None

def test_eliminar_parada_no_existente():
    """
    Prueba para eliminar una parada que no existe.
    """
    # Usar un ID muy alto que seguramente no existe
    parada_id = 99999

    # Intentar eliminar una parada que no existe
    response = client.post("/paradas/delete", data={"id": parada_id}, headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Parada no encontrada"
