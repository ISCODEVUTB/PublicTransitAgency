import logging, datetime
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.asistance import AsistanceCreate, AsistanceOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/asistance", tags=["asistance"])
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    current_user: dict = Security(
        get_current_user,
        scopes=["system", "administrador", "supervisor","tecnico","conductor"]
    )
):
    logger.info(f"[GET /crear] Asistencia: {current_user['user_id']} - Mostrando formulario de creación de asistencia")
    return templates.TemplateResponse("CrearAsistencia.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[GET /actualizar] Asistencia: {current_user['user_id']} - Mostrando formulario de actualización de asistencia")
    return templates.TemplateResponse("ActualizarAsistencia.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[GET /eliminar] Asistencia: {current_user['user_id']} - Mostrando formulario de eliminación de asistencia")
    return templates.TemplateResponse("EliminarAsistencia.html", {"request": request})


@app.post("/create")
async def create_asistance(
    id: int = Form(...),
    iduser:int= Form(...),
    horainicio: str = Form(...),
    horafinal: str = Form(...),
    fecha: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /create] Asistance: {current_user['user_id']} - Intentando crear asistencia con id: {id}")

    try:
        # Verificar si el asistencia ya existe
        existing_asistance = controller.get_by_column(AsistanceOut, "id", id)  
        if existing_asistance:
            logger.warning(f"[POST /create] Error de validación: El asistencia ya existe con identificación {id}")
            raise HTTPException(400, detail="El asistencia ya existe con la misma identificación.")
        if existing_asistance is None or not existing_asistance:
            # Crear asistencia
            new_asistance = AsistanceCreate(id=id, iduser=iduser,horainicio=horainicio,horafinal=horafinal,fecha=fecha)
            logger.info(f"Intentando insertar asistencia con datos: {new_asistance.model_dump()}")
            controller.add(new_asistance)
            logger.info(f"Asistencia insertado con id: {new_asistance.id}")  # Verifica si el ID se asigna
            logger.info(f"[POST /create] Asistencia creado exitosamente con identificación {id}")
            return {
                "operation": "create",
                "success": True,
                "data": AsistanceOut(id=new_asistance.id,iduser=new_asistance.iduser,
                                    horainicio=new_asistance.horainicio,
                                    horafinal=new_asistance.horafinal,
                                    fecha=new_asistance.fecha).model_dump(),
                "message": "Asistance created successfully."
            }
        
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_asistance(
    id: int = Form(...),
    iduser:int= Form(...),
    horainicio: str = Form(...),
    horafinal: str = Form(...),
    fecha: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /update] Asistencia: {current_user['user_id']} - Actualizando asistencia id={id}")
    try:
        existing = controller.get_by_column(AsistanceOut,"id" ,id)
        if existing is None or not existing:
            logger.warning(f"[POST /update] Asistencia no encontrada: id={id}")
            raise HTTPException(404, detail="Asistance not found")

        updated_asistance = AsistanceOut(id=id, iduser=iduser,
                                         horainicio=horainicio,
                                         horafinal=horafinal,
                                         fecha=fecha)
        controller.update(updated_asistance)
        logger.info(f"[POST /update] Asistencia actualizada exitosamente: {updated_asistance}")
        return {
            "operation": "update",
            "success": True,
            "data": AsistanceOut(id=id, iduser=updated_asistance.iduser,
                                 horainicio=updated_asistance.horainicio, 
                                 horafinal=updated_asistance.horafinal,
                                 fecha=updated_asistance.fecha).model_dump(),
            "message": f"Asistance {id} updated successfully."
        }
    except ValueError as e:
        if "No se encontró ningún registro" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_asistance(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /delete] Asistencia: {current_user['user_id']} - Eliminando asistencia id={id}")
    try:
        existing = controller.get_by_column(AsistanceOut,"id" ,id)
        if not existing:
            logger.warning(f"[POST /delete] Asistencia no encontrado en la base de datos: id={id}")
            raise HTTPException(404, detail="Asistance not found")

        logger.info(f"[POST /delete] Eliminando asistencia con id={id}")
        controller.delete(existing) 
        logger.info(f"[POST /delete] Asistencia eliminada exitosamente: id={id}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"Asistance {id} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
