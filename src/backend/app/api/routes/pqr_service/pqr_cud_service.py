import logging, datetime
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.pqr import PQRCreate, PQROut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/user", tags=["user"])
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/administrador/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(
        #get_current_user,
        #scopes=["system", "administrador", "pasajero"])
):
    #logger.info(f"[GET /crear] Usuario: {current_user['user_id']} - Mostrando formulario de creación de PQR")
    try:
        pqrs = controller.read_all(PQROut)
        ultimo_id = max(p["ID"] for p in pqrs) if pqrs else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearAdministradorPQR.html", {
        "request": request,
        "nuevo_id": nuevo_id
    })

@app.get("/pasajero/crear", response_class=HTMLResponse)
@app.get("/administrador/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(
        #get_current_user,
        #scopes=["system", "administrador", "pasajero"])
):
    #logger.info(f"[GET /crear] Usuario: {current_user['user_id']} - Mostrando formulario de creación de PQR")
    try:
        pqrs = controller.read_all(PQROut)
        ultimo_id = max(p["ID"] for p in pqrs) if pqrs else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearAdministradorPQR.html", {
        "request": request,
        "nuevo_id": nuevo_id
    })

@app.get("/pasajero/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(
        #get_current_user,
        #scopes=["system", "administrador", "pasajero"])
    #current_user: dict = Security(
        #get_current_user,
        #scopes=["system", "administrador", "pasajero"])
):
    #logger.info(f"[GET /crear] Usuario: {current_user['user_id']} - Mostrando formulario de creación de PQR")
    try:
        pqrs = controller.read_all(PQROut)
        ultimo_id = max(p["ID"] for p in pqrs) if pqrs else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearPasajeroPQR.html", {
        "request": request,
        "nuevo_id": nuevo_id
    })
    #logger.info(f"[GET /crear] Usuario: {current_user['user_id']} - Mostrando formulario de creación de PQR")
    try:
        pqrs = controller.read_all(PQROut)
        ultimo_id = max(p["ID"] for p in pqrs) if pqrs else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearPasajeroPQR.html", {
        "request": request,
        "nuevo_id": nuevo_id
    })


@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /actualizar] Usuario: {current_user['user_id']} - Mostrando formulario de actualización de PQR")
    #logger.info(f"[GET /actualizar] Usuario: {current_user['user_id']} - Mostrando formulario de actualización de PQR")
    return templates.TemplateResponse("ActualizarPQR.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /eliminar] Usuario: {current_user['user_id']} - Mostrando formulario de eliminación de PQR")
    #logger.info(f"[GET /eliminar] Usuario: {current_user['user_id']} - Mostrando formulario de eliminación de PQR")
    return templates.TemplateResponse("EliminarPQR.html", {"request": request})


@app.post("/create")
async def create_pqr(
    ID: int = Form(...),
    type: str  = Form(...),
    description: str  = Form(...),
    fecha: str = Form(...),
    identificationuser: int  = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "pasajero"])
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "pasajero"])
):
    #logger.info(f"[POST /create] Usuario: {current_user['user_id']} - Intentando crear PQR con identificación {ID}")
    #logger.info(f"[POST /create] Usuario: {current_user['user_id']} - Intentando crear PQR con identificación {ID}")
    try:
        # Verificar si el PQR ya existe
        existing_user = controller.get_by_column(PQROut, "ID", ID)  
        if existing_user:
            logger.warning(f"[POST /create] Error de validación: El PQR ya existe con ID {ID}")
            raise HTTPException(400, detail="El PQR ya existe con la misma identificación.")

        # Crear PQR
        new_pqr = PQRCreate(ID=ID, type=type, description=description, fecha=fecha,identificationuser=identificationuser)
        logger.info(f"Intentando insertar PQR con datos: {new_pqr.model_dump()}")
        controller.add(new_pqr)
        logger.info(f"PQR insertado con ID: {new_pqr.ID}")  # Verifica si el ID se asigna
        logger.info(f"[POST /create] Usuario creado exitosamente con ID {ID}")
        return {
            "operation": "create",
            "success": True,
            "data": PQROut(ID=new_pqr.ID, type=new_pqr.type, description=new_pqr.description,
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
    ID: int = Form(...),
    type: str  = Form(...),
    description: str  = Form(...),
    fecha: str = Form(...),
    identificationuser: int  = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /update] Usuario: {current_user['user_id']} - Actualizando PQR ID={ID}")
    try:
        existing = controller.get_by_id(PQROut, ID)
        if existing is None:
            logger.warning(f"[POST /update] PQR no encontrada: ID={ID}")
            raise HTTPException(404, detail="PQR not found")

        updated_pqr = PQROut(ID=ID, type=type,description=description,fecha=fecha,identificationuser=identificationuser)
        controller.update(updated_pqr)
        logger.info(f"[POST /update] PQR actualizada exitosamente: {updated_pqr}")
        return {
            "operation": "update",
            "success": True,
            "data": PQROut(ID=updated_pqr.ID, type=updated_pqr.type, description=updated_pqr.description,
                            fecha=updated_pqr.fecha,identificationuser=updated_pqr.identificationuser).model_dump(),
            "message": f"PQR {ID} updated successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_pqr(
    ID: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /delete] Usuario: {current_user['user_id']} - Eliminando PQR ID={ID}")
    try:
        existing = controller.get_by_column(PQROut,"ID" ,ID)
        if not existing:
            logger.warning(f"[POST /delete] PQR no encontrado en la base de datos")
            raise HTTPException(404, detail="PQR not found")

        logger.info(f"[POST /delete] Eliminando PQR")
        controller.delete(existing) 
        logger.info(f"[POST /delete] PQR eliminada exitosamente:")
        return {
            "operation": "delete",
            "success": True,
            "message": f"PQR {ID} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
