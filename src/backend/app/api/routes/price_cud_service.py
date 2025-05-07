#import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.price import PriceCreate, PriceOut
from backend.app.logic.universal_controller_sql import UniversalController
#from backend.app.core.auth import get_current_user

# Configuración de logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/price", tags=["price"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(
        #get_current_user,
        #scopes=["system", "administrador"])
):
    #logger.info(f"[GET /crear] Precio: {current_user['user_id']} - Mostrando formulario de creación de precio")
    return templates.TemplateResponse("CrearPrecio.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /actualizar] Precio: {current_user['user_id']} - Mostrando formulario de actualización de precio")
    return templates.TemplateResponse("ActualizarPrecio.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /eliminar] Precio: {current_user['user_id']} - Mostrando formulario de eliminación de precio")
    return templates.TemplateResponse("EliminarPrecio.html", {"request": request})


@app.post("/create")
async def create_price(
    id: int = Form(...),
    unidadtransportype:int= Form(...),
    amount:float=Form(...)
    #current_movement: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /create] Precio: {current_movement['user_id']} - Intentando crear precio con id: {id}")

    try:
        # Verificar si el precio ya existe
        existing_movement = controller.get_by_column(PriceOut, "id", id)  
        if existing_movement:
            #logger.warning(f"[POST /create] Error de validación: El precio ya existe con identificación {id}")
            raise HTTPException(400, detail="El precio ya existe con la misma identificación.")

        # Crear precio
        new_price = PriceCreate(id=id, unidadtransportype=unidadtransportype, amount=amount)
        #logger.info(f"Intentando insertar precio con datos: {new_price.model_dump()}")
        controller.add(new_price)
        #logger.info(f"Precio insertado con ID: {new_price.id}")  # Verifica si el ID se asigna
        #logger.info(f"[POST /create] Precio creado exitosamente con identificación {id}")
        return {
            "operation": "create",
            "success": True,
            "data": PriceOut(id=new_price.id,unidadtransportype=new_price.unidadtransportype,amount=new_price.amount).model_dump(),
            "message": "Price created successfully."
        }
        
    except ValueError as e:
        #logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        #logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_price(
    id: int = Form(...),
    unidadtransportype:int=Form(...),
    amount:float=Form(...)
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /update] Precio: {current_user['user_id']} - Actualizando precio id={id}")
    try:
        existing = controller.get_by_id(PriceOut, id)
        if existing is None:
            #logger.warning(f"[POST /update] Precio no encontrada: id={id}")
            raise HTTPException(404, detail="Price not found")

        updated_price = PriceOut(id=id, unidadtransportype=unidadtransportype, amount=amount)
        controller.update(updated_price)
        #logger.info(f"[POST /update] Precio actualizada exitosamente: {updated_price}")
        return {
            "operation": "update",
            "success": True,
            "data": PriceOut(id=id, unidadtransportype=updated_price.unidadtransportype,amount=updated_price.amount).model_dump(),
            "message": f"Price {id} updated successfully."
        }
    except ValueError as e:
        #logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_price(
    id: int = Form(...)
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /delete] Precio: {current_user['user_id']} - Eliminando precio id={id}")
    try:
        existing = controller.get_by_id(PriceOut, id)
        if not existing:
            #logger.warning(f"[POST /delete] Precio no encontrado en la base de datos: id={id}")
            raise HTTPException(404, detail="Price not found")

        #logger.info(f"[POST /delete] Eliminando precio con id={id}")
        controller.delete(existing) 
        #logger.info(f"[POST /delete] Precio eliminada exitosamente: id={id}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"Price {id} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        #logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
