import logging
import json
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.rol_user import RolUserOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for user-related endpoints
app = APIRouter(prefix="/roluser", tags=["roluser"])

# Initialize universal controller instance


# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request
):
    """
    Render the 'ConsultarRolUsuario.html' template for the user consultation page.
    """
    return templates.TemplateResponse("ConsultarRolUser.html", {"request": request})


@app.get("/rolusers")
async def get_roluser(
):
    """
    Retrieve and return all rolusers records from the database.
    """
    #logger.info(f"[GET /rolusers] Usuario: {current_user['user_id']} - Consultando todas los tipos de usuarios.")
    rolusers = controller.read_all(RolUserOut)
    logger.info(f"[GET /rolusers] Número de tipo de usuarios encontrados: {len(rolusers)}")
    return rolusers


@app.get("/tipousuario", response_class=HTMLResponse)
def roluser(
    request: Request,
    ID: int = Query(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve a user by its ID and render the 'typetransport.html' template with its details.
    If the user is not found, display 'None' for all fields.
    """
    #logger.info(f"[GET /roluser] Usuario: {current_user['user_id']} - Consultando tipo de usuario con id={ID}")
    unit_roluser= controller.get_by_id(RolUserOut, ID)

    if unit_roluser:
        logger.info(f"[GET /roluser] Tipo de Usuario encontrado: {unit_roluser.ID}, {unit_roluser.Rol}")

    else:
        logger.warning(f"[GET /roluser] No se encontró tipo de usuario con id={ID}")

    context = {
        "request": request,
        "id": unit_roluser.ID if unit_roluser else "None",
        "type": unit_roluser.Rol if unit_roluser else "None"
    }

    return templates.TemplateResponse(request,"roluser.html", context)
