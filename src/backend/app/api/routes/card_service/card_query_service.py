import logging
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.card import CardOut
from backend.app.logic.universal_controller_sqlserver import UniversalController

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for card-related endpoints
app = APIRouter(prefix="/card", tags=["card"])

# Initialize universal controller instance
controller = UniversalController()

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
def tarjeta(request: Request, id: int = Query(...)):
    """
    Retrieve a card by its ID and render the 'tarjeta.html' template with its details.
    If the card is not found, display 'None' for all fields.
    """
    unit_tarjeta = controller.get_by_id(CardOut, id)

    if unit_tarjeta:
        logger.info(f"[GET /tarjeta] Tarjeta encontrada: {unit_tarjeta.id}, iduser: {unit_tarjeta.iduser}, idtype: {unit_tarjeta.idtype}")
    else:
        logger.warning(f"[GET /tarjeta] No se encontró tarjeta con id={id}")

    context = {
        "request": request,
        "id": unit_tarjeta.id if unit_tarjeta else "None",
        "iduser": unit_tarjeta.iduser if unit_tarjeta else "None",
        "idtype": unit_tarjeta.idtype if unit_tarjeta else "None",
        "balance": unit_tarjeta.balance if unit_tarjeta else "None"
    }

    return templates.TemplateResponse(request,"tarjeta.html", context)