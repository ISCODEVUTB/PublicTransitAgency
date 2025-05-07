#import logging
import json
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

#from backend.app.core.auth import get_current_user
from backend.app.models.user import UserOut
from backend.app.logic.universal_controller_sql import UniversalController

# Configuración del logger
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO)

# Create the router for user-related endpoints
app = APIRouter(prefix="/user", tags=["user"])

# Initialize universal controller instance
controller = UniversalController()

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request
):
    """
    Render the 'ConsultarUsuario.html' template for the user consultation page.
    """
    return templates.TemplateResponse("ConsultarUsuario.html", {"request": request})


@app.get("/users")
async def get_users(
):
    """
    Retrieve and return all user records from the database.
    """
    usuarios = controller.read_all(UserOut)
    return usuarios


@app.get("/{id}", response_class=HTMLResponse)
def usuario(
    request: Request,
    id: int,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "pasajero"])
):
    """
    Retrieve a user by its ID and render the 'usuario.html' template with its details.
    If the user is not found, display 'None' for all fields.
    """
    logger.info(f"[GET /user] Usuario: {current_user['user_id']} - Consultando usuario con id={id}")
    unit_usuario= controller.get_by_id(UserOut, id)

    if unit_usuario:
        logger.info(f"[GET /user] Usuario encontrados: {unit_usuario.id}, {unit_usuario.identification},{unit_usuario.name},{unit_usuario.lastname},{unit_usuario.email},{unit_usuario.password},{unit_usuario.idtype_user},{unit_usuario.idturn}")
        return JSONResponse(content=unit_usuario.model_dump(), status_code=200)

    else:
        logger.warning(f"[GET /user] No se encontró usuario con id={id}")
        return JSONResponse(content="Usuario no encontrado", status_code=404)