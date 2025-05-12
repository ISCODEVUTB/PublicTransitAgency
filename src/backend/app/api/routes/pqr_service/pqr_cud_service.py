import logging, datetime
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.pqr import PQRCreate, PQROut
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/user", tags=["user"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    current_user: dict = Security(
        get_current_user,
        scopes=["system", "administrador", "pasajero"]
    )
):
    logger.info(f"[GET /crear] Usuario: {current_user['user_id']} - Mostrando formulario de creación de PQR")
    return templates.TemplateResponse("CrearPQR.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[GET /actualizar] Usuario: {current_user['user_id']} - Mostrando formulario de actualización de PQR")
    return templates.TemplateResponse("ActualizarPQR.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[GET /eliminar] Usuario: {current_user['user_id']} - Mostrando formulario de eliminación de PQR")
    return templates.TemplateResponse("EliminarPQR.html", {"request": request})


@app.post("/create")
async def create_pqr(
    id: int = Form(...),
    type: str  = Form(...),
    description: str  = Form(...),
    fecha: datetime.date = Form(...),
    identificationuser: int  = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "pasajero"])
):
    logger.info(f"[POST /create] Usuario: {current_user['user_id']} - Intentando crear PQR con identificación {id}")

    try:
        # Verificar si el PQR ya existe
        existing_user = controller.get_by_column(PQROut, "id", id)  
        if existing_user:
            logger.warning(f"[POST /create] Error de validación: El PQR ya existe con id {id}")
            raise HTTPException(400, detail="El PQR ya existe con la misma identificación.")

        # Crear PQR
        new_pqr = PQRCreate(id=id, type=type, description=description, fecha=fecha,identificationuser=identificationuser)
        logger.info(f"Intentando insertar PQR con datos: {new_pqr.model_dump()}")
        controller.add(new_pqr)
        logger.info(f"PQR insertado con ID: {new_pqr.id}")  # Verifica si el ID se asigna
        logger.info(f"[POST /create] Usuario creado exitosamente con id {id}")
        return {
            "operation": "create",
            "success": True,
            "data": PQROut(id=new_pqr.id, type=new_pqr.type, description=new_pqr.description,
                            fecha=new_pqr.fecha,identificationuser=new_pqr.identificationuser).model_dump(),
            "message": "PQR created successfully."
        }
        
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_pqr(
    id: int = Form(...),
    type: str  = Form(...),
    description: str  = Form(...),
    fecha: datetime.date = Form(...),
    identificationuser: int  = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /update] Usuario: {current_user['user_id']} - Actualizando PQR id={id}")
    try:
        existing = controller.get_by_id(PQROut, id)
        if existing is None:
            logger.warning(f"[POST /update] PQR no encontrada: id={id}")
            raise HTTPException(404, detail="PQR not found")

        updated_pqr = PQROut(id=id, type=type,description=description,fecha=fecha,identificationuser=identificationuser)
        controller.update(updated_pqr)
        logger.info(f"[POST /update] PQR actualizada exitosamente: {updated_pqr}")
        return {
            "operation": "update",
            "success": True,
            "data": PQROut(id=updated_pqr.id, type=updated_pqr.type, description=updated_pqr.description,
                            fecha=updated_pqr.fecha,identificationuser=updated_pqr.identificationuser).model_dump(),
            "message": f"PQR {id} updated successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_user(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /delete] Usuario: {current_user['user_id']} - Eliminando PQR id={id}")
    try:
        existing = controller.get_by_id(PQROut, id)
        if not existing:
            logger.warning(f"[POST /delete] PQR no encontrado en la base de datos: id={id}")
            raise HTTPException(404, detail="PQR not found")

        logger.info(f"[POST /delete] Eliminando PQR con id={id}")
        controller.delete(existing) 
        logger.info(f"[POST /delete] PQR eliminada exitosamente: id={id}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"PQR {id} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
