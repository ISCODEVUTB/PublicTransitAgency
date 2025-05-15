import logging
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.card import CardOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for card-related endpoints
app = APIRouter(prefix="/card", tags=["card"])

# Initialize universal controller instance

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(request: Request):
    """
    Render the 'ConsultarTarjeta.html' template for the card consultation page.
    """
    return templates.TemplateResponse(request,"ConsultarTarjeta.html", {"request": request})


@app.get("/tarjetas")
async def get_tarjetas():
    """
    Retrieve and return all card records from the database.
    """
    tarjetas = controller.read_all(CardOut)
    logger.info(f"[GET /tarjetas] Número de tarjetas encontradas: {len(tarjetas)}")
    return tarjetas


@app.get("/tarjeta", response_class=HTMLResponse)
def tarjeta(request: Request, ID: int = Query(...)):
    """
    Retrieve a card by its ID and render the 'tarjeta.html' template with its details.
    If the card is not found, display 'None' for all fields.
    """
    unit_tarjeta = controller.get_by_id(CardOut, ID)

    if unit_tarjeta:
        logger.info(f"[GET /tarjeta] Tarjeta encontrada: {unit_tarjeta.ID}, IDUsuario: {unit_tarjeta.IDUsuario}, IDTipoTarjeta: {unit_tarjeta.IDTipoTarjeta}")
    else:
        logger.warning(f"[GET /tarjeta] No se encontró tarjeta con ID={ID}")

    context = {
        "request": request,
        "ID": unit_tarjeta.ID if unit_tarjeta else "None",
        "IDUsuario": unit_tarjeta.IDUsuario if unit_tarjeta else "None",
        "IDTipoTarjeta": unit_tarjeta.IDTipoTarjeta if unit_tarjeta else "None",
        "Saldo": unit_tarjeta.Saldo if unit_tarjeta else "None"
    }

    return templates.TemplateResponse(request,"tarjeta.html", context)
