import logging
from fastapi import Request, Query, APIRouter, Security, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.asistance import AsistanceOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for asistance-related endpoints
app = APIRouter(prefix="/asistance", tags=["asistance"])

# Initialize universal controller instance


# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "conductor", "supervisor", "mantenimiento"])
):
    """
    Render the 'ConsultarAsistencia.html' template for the asistance consultation page.
    """
    #logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de asistencia")
    return templates.TemplateResponse(request,"ConsultarAsistencia.html", {"request": request})

@app.get("/consultar/user", response_class=HTMLResponse)
def consultar(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Render the 'ConsultarPQR.html' template for the pqr consultation page.
    """
    #logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de pqr")
    return templates.TemplateResponse(request,"ConsultarAsistenciaUsuario.html", {"request": request})

@app.get("/asistencias")
async def get_asistencias(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all asistance records from the database.
    """
    #logger.info(f"[GET /asistencias] Usuario: {current_user['user_id']} - Consultando todas las asistencias.")
    asistencias = controller.read_all(AsistanceOut)
    logger.info(f"[GET /asistencias] Número de asistencias encontradas: {len(asistencias)}")
    context ={
        "request": request,
        "asistencias": asistencias
    }
    return templates.TemplateResponse("asistencias.html", context)

#asistance by id asistance
@app.get("/find", response_class=HTMLResponse)
def asistencia_by_id(
    request: Request,
    id: int = Query(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve a asistance by its ID and render the 'asistencia.html' template with its details.
    If the asistance is not found, display 'None' for all fields.
    """
    #logger.info(f"[GET /asistencia] Usuario: {current_user['user_id']} - Consultando asistencia con id={id}")
    unit_asistencia = controller.get_by_id(AsistanceOut,id)

    if unit_asistencia:
        logger.info(f"[GET /asistencia] Asistencia encontrada: {unit_asistencia.ID}")
    else:
        logger.warning(f"[GET /asistencia] No se encontró asistencia con id={id}")

    context = {
        "request": request,
        "ID": unit_asistencia.ID if unit_asistencia else "None",
        "iduser": unit_asistencia.iduser if unit_asistencia else "None",
        "horainicio":unit_asistencia.horainicio if unit_asistencia else "None",
        "horafinal":unit_asistencia.horafinal if unit_asistencia else "None",
        "fecha":unit_asistencia.fecha if unit_asistencia else "None"
    }

    return templates.TemplateResponse(request,"asistencia.html", context)

#asistance by user id
@app.get("/user", response_class=HTMLResponse)
def asistencia_by_user(
    request: Request,
    iduser: int = Query(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador","conductor","tecnico","supervisor"])
):
    """
    Retrieve a asistance by its ID and render the 'asistencia.html' template with its details.
    If the asistance is not found, display 'None' for all fields.
    """
    #logger.info(f"[GET /asistencia] Usuario: {current_user['user_id']} - Consultando asistencia con id={iduser}")
    asistencias = controller.get_by_column(AsistanceOut, column_name="iduser", value = iduser)

    if asistencias:
        # Si hay varias asistencias, iterar sobre ellas
        context = {
            "request": request,
            "asistencias": asistencias,  # Lista de asistencias
        }
    else:
        logger.warning(f"[GET /asistencia] No se encontraron asistencias con iduser={iduser}")
        context = {
            "request": request,
            "asistencia_list": asistencias  # Si no se encontraron asistencias, pasar una lista vacía
        }

    return templates.TemplateResponse("asistencias.html", context)
