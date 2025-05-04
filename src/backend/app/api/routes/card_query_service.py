import logging
from fastapi import Request, Query, APIRouter, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import verify_token_and_scope
from backend.app.models.card import CardOut
from backend.app.logic.universal_controller_sql import UniversalController

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Crear el router
app = APIRouter(prefix="/card", tags=["card"])

# Controlador y plantillas
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request,
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, required_scopes=[
        "system", "administrador", "pasajero", "supervisor", "mantenimiento"
    ])
    logger.info(f"[GET /consultar] Usuario: {user_id} - Mostrando página de consulta de tarjeta")
    return templates.TemplateResponse("ConsultarTarjeta.html", {"request": request})


@app.get("/tarjetas")
async def get_tarjetas(
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "administrador"])
    logger.info(f"[GET /tarjetas] Usuario: {user_id} - Consultando todas las tarjetas.")
    
    tarjetas = controller.read_all(CardOut)
    logger.info(f"[GET /tarjetas] Número de tarjetas encontradas: {len(tarjetas)}")
    return tarjetas


@app.get("/tarjeta", response_class=HTMLResponse)
def tarjeta(
    request: Request,
    id: int = Query(...),
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "administrador", "pasajero"])
    logger.info(f"[GET /tarjeta] Usuario: {user_id} - Consultando tarjeta con id={id}")
    
    unit_tarjeta = controller.get_by_id(CardOut, id)

    if unit_tarjeta:
        logger.info(f"[GET /tarjeta] Tarjeta encontrada: {unit_tarjeta.id}, Tipo: {unit_tarjeta.tipo}, Saldo: {unit_tarjeta.balance}")
    else:
        logger.warning(f"[GET /tarjeta] No se encontró tarjeta con id={id}")

    context = {
        "request": request,
        "id": unit_tarjeta.id if unit_tarjeta else "None",
        "tipo": unit_tarjeta.tipo if unit_tarjeta else "None",
        "saldo": unit_tarjeta.balance if unit_tarjeta else "None"
    }

    return templates.TemplateResponse("tarjeta.html", context)
