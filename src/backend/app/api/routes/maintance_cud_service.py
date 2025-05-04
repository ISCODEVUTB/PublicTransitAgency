import logging
from fastapi import APIRouter, Form, Request, HTTPException, Security, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from backend.app.models.maintainance import MaintenanceCreate, MaintenanceOut
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.auth import get_current_user, verify_token_and_scope
from jose import jwt, JWTError
from backend.app.core.config import settings

# Initialize the controller and templates
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Define the APIRouter with a prefix and tags
app = APIRouter(prefix="/maintainance", tags=["maintainance"])

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.get("/maintenance/token_info", response_model=dict[str, str])
async def maintenance_token_info(request: Request, token_info= get_current_user):
    return {"token_info": token_info}

@app.get("/crear", response_class=HTMLResponse)
def crear_mantenimiento(
    request: Request,
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "tecnico", "administrador"])
    logger.info(f"[GET /crear] Usuario {user_id} accede al formulario para crear mantenimiento.")
    return templates.TemplateResponse("CrearMantenimiento.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_mantenimiento(
    request: Request,
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "tecnico", "administrador"])
    logger.info(f"[GET /eliminar] Usuario {user_id} accede al formulario para eliminar mantenimiento.")
    return templates.TemplateResponse("EliminarMantenimiento.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_mantenimiento(
    request: Request,
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "tecnico"])
    logger.info(f"[GET /actualizar] Usuario {user_id} accede al formulario para actualizar mantenimiento.")
    return templates.TemplateResponse("ActualizarMantenimiento.html", {"request": request})


@app.post("/create")
async def add(
    id_unit: int = Form(...),
    id_status: int = Form(...),
    type: str = Form(...),
    date: datetime = Form(...),
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "administrador", "tecnico"])
    logger.info(f"[POST /create] Usuario {user_id} intenta crear mantenimiento: {id_unit}, {type}, {date}")

    maintenance_temp = MaintenanceCreate(
        id_unit=id_unit, id_status=id_status, type=type, date=date
    )

    try:
        controller.add(maintenance_temp)
        logger.info(f"[POST /create] Mantenimiento con ID {maintenance_temp.id_unit} creado con éxito.")
        return {"message": "Maintenance added successfully"}
    except Exception as e:
        logger.error(f"[POST /create] Error al crear mantenimiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update")
async def update(
    id: int = Form(...),
    id_unit: int = Form(...),
    id_status: int = Form(...),
    type: str = Form(...),
    date: datetime = Form(...),
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "administrador", "tecnico"])
    logger.info(f"[POST /update] Usuario {user_id} intenta actualizar mantenimiento con ID {id}.")

    existing_maintenance = controller.get_by_id(MaintenanceOut, id)
    if not existing_maintenance:
        logger.warning(f"[POST /update] No se encontró mantenimiento con ID {id}.")
        raise HTTPException(status_code=404, detail="Maintenance not found")

    maintenance_temp = MaintenanceCreate(
        id=id,
        id_unit=id_unit,
        id_status=id_status,
        type=type,
        date=date
    )

    try:
        controller.update(maintenance_temp)
        logger.info(f"[POST /update] Mantenimiento con ID {id} actualizado con éxito.")
        return {"message": f"Maintenance {id} updated successfully"}
    except Exception as e:
        logger.error(f"[POST /update] Error al actualizar mantenimiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/delete")
async def delete_maintenance(
    id: int = Form(...),
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "administrador", "tecnico"])
    logger.info(f"[POST /delete] Usuario {user_id} intenta eliminar mantenimiento con ID {id}.")

    try:
        existing_maintenance = controller.get_by_id(MaintenanceOut, id)
        if not existing_maintenance:
            logger.warning(f"[POST /delete] No se encontró mantenimiento con ID {id}.")
            raise HTTPException(status_code=404, detail="Maintenance not found")

        controller.delete(existing_maintenance)
        logger.info(f"[POST /delete] Mantenimiento con ID {id} eliminado con éxito.")
        return {"message": f"Maintenance {id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[POST /delete] Error al eliminar mantenimiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))