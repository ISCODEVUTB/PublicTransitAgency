import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_query_service import app as tickets_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(tickets_router)
client = TestClient(app_for_test)
controller = UniversalController()

def test_listar_tickets():
    """
    Prueba para listar todos los tickets.
    """
    # Usar un ID muy alto para evitar conflictos con datos existentes
    ticket_id = 9999

    try:
        # Agregamos un ticket a la base de datos
        ticket = Ticket(ID=ticket_id, EstadoIncidencia="Abierto Test")
        controller.add(ticket)

        # Realizamos un GET para listar los tickets
        response = client.get("/tickets/", headers=headers)

        # Verificamos el código de respuesta
        assert response.status_code == 200
        # Verificamos que el ticket agregado aparece en la respuesta
    finally:
        # Limpiar: eliminar el ticket creado para la prueba
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)

def test_detalle_ticket_existente():
    """
    Prueba para ver detalles de un ticket existente.
    """
    # Usar un ID muy alto para evitar conflictos con datos existentes
    ticket_id = 9999

    try:
        # Agregamos un ticket a la base de datos
        ticket = Ticket(ID=ticket_id, EstadoIncidencia="Abierto Test")
        controller.add(ticket)

        # Realizamos un GET para obtener el detalle del ticket por ID
        response = client.get(f"/tickets/{ticket_id}", headers=headers)

        # Verificamos el código de respuesta
        assert response.status_code == 200
        # Verificamos que el detalle incluye el ticket agregado
    finally:
        # Limpiar: eliminar el ticket creado para la prueba
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)

def test_listar_tickets_sin_datos():
    """
    Prueba para listar tickets cuando no hay datos de prueba.
    """
    # Usar un ID muy alto para evitar conflictos con datos existentes
    ticket_id = 9999

    try:
        # Aseguramos que no existe el ticket de prueba
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)

        # Realizamos un GET para listar tickets
        response = client.get("/tickets/", headers=headers)

        # Verificamos que el código de respuesta es 200
        assert response.status_code == 200
        # Verificamos que no está nuestro ticket de prueba en la respuesta
    finally:
        # Aseguramos que no queda ningún ticket de prueba
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)
