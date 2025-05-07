from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.payments import Payment
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/payments", tags=["payments"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_pagos(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    List all payments. Requires authentication.
    """
    pagos = controller.read_all(Payment)
    return templates.TemplateResponse("ListarPagos.html", {"request": request, "pagos": pagos})

@app.get("/{id}", response_class=HTMLResponse)
def detalle_pago(
    id: int,
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Get details of a specific payment by ID. Requires authentication.
    """
    pago = controller.get_by_id(Payment, id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return templates.TemplateResponse("DetallePago.html", {"request": request, "pago": pago})