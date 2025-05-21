import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security, FastAPI
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.price import PriceCreate, PriceOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/price", tags=["price"])

templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/administrador/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    current_user: dict = Security(get_current_user,scopes=["system", "administrador"])
):
    #logger.info(f"[GET /crear] Precio: {current_user['user_id']} - Mostrando formulario de creación de precio")
    try:
        prices = controller.read_all(PriceOut)
        ultimo_id = max(p["ID"] for p in prices) if prices else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return templates.TemplateResponse("CrearAdministradorPrecio.html", {
        "request": request,
        "nuevo_id": nuevo_id
    })


@app.get("/administrador/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /actualizar] Precio: {current_user['user_id']} - Mostrando formulario de actualización de precio")
    return templates.TemplateResponse("ActualizarAdministradorPrecio.html", {"request": request})


@app.get("/administrador/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /eliminar] Precio: {current_user['user_id']} - Mostrando formulario de eliminación de precio")
    return templates.TemplateResponse("EliminarAdministradorPrecio.html", {"request": request})


@app.post("/create")
async def create_price(
    request:Request,
    ID: int = Form(...),
    IDTipoTransporte:int= Form(...),
    Monto:float=Form(...),
    current_movement: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /create] Precio: {current_movement['user_id']} - Intentando crear precio con ID: {ID}")

    try:
        # Verificar si el precio ya existe
        existing_movement = controller.get_by_column(PriceOut, "ID", ID)  
        if existing_movement:
            logger.warning(f"[POST /create] Error de validación: El precio ya existe con identificación {ID}")
            raise HTTPException(400, detail="El precio ya existe con la misma identificación.")

        # Crear precio
        new_price = PriceCreate(ID=ID, IDTipoTransporte=IDTipoTransporte, Monto=Monto)
        logger.info(f"Intentando insertar precio con datos: {new_price.model_dump()}")
        controller.add(new_price)
        logger.info(f"[POST /create] Precio creado exitosamente con identificación {ID}")
        context= {
            "request":request,
            "operation": "create",
            "success": True,
            "data": PriceOut(ID=new_price.ID,IDTipoTransporte=new_price.IDTipoTransporte,Monto=new_price.Monto).model_dump(),
            "message": "Price created successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)
        
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_price(
    request:Request,
    ID: int = Form(...),
    IDTipoTransporte:int=Form(...),
    Monto:float=Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /update] Precio: {current_user['user_id']} - Actualizando precio id={ID}")
    try:
        existing = controller.get_by_column(PriceOut,"ID",ID)
        if existing is None:
            logger.warning(f"[POST /update] Precio no encontrada: id={ID}")
            raise HTTPException(404, detail="Price not found")

        updated_price = PriceOut(ID=ID, IDTipoTransporte=IDTipoTransporte, Monto=Monto)
        controller.update(updated_price)
        logger.info(f"[POST /update] Precio actualizada exitosamente: {updated_price}")
        context= {
            "request":request,
            "operation": "update",
            "success": True,
            "data": PriceOut(ID=ID, IDTipoTransporte=updated_price.IDTipoTransporte,Monto=updated_price.Monto).model_dump(),
            "message": f"Price {ID} updated successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)
    
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_price(
    request:Request,
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /delete] Precio: {current_user['user_id']} - Eliminando precio id={ID}")
    try:
        existing = controller.get_by_column(PriceOut,"ID",ID)
        if not existing:
            logger.warning(f"[POST /delete] Precio no encontrado en la base de datos: id={ID}")
            raise HTTPException(404, detail="Price not found")

        logger.info(f"[POST /delete] Eliminando precio con ID={ID}")
        controller.delete(existing) 
        logger.info(f"[POST /delete] Precio eliminada exitosamente: id={ID}")
        context = {
            "request":request,
            "operation": "delete",
            "success": True,
            "message": f"Price {ID} deleted successfully."
        }
        return templates.TemplateResponse("Confirmacion.html", context)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
