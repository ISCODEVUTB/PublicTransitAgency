from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.ticket import Ticket
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/tickets", tags=["tickets"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_tickets(
    request: Request,
):
    """
    Lista todos los tickets.
    """
    tickets = controller.read_all(Ticket)
    return templates.TemplateResponse("ListarTickets.html", {"request": request, "tickets": tickets})

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_ticket(
    ID: int,
    request: Request,
):
    """
    Obtiene el detalle de un ticket por su ID.
    """
    ticket = controller.get_by_id(Ticket, ID)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return templates.TemplateResponse("DetalleTicket.html", {"request": request, "ticket": ticket.to_dict()})
