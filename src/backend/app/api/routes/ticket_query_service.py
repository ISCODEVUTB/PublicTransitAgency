from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/tickets", tags=["tickets"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_tickets(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    try:
        tickets = controller.read_all(Ticket)
        return templates.TemplateResponse("ListarTickets.html", {"request": request, "tickets": tickets})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id}", response_class=HTMLResponse)
def detalle_ticket(
    id: int,
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    try:
        ticket = controller.get_by_id(Ticket, id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
        return templates.TemplateResponse("DetalleTicket.html", {
            "request": request,
            "ticket": ticket.to_dict()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))