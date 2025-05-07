from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.auth import get_current_user
from starlette.responses import HTMLResponse
from src.backend.app.api.routes.card_query_service import templates
from fastapi import Request
app = APIRouter(prefix="/tickets", tags=["tickets"])
controller = UniversalController()

@app.get("/create", response_class=HTMLResponse)
def crear_ticket_form(request: Request):
    return templates.TemplateResponse("CrearTicket.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_ticket_form(request: Request):
    return templates.TemplateResponse("EliminarTicket.html", {"request": request})

@app.get("/update", response_class=HTMLResponse)
def actualizar_ticket_form(request: Request):
    return templates.TemplateResponse("ActualizarTicket.html", {"request": request})

@app.post("/create")
def crear_ticket(
    id: int = Form(...),
    estadoincidencia: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Endpoint para crear un ticket.
    """
    ticket = Ticket(id=id, estadoincidencia=estadoincidencia)
    try:
        controller.add(ticket)
        return {"message": "Ticket creado exitosamente.", "data": ticket.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_ticket(
    id: int = Form(...),
    estadoincidencia: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Endpoint para actualizar un ticket existente.
    """
    existing_ticket = controller.get_by_id(Ticket, id)
    if not existing_ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    updated_ticket = Ticket(id=id, estadoincidencia=estadoincidencia)
    try:
        controller.update(updated_ticket)
        return {"message": "Ticket actualizado exitosamente.", "data": updated_ticket.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_ticket(
    id: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Endpoint para eliminar un ticket por su ID.
    """
    existing_ticket = controller.get_by_id(Ticket, id)
    if not existing_ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    try:
        controller.delete(existing_ticket)
        return {"message": "Ticket eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))