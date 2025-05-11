#import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.type_transport import TypeTransportCreate,TypeTransportOut
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.auth import get_current_user

# Configuración de logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/typetransport", tags=["typetransport"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(get_current_user,
        #scopes=["system", "administrador"])
):
    #logger.info(f"[GET /crear] Usuario: {current_user['user_id']} - Mostrando formulario de creación de tipo de transporte")
    return templates.TemplateResponse("CrearTipoTransporte.html", {"request": request})

@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /actualizar] Usuario: {current_user['user_id']} - Mostrando formulario de actualización de tipo de transporte")
    return templates.TemplateResponse("ActualizarTipoTransporte.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /eliminar] Usuario: {current_user['user_id']} - Mostrando formulario de eliminación de tipo de transporte")
    return templates.TemplateResponse("EliminarTipoTransporte.html", {"request": request})

#
@app.post("/create")
async def create_typetransport(
    id: int = Form(...),
    TipoTransporte: str = Form(...)
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /create] Usuario: {current_user['user_id']} - Intentando crear tipo de transporte {TipoTransporte}")

    try:
        # Verificar si el tipo de transporte ya existe
        existing_transport = controller.get_by_column(TypeTransportOut, "TipoTransporte", TipoTransporte)  
        if existing_transport:
            #logger.warning(f"[POST /create] Error de validación: El tipo de transporte ya existe con id {id}")
            raise HTTPException(400, detail="El tipo de transporte ya existe con la misma identificación.")

        # Crear tipo de transporte
        new_typetransport = TypeTransportCreate(id=id, TipoTransporte=TipoTransporte)
        #logger.info(f"Intentando insertar rol de usuario con datos: {new_typetransport.model_dump()}")
        controller.add(new_typetransport)
        #logger.info(f"Rol de Usuario insertado con ID: {new_typetransport.id}")  # Verifica si el ID se asigna
        #logger.info(f"[POST /create] Tipo de Transporte creado exitosamente con identificación {id}")
        return {
            "operation": "create",
            "success": True,
            "data": TypeTransportOut(id=new_typetransport.id, TipoTransporte=new_typetransport.TipoTransporte).model_dump(),
            "message": "TypeTransport created successfully."
        }
        
    except ValueError as e:
        #logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        #logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_typetransport(
    id: int = Form(...),
    TipoTransporte: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /update] Usuario: {current_user['user_id']} - Actualizando tipo de transporte id={id}")
    try:
        existing = controller.get_by_id(TypeTransportOut, id)
        if existing is None:
            #logger.warning(f"[POST /update] Tipo de Transporte no encontrada: id={id}")
            raise HTTPException(404, detail="TypeTransport not found")

        updated_typetransport = TypeTransportOut(id=id, TipoTransporte=TipoTransporte)
        controller.update(updated_typetransport)
        #logger.info(f"[POST /update] TipoTransporte actualizada exitosamente: {updated_typetransport}")
        return {
            "operation": "update",
            "success": True,
            "data": TypeTransportOut(id=id, TipoTransporte=updated_typetransport.TipoTransporte).model_dump(),
            "message": f"TypeTransport {id} updated successfully."
        }
    except ValueError as e:
        #logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_roluser(
    id: int = Form(...)
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /delete] Usuario: {current_user['user_id']} - Eliminando tipo de transporte con id={id}")
    try:
        existing = controller.get_by_id(TypeTransportOut, id)
        if not existing:
            #logger.warning(f"[POST /delete] Tipo de transporte no encontrado en la base de datos: id={id}")
            raise HTTPException(404, detail="TypeTransport not found")

        #logger.info(f"[POST /delete] Eliminando tipo de transporte con id={id}")
        controller.delete(existing) 
        #logger.info(f"[POST /delete] Tipo de Transporte eliminada exitosamente: id={id}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"TypeTransport {id} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        #logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
