#import logging
import json
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

#from backend.app.core.auth import get_current_user
from backend.app.models.type_movement import TypeMovementOut
from backend.app.logic.universal_controller_sql import UniversalController

# Configuración del logger
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO)

# Create the router for user-related endpoints
app = APIRouter(prefix="/typemovement", tags=["typemovement"])

# Initialize universal controller instance
controller = UniversalController()

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Render the 'ConsultarTipoMovimiento.html' template for the user consultation page.
    """
    #logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de tipo de movimiento")
    return templates.TemplateResponse("ConsultarTipoMovimiento.html", {"request": request})


@app.get("/typemovements")
async def get_typemovement(
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all typemovements records from the database.
    """
    #logger.info(f"[GET /typemovements] Usuario: {current_user['user_id']} - Consultando todas los tipos de movimiento.")
    typemovements = controller.read_all(TypeMovementOut)
    #logger.info(f"[GET /typemovements] Número de tipo de movimientos encontrados: {len(typemovements)}")
    return typemovements


@app.get("/{id}", response_class=HTMLResponse)
def typetransport(
    request: Request,
    id: int
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve a user by its ID and render the 'typetransport.html' template with its details.
    If the user is not found, display 'None' for all fields.
    """
    #logger.info(f"[GET /typemovement] Usuario: {current_user['user_id']} - Consultando tipo de movimiento con id={id}")
    unit_typemovement= controller.get_by_id(TypeMovementOut, id)

    if unit_typemovement:
        #logger.info(f"[GET /typemovement] Tipo de Movimiento encontrado: {unit_typemovement.id}, {unit_typemovement.type}")
        return JSONResponse(content=unit_typemovement.model_dump(), status_code=200)

    else:
        #logger.warning(f"[GET /typemovement] No se encontró tipo de movimientos con id={id}")
        return JSONResponse(content="Tipo de Movimientos no encontrado", status_code=404)