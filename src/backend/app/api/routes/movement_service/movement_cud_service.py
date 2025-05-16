import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security, FastAPI
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.type_movement import TypeMovementCreate, TypeMovementOut
from backend.app.models.movement import MovementCreate, MovementOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/movement", tags=["movement"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/administrador/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(get_current_user,scopes=["system", "administrador"])
):
    #logger.info(f"[GET /crear] Movimiento: {current_user['user_id']} - Mostrando formulario de creación de movimiento")
    try:
        typemovements = controller.read_all(TypeMovementOut)
        movements = controller.read_all(MovementOut)
        ultimo_id = max(p["ID"] for p in movements) if movements else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearAdministradorMovimiento.html", {
        "request": request,
        "nuevo_id": nuevo_id,
        "typemovements":typemovements
    })


@app.get("/administrador/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try: 
        typemovements = controller.read_all(TypeMovementOut)

    #logger.info(f"[GET /actualizar] Movimiento: {current_user['user_id']} - Mostrando formulario de actualización de movimiento")
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        
    return templates.TemplateResponse("ActualizarAdministradorMovimiento.html", {
        "request": request,
        "typemovements":typemovements
    })


@app.get("/administrador/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /eliminar] Movimiento: {current_user['user_id']} - Mostrando formulario de eliminación de movimiento")
    return templates.TemplateResponse("EliminarAdministradorMovimiento.html", {"request": request})


@app.post("/create")
async def create_movement(
    request:Request,
    ID: int = Form(...),
    IDTipoMovimiento:int= Form(...),
    Monto:float=Form(...),
    #current_movement: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /create] Movimiento: {current_movement['user_id']} - Intentando crear movimiento con id: {ID}")

    try:
        # Verificar si el movimiento ya existe
        existing_movement = controller.get_by_column(MovementOut, "ID", ID)  
        if existing_movement:
            logger.warning(f"[POST /create] Error de validación: El movimiento ya existe con identificación {ID}")
            raise HTTPException(400, detail="El movimiento ya existe con la misma identificación.")

        # Crear movimiento
        new_movement = MovementCreate(ID=ID, IDTipoMovimiento=IDTipoMovimiento, Monto=Monto)
        controller.add(new_movement)
        logger.info(f"[POST /create] Movimiento creado exitosamente con identificación {ID}")
        context = {
            "request":request,
            "operation": "create",
            "success": True,
            "data": MovementOut(ID=new_movement.ID,IDTipoMovimiento=new_movement.IDTipoMovimiento,Monto=new_movement.Monto).model_dump(),
            "message": "Movement created successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)
        
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}") 


@app.post("/update")
async def update_movement(
    request:Request,
    ID: int = Form(...),
    IDTipoMovimiento:int=Form(...),
    Monto:float=Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /update] Movimiento: {current_user['user_id']} - Actualizando movimiento id={ID}")
    try:
        existing = controller.get_by_column(MovementOut, "ID",ID)
        if existing is None:
            logger.warning(f"[POST /update] Movimiento no encontrada: id={ID}")
            raise HTTPException(404, detail="Movement not found")

        updated_movement = MovementOut(ID=ID, IDTipoMovimiento=IDTipoMovimiento, Monto=Monto)
        controller.update(updated_movement)
        logger.info(f"[POST /update] Movimiento actualizada exitosamente: {updated_movement}")
        context= {
            "request":request,
            "operation": "update",
            "success": True,
            "data": MovementOut(ID=ID, IDTipoMovimiento=updated_movement.IDTipoMovimiento,Monto=updated_movement.Monto).model_dump(),
            "message": f"Movement {ID} updated successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_movement(
    request:Request,
    ID: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /delete] Movimiento: {current_user['user_id']} - Eliminando movimiento id={ID}")
    try:
        existing = controller.get_by_column(MovementOut, "ID",ID)
        if not existing:
            logger.warning(f"[POST /delete] Movimiento no encontrado en la base de datos: id={ID}")
            raise HTTPException(404, detail="Movement not found")

        controller.delete(existing) 
        logger.info(f"[POST /delete] Movimiento eliminada exitosamente: id={ID}")
        context = {
            "request":request,
            "operation": "delete",
            "success": True,
            "message": f"Movement {ID} deleted successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
