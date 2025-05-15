import logging
from fastapi import Request, Query, APIRouter, Security, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.behavior import BehaviorOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for behavior-related endpoints
app = APIRouter(prefix="/behavior", tags=["behavior"])

# Initialize universal controller instance

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=[
        "system", "administrador"
    ])
):
    """
    Render the 'ConsultarRendimiento.html' template for the behavior consultation page.
    """
    logger.info(f"[GET /consultar] Usuario: {current_user['user_id']} - Mostrando página de consulta de rendimiento")
    return templates.TemplateResponse(request,"ConsultarRendimiento.html", {"request": request})

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
    return templates.TemplateResponse(request,"ConsultarRendimientoUsuario.html", {"request": request})



@app.get("/rendimientos")
async def get_rendimientos(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all behavior records from the database.
    """
    logger.info(f"[GET /rendimientos] Usuario: {current_user['user_id']} - Consultando todas las rendimientos.")
    rendimientos = controller.read_all(BehaviorOut)
    logger.info(f"[GET /rendimientos] Número de rendimientos encontradas: {len(rendimientos)}")
    return rendimientos

#behavior by id behavior
@app.get("/rendimiento", response_class=HTMLResponse)
def rendimiento_by_id(
    request: Request,
    id: int =Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve a behavior by its ID and render the 'rendimiento.html' template with its details.
    If the behavior is not found, display 'None' for all fields.
    """
    logger.info(f"[GET /rendimiento] Usuario: {current_user['user_id']} - Consultando rendimiento con id={id}")
    unit_rendimiento = controller.get_by_id(BehaviorOut, id)

    if unit_rendimiento:
        logger.info(f"[GET /rendimiento] Rendimiento encontrada: {unit_rendimiento.id}, iduser: {unit_rendimiento.iduser}")
    else:
        logger.warning(f"[GET /rendimiento] No se encontró rendimiento con id={id}")

    context = {
        "request": request,
        "id": unit_rendimiento.id if unit_rendimiento else "None",
        "iduser": unit_rendimiento.iduser if unit_rendimiento else "None",
        "cantidadrutas": unit_rendimiento.cantidadrutas if unit_rendimiento else "None",
        "horastrabajadas": unit_rendimiento.horastrabajadas if unit_rendimiento else "None",
        "observaciones":unit_rendimiento.observaciones if unit_rendimiento else "None",
        "fecha": unit_rendimiento.fecha if unit_rendimiento else "None",
    }

    return templates.TemplateResponse(request,"rendimiento.html", context)

#behavior by user id
@app.get("/user", response_class=HTMLResponse)
def rendimiento_by_user(
    request: Request,
    iduser: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador","supervisor"])
):
    """
    Retrieve a behavior by its ID and render the 'rendimiento.html' template with its details.
    If the behavior is not found, display 'None' for all fields.
    """
    logger.info(f"[GET /rendimiento] Usuario: {current_user['user_id']} - Consultando rendimiento con id={iduser}")
    unit_rendimiento = controller.get_by_column(BehaviorOut, column_name="iduser", value = iduser)

    if unit_rendimiento:
        # Si hay varias asistencias, iterar sobre ellas
        context = {
            "request": request,
            "asistencias": unit_rendimiento,  # Lista de asistencias
        }
    else:
        logger.warning(f"[GET /asistencia] No se encontraron asistencias con iduser={iduser}")
        context = {
            "request": request,
            "rendimientos_list": []  # Si no se encontraron asistencias, pasar una lista vacía
        }
    return templates.TemplateResponse(request,"rendimientos.html", context)
