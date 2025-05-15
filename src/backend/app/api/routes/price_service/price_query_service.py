import logging
import json
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.price import PriceOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for user-related endpoints
app = APIRouter(prefix="/price", tags=["price"])

# Initialize universal controller instance


# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=[
        "system", "administrador"])
):
    """
    Render the 'ConsultarPrecio.html' template for the user consultation page.
    """
    logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de precio")
    return templates.TemplateResponse("ConsultarPrecio.html", {"request": request})


@app.get("/prices")
async def get_price(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all prices records from the database.
    """
    logger.info(f"[GET /prices] Usuario: {current_user['user_id']} - Consultando todas los precios.")
    prices = controller.read_all(PriceOut)
    logger.info(f"[GET /prices] Número de precios encontrados: {len(prices)}")
    return prices


@app.get("/precio", response_class=HTMLResponse)
def price(
    request: Request,
    id: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve a user by its ID and render the 'price.html' template with its details.
    If the user is not found, display 'None' for all fields.
    """
    logger.info(f"[GET /price] Usuario: {current_user['user_id']} - Consultando precio con id={id}")
    unit_price= controller.get_by_id(PriceOut, id)

    if unit_price:
        logger.info(f"[GET /price] Precio encontrado: {unit_price.ID}, {unit_price.IDTipoTransporte},{unit_price.Monto}")

    else:
        logger.warning(f"[GET /price] No se encontró precio con id={id}")

        context = {
        "request": request,
        "ID": unit_price.ID if unit_price else "None",
        "IDTipoTransporte": unit_price.IDTipoTransporte if unit_price else "None",
        "Monto": unit_price.Monto if unit_price else "None"
    }

    return templates.TemplateResponse(request,"precio.html", context)
