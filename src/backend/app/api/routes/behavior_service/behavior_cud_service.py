import logging, datetime
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.behavior import BehaviorCreate, BehaviorOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/behavior", tags=["behavior"])
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/supervisor/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(
        #get_current_user,
        #scopes=["system", "administrador", "pasajero"])
):
    #logger.info(f"[GET /crear] Usuario: {current_user['user_id']} - Mostrando formulario de creación de PQR")
    try:
        behaviors = controller.read_all(BehaviorOut)
        ultimo_id = max(p["ID"] for p in behaviors) if behaviors else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearSupervisorRendimiento.html", {
        "request": request,
        "nuevo_id": nuevo_id
    })

@app.get("/administrador/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador","supervisor"])
):
    logger.info(f"[GET /actualizar] Rendimiento: {current_user['user_id']} - Mostrando formulario de actualización de rendimiento")
    return templates.TemplateResponse("ActualizarRendimiento.html", {"request": request})


@app.get("/administrador/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /eliminar] Rendimiento: {current_user['user_id']} - Mostrando formulario de eliminación de rendimiento")
    return templates.TemplateResponse("EliminarRendimiento.html", {"request": request})


@app.post("/create")
async def create_behavior(
    request: Request,
    ID: int = Form(...),
    iduser:int= Form(...),
    cantidadrutas: int=Form(...),
    horastrabajadas: int=Form(...),
    observaciones:str=Form(...),
    fecha: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /create] Behavior: {current_user['user_id']} - Intentando crear rendimiento con ID: {ID}")

    try:
        # Verificar si el rendimiento ya existe
        existing_behavior = controller.get_by_id(BehaviorOut, ID)  
        if existing_behavior:
            logger.warning(f"[POST /create] Error de validación: El rendimiento ya existe con identificación {ID}")
            raise HTTPException(400, detail="El rendimiento ya existe con la misma identificación.")

        # Crear rendimiento
        new_behavior = BehaviorCreate(ID=ID, iduser=iduser,cantidadrutas=cantidadrutas, horastrabajadas=horastrabajadas,observaciones=observaciones,fecha=fecha)
        controller.add(new_behavior)
        logger.info(f"Rendimiento insertado con ID: {new_behavior.ID}")  # Verifica si el ID se asigna
        logger.info(f"[POST /create] Rendimiento creado exitosamente con identificación {ID}")
        context =  {
            "operation": "create",
            "success": True,
            "data": BehaviorOut(ID=new_behavior.ID,iduser=new_behavior.iduser,cantidadrutas=new_behavior.cantidadrutas,horastrabajadas=new_behavior.horastrabajadas,observaciones=new_behavior.observaciones,fecha=new_behavior.fecha).model_dump(),
            "message": "Behavior created successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)
        
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_behavior(
    request: Request,
    ID: int = Form(...),
    iduser:int= Form(...),
    cantidadrutas: int=Form(...),
    horastrabajadas: int=Form(...),
    observaciones:str=Form(...),
    fecha: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /update] Rendimiento: {current_user['user_id']} - Actualizando rendimiento ID={ID}")
    try:
        existing = controller.get_by_column(BehaviorOut,"ID" ,ID)
        if existing is None:
            logger.warning(f"[POST /update] Rendimiento no encontrada: ID={ID}")
            raise HTTPException(404, detail="Behavior not found")

        updated_behavior = BehaviorOut(ID=ID, iduser=iduser,cantidadrutas=cantidadrutas,
                                       horastrabajadas=horastrabajadas,
                                       observaciones=observaciones,fecha=fecha)
        controller.update(updated_behavior)
        logger.info(f"[POST /update] Rendimiento actualizada exitosamente: {updated_behavior}")
        context = {
            "operation": "update",
            "success": True,
            "data": BehaviorOut(ID=ID, iduser=updated_behavior.iduser,horastrabajadas=updated_behavior.horastrabajadas, 
                                cantidadrutas=updated_behavior.cantidadrutas,
                                observaciones=updated_behavior.observaciones,
                                fecha=updated_behavior.fecha).model_dump(),
            "message": f"Behavior {ID} updated successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_behavior(
    ID: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /delete] Rendimiento: {current_user['user_id']} - Eliminando rendimiento ID={ID}")
    try:
        existing = controller.get_by_column(BehaviorOut,"ID",ID)
        if not existing:
            logger.warning(f"[POST /delete] Rendimiento no encontrado en la base de datos: ID={ID}")
            raise HTTPException(404, detail="Behavior not found")

        logger.info(f"[POST /delete] Eliminando rendimiento con ID={ID}")
        controller.delete(existing) 
        logger.info(f"[POST /delete] Rendimiento eliminada exitosamente: ID={ID}")
        context= {
            "operation": "delete",
            "success": True,
            "message": f"Behavior {ID} deleted successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
