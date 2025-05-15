import logging
import json
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.type_movement import TypeMovementOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user
# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for user-related endpoints
app = APIRouter(prefix="/typemovement", tags=["typemovement"])

# Initialize universal controller instance


# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Render the 'ConsultarTipoMovimiento.html' template for the user consultation page.
    """
    #logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de tipo de movimiento")
    #logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de tipo de movimiento")
    return templates.TemplateResponse("ConsultarTipoMovimiento.html", {"request": request})


@app.get("/typemovements")
async def get_typemovement(
    request:Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
    request:Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all typemovements records from the database.
    """
    #logger.info(f"[GET /typemovements] Usuario: {current_user['user_id']} - Consultando todas los tipos de movimiento.")
    #logger.info(f"[GET /typemovements] Usuario: {current_user['user_id']} - Consultando todas los tipos de movimiento.")
    typemovements = controller.read_all(TypeMovementOut)
    if typemovements:
        # Si hay varias asistencias, iterar sobre ellas
        context = {
            "request": request,
            "tiposmovimientos": typemovements,  # Lista de asistencias
        }
    else:
        logger.warning(f"[GET /users] No se encontraron usuarios registrados")
        context = {
            "request": typemovements,
            "tiposmovimientos": []  # Si no se encontraron usuarios
        }

    return templates.TemplateResponse("tiposmovimientos.html", context)
    if typemovements:
        # Si hay varias asistencias, iterar sobre ellas
        context = {
            "request": request,
            "tiposmovimientos": typemovements,  # Lista de asistencias
        }
    else:
        logger.warning(f"[GET /users] No se encontraron usuarios registrados")
        context = {
            "request": typemovements,
            "tiposmovimientos": []  # Si no se encontraron usuarios
        }

    return templates.TemplateResponse("tiposmovimientos.html", context)


@app.get("/tipomovimiento", response_class=HTMLResponse)
def typemovement(
    request: Request,
    id: int = Query(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve a user by its ID and render the 'typetransport.html' template with its details.
    If the user is not found, display 'None' for all fields.
    """
    logger.info(f"[GET /typemovement] Usuario: {current_user['user_id']} - Consultando tipo de movimiento con ID={id}")
    unit_typemovement= controller.get_by_id(TypeMovementOut, id)

    if unit_typemovement:
        logger.info(f"[GET /typemovement] Tipo de Movimiento encontrado: {unit_typemovement.ID}, {unit_typemovement.TipoMovimiento}")
        logger.info(f"[GET /typemovement] Tipo de Movimiento encontrado: {unit_typemovement.ID}, {unit_typemovement.TipoMovimiento}")

    else:
        logger.warning(f"[GET /typemovement] No se encontró tipo de movimientos con id={id}")
        
    context = {
        "request": request,
        "ID": unit_typemovement.ID if unit_typemovement else "None",
        "TipoMovimiento": unit_typemovement.TipoMovimiento if unit_typemovement else "None"
        "ID": unit_typemovement.ID if unit_typemovement else "None",
        "TipoMovimiento": unit_typemovement.TipoMovimiento if unit_typemovement else "None"
    }

    return templates.TemplateResponse(request,"tipomovimiento.html", context)
