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
    #current_user: dict = Security(get_current_user, scopes=[
        #"system", "administrador", "pasajero"])
):
    """
    Render the 'ConsultarPQR.html' template for the pqr consultation page.
    """
    #logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de pqr")
    return templates.TemplateResponse(request,"ConsultarPQR.html", {"request": request})

@app.get("/consultar/administrador", response_class=HTMLResponse)
def consultar(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=[
        #"system", "administrador", "pasajero"])
):
    """
    Render the 'ConsultarPQR.html' template for the pqr consultation page.
    """
    #logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de pqr")
    return templates.TemplateResponse(request,"ConsultarPQRViaAdministrador.html", {"request": request})


@app.get("/consultar/pasajero", response_class=HTMLResponse)
def consultar(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=[
        #"system", "administrador"])
):
    """
    Render the 'ConsultarPQR.html' template for the pqr consultation page.
    """
    #logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de pqr")
    return templates.TemplateResponse(request,"ConsultarPQRViaPasajero.html", {"request": request})


@app.get("/pasajero/pqrs")
async def get_pqrs(
    request:Request
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all pqr records from the database.
    """
    #logger.info(f"[GET /pqrs] Usuario: {current_user['user_id']} - Consultando todas las pqrs.")
    pqrs = controller.read_all(PQROut)
    if pqrs:
        # Si hay varias asistencias, iterar sobre ellas
        context = {
            "request": request,
            "pqrs": pqrs,  # Lista de asistencias
        }
    else:
        logger.warning(f"[GET /pqrs] No se encontraron usuarios registrados")
        context = {
            "request": request,
            "pqrs": []  # Si no se encontraron usuarios
        }
    return templates.TemplateResponse("Pasajeropqrs.html", context)

@app.get("/administrador/pqrs")
async def get_pqrs(
    request:Request
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all pqr records from the database.
    """
    #logger.info(f"[GET /pqrs] Usuario: {current_user['user_id']} - Consultando todas las pqrs.")
    pqrs = controller.read_all(PQROut)
    if pqrs:
        # Si hay varias asistencias, iterar sobre ellas
        context = {
            "request": request,
            "pqrs": pqrs,  # Lista de asistencias
        }
    else:
        logger.warning(f"[GET /pqrs] No se encontraron usuarios registrados")
        context = {
            "request": request,
            "pqrs": []  # Si no se encontraron usuarios
        }
    return templates.TemplateResponse("Administradorpqrs.html", context)

#pqr by codigogenerado pqr
@app.get("/find", response_class=HTMLResponse)
def pqr_by_id(
    request: Request,
    ID: int = Query(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve a pqr by its ID and render the 'pqr.html' template with its details.
    If the pqr is not found, display 'None' for all fields.
    """
    #logger.info(f"[GET /pqr] Usuario: {current_user['user_id']} - Consultando pqr con ID={ID}")
    unit_pqr = controller.get_by_column(PQROut, "ID",ID)

    if unit_pqr:
        logger.info(f"[GET /pqr] PQR encontrada: {unit_pqr.ID}")
    else:
        logger.warning(f"[GET /pqr] No se encontró pqr con ID={ID}")

    context = {
        "request": request,
        "ID": unit_pqr.ID if unit_pqr else "None",
        "iduser": unit_pqr.iduser if unit_pqr else "None",
        "type": unit_pqr.type if unit_pqr else "None",
        "description": unit_pqr.description if unit_pqr else "None",
        "fecha": unit_pqr.fecha if unit_pqr else "None",
    }

    return templates.TemplateResponse(request,"pqr.html", context)

#pqr by user ID
@app.get("/user", response_class=HTMLResponse)
def pqr_by_user(
    request: Request,
    iduser: int = Query(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador","pasajero"])
):
    """
    Retrieve a pqr by its ID and render the 'pqr.html' template with its details.
    If the pqr is not found, display 'None' for all fields.
    """
    #logger.info(f"[GET /pqr] Usuario: {current_user['user_id']} - Consultando pqr con ID={iduser}")
    unit_pqr = controller.get_by_column(PQROut, column_name="iduser", value = iduser)

    if unit_pqr:
        logger.info(f"[GET /pqr] PQR encontrada: {unit_pqr.ID}, iduser: {unit_pqr.iduser}")
        context = {
            "request": request,
            "pqrs": unit_pqr,  # Lista de asistencias
        }
    else:
        logger.warning(f"[GET /pqr] No se encontró pqr con iduser={iduser}")
        context = {
            "request": request,
            "pqrs": []  # Si no se encontraron asistencias, pasar una lista vacía
        }

    return templates.TemplateResponse(request,"pqrs.html", context)
