import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_cud_service import app as tickets_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(tickets_router)
client = TestClient(app_for_test)
controller = UniversalController()


def test_crear_ticket():
    """Prueba para crear un ticket"""
    # Usar un ID muy alto para evitar conflictos con datos existentes
    ticket_id = 9999

    try:
        response = client.post("/tickets/create", data={
            "ID": ticket_id,
            "EstadoIncidencia": "Abierto"
        }, headers=headers)

        assert response.status_code == 200
        assert response.json()["message"] == "Ticket creado exitosamente."

        # Verificar que el ticket se creó correctamente
        ticket = controller.get_by_id(Ticket, ticket_id)
        assert ticket is not None
        assert ticket.EstadoIncidencia == "Abierto"
    finally:
        # Limpiar: eliminar el ticket creado para la prueba
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)

def test_actualizar_ticket():
    """Prueba para actualizar un ticket existente"""
    # Usar un ID muy alto para evitar conflictos con datos existentes
    ticket_id = 9999

    try:
        # Crear un ticket para la prueba
        ticket = Ticket(ID=ticket_id, EstadoIncidencia="Abierto")
        controller.add(ticket)

        # Actualizar el ticket
        response = client.post("/tickets/update", data={
            "ID": ticket_id,
            "EstadoIncidencia": "Cerrado"
        }, headers=headers)

        assert response.status_code == 200
        assert response.json()["message"] == "Ticket actualizado exitosamente."

        # Verificar que el ticket se actualizó correctamente
        ticket_actualizado = controller.get_by_id(Ticket, ticket_id)
        assert ticket_actualizado is not None
        assert ticket_actualizado.EstadoIncidencia == "Cerrado"
    finally:
        # Limpiar: eliminar el ticket creado para la prueba
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)

def test_eliminar_ticket():
    """Prueba para eliminar un ticket existente"""
    # Usar un ID muy alto para evitar conflictos con datos existentes
    ticket_id = 9999

    # Crear un ticket para la prueba
    ticket = Ticket(ID=ticket_id, EstadoIncidencia="Abierto")
    controller.add(ticket)

    # Eliminar el ticket
    response = client.post("/tickets/delete", data={"ID": ticket_id}, headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Ticket eliminado exitosamente."

    # Verificar que el ticket se eliminó correctamente
    ticket_eliminado = controller.get_by_id(Ticket, ticket_id)
    assert ticket_eliminado is None

def test_eliminar_ticket_no_existente():
    """Prueba para eliminar un ticket que no existe"""
    # Usar un ID muy alto que seguramente no existe
    ticket_id = 99999

    # Intentar eliminar un ticket que no existe
    response = client.post("/tickets/delete", data={"ID": ticket_id}, headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket no encontrado"
