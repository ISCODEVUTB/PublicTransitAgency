from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.auth import get_current_user
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = APIRouter(prefix="/tickets", tags=["tickets"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_ticket_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return templates.TemplateResponse("CrearTicket.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_ticket_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return templates.TemplateResponse("EliminarTicket.html", {"request": request})

@app.get("/update", response_class=HTMLResponse)
def actualizar_ticket_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return templates.TemplateResponse("ActualizarTicket.html", {"request": request})

@app.post("/create")
def crear_ticket(
    ID: int = Form(...),
    EstadoIncidencia: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Endpoint para crear un ticket.
    """
    ticket = Ticket(ID=ID, EstadoIncidencia=EstadoIncidencia)
    try:
        controller.add(ticket)
        return {"message": "Ticket creado exitosamente.", "data": ticket.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_ticket(
    ID: int = Form(...),
    EstadoIncidencia: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Endpoint para actualizar un ticket existente.
    """
    existing_ticket = controller.get_by_id(Ticket, ID)
    if not existing_ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    updated_ticket = Ticket(ID=ID, EstadoIncidencia=EstadoIncidencia)
    try:
        controller.update(updated_ticket)
        return {"message": "Ticket actualizado exitosamente.", "data": updated_ticket.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_ticket(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Endpoint para eliminar un ticket por su ID.
    """
    existing_ticket = controller.get_by_id(Ticket, ID)
    if not existing_ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    try:
        controller.delete(existing_ticket)
        return {"message": "Ticket eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
