import logging
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.pqr import PQROut
from backend.app.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for pqr-related endpoints
app = APIRouter(prefix="/pqr", tags=["pqr"])

# Initialize universal controller instance

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=[
        "system", "administrador", "pasajero"
    ])
):
    """
    Render the 'ConsultarPQR.html' template for the pqr consultation page.
    """
    logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de pqr")
    return templates.TemplateResponse(request,"ConsultarPQR.html", {"request": request})

@app.get("/consultar/user", response_class=HTMLResponse)
def consultar(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=[
        "system", "administrador"
    ])
):
    """
    Render the 'ConsultarPQR.html' template for the pqr consultation page.
    """
    logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de pqr")
    return templates.TemplateResponse(request,"ConsultarPQRUser.html", {"request": request})


@app.get("/pqrs")
async def get_pqrs(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all pqr records from the database.
    """
    logger.info(f"[GET /pqrs] Usuario: {current_user['user_id']} - Consultando todas las pqrs.")
    pqrs = controller.read_all(PQROut)
    logger.info(f"[GET /pqrs] Número de pqrs encontradas: {len(pqrs)}")
    return pqrs

#pqr by id pqr
@app.get("/find", response_class=HTMLResponse)
def pqr_by_id(
    request: Request,
    id: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve a pqr by its ID and render the 'pqr.html' template with its details.
    If the pqr is not found, display 'None' for all fields.
    """
    logger.info(f"[GET /pqr] Usuario: {current_user['user_id']} - Consultando pqr con id={id}")
    unit_pqr = controller.get_by_id(PQROut, id)

    if unit_pqr:
        logger.info(f"[GET /pqr] PQR encontrada: {unit_pqr.id}, iduser: {unit_pqr.iduser}")
    else:
        logger.warning(f"[GET /pqr] No se encontró pqr con id={id}")

    context = {
        "request": request,
        "id": unit_pqr.id if unit_pqr else "None",
        "iduser": unit_pqr.iduser if unit_pqr else "None",
        "type": unit_pqr.type if unit_pqr else "None",
        "description": unit_pqr.description if unit_pqr else "None",
        "codigogenerado":unit_pqr.codigogenerado if unit_pqr else "None",
        "fecha": unit_pqr.fecha if unit_pqr else "None",
    }

    return templates.TemplateResponse(request,"pqr.html", context)

#pqr by user id
@app.get("/user", response_class=HTMLResponse)
def pqr_by_user(
    request: Request,
    iduser: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador","pasajero"])
):
    """
    Retrieve a pqr by its ID and render the 'pqr.html' template with its details.
    If the pqr is not found, display 'None' for all fields.
    """
    logger.info(f"[GET /pqr] Usuario: {current_user['user_id']} - Consultando pqr con id={iduser}")
    unit_pqr = controller.get_by_column(PQROut, column_name="iduser", value = iduser)

    if unit_pqr:
        logger.info(f"[GET /pqr] PQR encontrada: {unit_pqr.id}, iduser: {unit_pqr.iduser}")
        context = {
            "request": request,
            "pqrs": unit_pqr,  # Lista de asistencias
        }
    else:
        logger.warning(f"[GET /pqr] No se encontró pqr con iduser={iduser}")
        context = {
            "request": request,
            "pqrs_list": []  # Si no se encontraron asistencias, pasar una lista vacía
        }

    return templates.TemplateResponse(request,"pqrs.html", context)
