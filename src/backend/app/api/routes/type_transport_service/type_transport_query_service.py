import logging
import json
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.type_transport import TypeTransportOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for user-related endpoints
app = APIRouter(prefix="/typetransport", tags=["typetransport"])

# Initialize universal controller instance


# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Render the 'ConsultarTipoTransporte.html' template for the user consultation page.
    """
    #logger.info(f"[GET /consultar] Usuario: {current_user['user_ID']} - Mostrando página de consulta de tipo de transporte")
    return templates.TemplateResponse("ConsultarTipoTransporte.html", {"request": request})


@app.get("/typetransports")
async def get_typetransport(
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all typetransports records from the database.
    """
    #logger.info(f"[GET /typetransports] Usuario: {current_user['user_ID']} - Consultando todas los tipos de transporte.")
    typetransports = controller.read_all(TypeTransportOut)
    logger.info(f"[GET /typetransports] Número de tipo de transportes encontrados: {len(typetransports)}")
    return typetransports


@app.get("/tipotransporte", response_class=HTMLResponse)
def typetransport(
    request: Request,
    ID: int = Query(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve a user by its ID and render the 'typetransport.html' template with its details.
    If the user is not found, display 'None' for all fields.
    """
    #logger.info(f"[GET /typetransport] Usuario: {current_user['user_ID']} - Consultando tipo de transporte con ID={ID}")
    unit_typetransport= controller.get_by_ID(TypeTransportOut, ID)

    if unit_typetransport:
        logger.info(f"[GET /typetransport] Tipo de Transporte encontrados: {unit_typetransport.id}, {unit_typetransport.type}")

    else:
        logger.warning(f"[GET /typetransport] No se encontró tipo de transporte con id={id}")
    
    context = {
        "request": request,
        "id": unit_typetransport.id if unit_typetransport else "None",
        "type": unit_typetransport.type if unit_typetransport else "None"
    }

    return templates.TemplateResponse(request,"tipotransporte.html", context)
