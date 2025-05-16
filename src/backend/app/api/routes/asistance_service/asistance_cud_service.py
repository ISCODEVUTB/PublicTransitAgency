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



@app.get("/administrador/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(
        #get_current_user,scopes=["system", "administrador", "supervisor","tecnico","conductor"])
):
    #logger.info(f"[GET /crear] Asistencia: {current_user['user_id']} - Mostrando formulario de creación de asistencia")
    try:
        asistances = controller.read_all(AsistanceOut)
        ultimo_id = max(p["ID"] for p in asistances) if asistances else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearAdministradorAsistencia.html", {
        "request": request,
        "nuevo_id": nuevo_id
    })

@app.get("/conductor/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(
        #get_current_user,scopes=["system", "administrador", "supervisor","tecnico","conductor"])
):
    #logger.info(f"[GET /crear] Asistencia: {current_user['user_id']} - Mostrando formulario de creación de asistencia")
    try:
        asistances = controller.read_all(AsistanceOut)
        ultimo_id = max(p["ID"] for p in asistances) if asistances else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearConductorAsistencia.html", {
        "request": request,
        "nuevo_id": nuevo_id
    })

@app.get("/supervisor/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(
        #get_current_user,scopes=["system", "administrador", "supervisor","tecnico","conductor"])
):
    #logger.info(f"[GET /crear] Asistencia: {current_user['user_id']} - Mostrando formulario de creación de asistencia")
    try:
        asistances = controller.read_all(AsistanceOut)
        ultimo_id = max(p["ID"] for p in asistances) if asistances else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearSupervisorAsistencia.html", {
        "request": request,
        "nuevo_id": nuevo_id
    })

@app.get("/tecnico/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(
        #get_current_user,scopes=["system", "administrador", "supervisor","tecnico","conductor"])
):
    #logger.info(f"[GET /crear] Asistencia: {current_user['user_id']} - Mostrando formulario de creación de asistencia")
    try:
        asistances = controller.read_all(AsistanceOut)
        ultimo_id = max(p["ID"] for p in asistances) if asistances else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearTecnicoAsistencia.html", {
        "request": request,
        "nuevo_id": nuevo_id
    })


@app.get("/administrador/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /actualizar] Asistencia: {current_user['user_id']} - Mostrando formulario de actualización de asistencia")
    return templates.TemplateResponse("ActualizarAdministradorAsistencia.html", {"request": request})


@app.get("/administrador/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /eliminar] Asistencia: {current_user['user_id']} - Mostrando formulario de eliminación de asistencia")
    return templates.TemplateResponse("EliminarAdministradorAsistencia.html", {"request": request})


@app.post("/create")
async def create_asistance(
    request: Request,
    ID: int = Form(...),
    iduser:int= Form(...),
    horainicio: str = Form(...),
    horafinal: str = Form(...),
    fecha: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /create] Asistance: {current_user['user_id']} - Intentando crear asistencia con ID: {ID}")

    try:
        # Verificar si el asistencia ya existe
        existing_asistance = controller.get_by_column(AsistanceOut,"ID" ,ID)  
        if existing_asistance:
            logger.warning(f"[POST /create] Error de validación: El asistencia ya existe con identificación {ID}")
            raise HTTPException(400, detail="El asistencia ya existe con la misma identificación.")
        if existing_asistance is None or not existing_asistance:
            # Crear asistencia
            new_asistance = AsistanceCreate(ID=ID, iduser=iduser,horainicio=horainicio,horafinal=horafinal,fecha=fecha)
            controller.add(new_asistance)
            logger.info(f"[POST /create] Asistencia creado exitosamente con identificación {ID}")
            context = {
                "request": request,
                "operation": "create",
                "success": True,
                "data": AsistanceOut(ID=new_asistance.ID,iduser=new_asistance.iduser,
                                    horainicio=new_asistance.horainicio,
                                    horafinal=new_asistance.horafinal,
                                    fecha=new_asistance.fecha).model_dump(),
                "message": "Asistance created successfully."
            }
            return templates.TemplateResponse("Confirmacion.html", context)
        
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_asistance(
    request: Request,
    ID: int = Form(...),
    iduser:int= Form(...),
    horainicio: str = Form(...),
    horafinal: str = Form(...),
    fecha: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /update] Asistencia: {current_user['user_id']} - Actualizando asistencia ID={ID}")
    try:
        existing = controller.get_by_column(AsistanceOut,"ID" ,ID) 
        if existing is None or not existing:
            logger.warning(f"[POST /update] Asistencia no encontrada: ID={ID}")
            raise HTTPException(404, detail="Asistance not found")

        updated_asistance = AsistanceOut(ID=ID, iduser=iduser,
                                         horainicio=horainicio,
                                         horafinal=horafinal,
                                         fecha=fecha)
        controller.update(updated_asistance)
        logger.info(f"[POST /update] Asistencia actualizada exitosamente: {updated_asistance}")
        context=  {
            "request":request,
            "operation": "update",
            "success": True,
            "data": AsistanceOut(ID=ID, iduser=updated_asistance.iduser,
                                 horainicio=updated_asistance.horainicio, 
                                 horafinal=updated_asistance.horafinal,
                                 fecha=updated_asistance.fecha).model_dump(),
            "message": f"Asistance {ID} updated successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)

    except ValueError as e:
        if "No se encontró ningún registro" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_asistance(
    request:Request,
    ID: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /delete] Asistencia: {current_user['user_id']} - Eliminando asistencia ID={ID}")
    try:
        existing = controller.get_by_column(AsistanceOut, "ID" ,ID) 
        if not existing:
            logger.warning(f"[POST /delete] Asistencia no encontrado en la base de datos: ID={ID}")
            raise HTTPException(404, detail="Asistance not found")
        
        controller.delete(existing) 
        logger.info(f"[POST /delete] Asistencia eliminada exitosamente: ID={ID}")
        context= {
            "request":request,
            "operation": "delete",
            "success": True,
            "message": f"Asistance {ID} deleted successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
