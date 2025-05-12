import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.card import CardCreate, CardOut
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/card", tags=["card"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def index_create(request: Request):
    return templates.TemplateResponse(request,"CrearTarjeta.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def index_update(request: Request):
    return templates.TemplateResponse(request,"ActualizarTarjeta.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request
    
):
    return templates.TemplateResponse(request,"EliminarTarjeta.html", {"request": request})


@app.post("/create")
async def create_card(
    id: int = Form(...),
    iduser: int = Form(...),
    idtype: int = Form(...)
):
    try:
        new_card = CardCreate(id=id, iduser=iduser,idtype=idtype, balance=0)
        controller.add(new_card)

        logger.info(f"[POST /create] Tarjeta creada exitosamente: {new_card}")
        return {
            "operation": "create",
            "success": True,
            "data": CardOut(id=new_card.id, iduser=new_card.iduser,idtype=new_card.idtype, balance=new_card.balance).model_dump(),
            "message": "Card created successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_card(
    id: int = Form(...),
    iduser: int = Form(...),
    idtype: int = Form(...),
    
):
    try:
        existing = controller.get_by_id(CardOut, id)
        if existing is None:
            logger.warning(f"[POST /update] Tarjeta no encontrada: id={id}")
            raise HTTPException(404, detail="Card not found")

        updated_card = CardCreate(id=id,iduser=iduser,idtype=idtype, balance=existing.balance)
        controller.update(updated_card)

        logger.info(f"[POST /update] Tarjeta actualizada exitosamente: {updated_card}")
        return {
            "operation": "update",
            "success": True,
            "data": CardOut(id=updated_card.id, iduser=updated_card.iduser,idtype=updated_card.idtype, balance=updated_card.balance).model_dump(),
            "message": f"Card {id} updated successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_card(
    id: int = Form(...),
    
):
    try:
        existing = controller.get_by_id(CardOut, id)
        if not existing:
            logger.warning(f"[POST /delete] Tarjeta no encontrada: id={id}")
            raise HTTPException(404, detail="Card not found")

        controller.delete(existing)
        logger.info(f"[POST /delete] Tarjeta eliminada exitosamente: id={id}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"Card {id} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=str(e))
