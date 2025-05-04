import logging
from fastapi import APIRouter, Form, Request, HTTPException, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.models.type_card import TypeCardOut, TypeCardCreate
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.auth import verify_token_and_scope

# Initialize the controller
controller = UniversalController()

# Set up the template engine
templates = Jinja2Templates(directory="src/backend/app/templates")

# Create the router
app = APIRouter(prefix="/typecard", tags=["Type Card"])

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.get("/crear", response_class=HTMLResponse)
def create_typecard_form(request: Request, access_token: str = Cookie(default=None)):
    user_id = verify_token_and_scope(access_token, ["system", "administrador"])
    logger.info(f"[GET /crear] User {user_id} accessed the create card type form.")
    return templates.TemplateResponse("CrearTipoTarjeta.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def delete_typecard_form(request: Request, access_token: str = Cookie(default=None)):
    user_id = verify_token_and_scope(access_token, ["system", "administrador"])
    logger.info(f"[GET /eliminar] User {user_id} accessed the delete card type form.")
    return templates.TemplateResponse("EliminarTipoTarjeta.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def update_typecard_form(request: Request, access_token: str = Cookie(default=None)):
    user_id = verify_token_and_scope(access_token, ["system", "administrador"])
    logger.info(f"[GET /actualizar] User {user_id} accessed the update card type form.")
    return templates.TemplateResponse("ActualizarTipoTarjeta.html", {"request": request})


@app.post("/create")
async def create_typecard(
    id: int = Form(...),
    type: str = Form(...),
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, ["system", "administrador"])
    try:
        new_typecard = TypeCardCreate(id=id, type=type)
        controller.add(new_typecard)
        logger.info(f"[POST /create] User {user_id} created a new card type: ID={id}, type='{type}'")
        return {
            "operation": "create",
            "success": True,
            "data": TypeCardOut(id=id, type=type).model_dump(),
            "message": "Card type created successfully"
        }
    except ValueError as e:
        logger.error(f"[POST /create] Error creating card type: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Internal server error: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_typecard(
    id: int = Form(...),
    type: str = Form(...),
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, ["system", "administrador"])
    try:
        existing = controller.get_by_id(TypeCardOut, id)
        if not existing:
            logger.warning(f"[POST /update] Card type with ID {id} not found.")
            raise HTTPException(404, detail="Card type not found")

        updated_typecard = TypeCardCreate(id=id, type=type)
        controller.update(updated_typecard)
        logger.info(f"[POST /update] User {user_id} updated card type {id} to '{type}'")
        return {
            "operation": "update",
            "success": True,
            "data": TypeCardOut(id=id, type=type).model_dump(),
            "message": f"Card type {id} updated successfully"
        }
    except ValueError as e:
        logger.error(f"[POST /update] Error updating card type: {str(e)}")
        raise HTTPException(400, detail=str(e))


@app.post("/delete")
async def delete_typecard(
    id: int = Form(...),
    access_token: str = Cookie(default=None)
):
    user_id = verify_token_and_scope(access_token, ["system", "administrador"])
    try:
        existing = controller.get_by_id(TypeCardOut, id)
        if not existing:
            logger.warning(f"[POST /delete] Card type with ID {id} not found.")
            raise HTTPException(404, detail="Card type not found")

        controller.delete(existing)
        logger.info(f"[POST /delete] User {user_id} deleted card type ID {id}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"Card type {id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[POST /delete] Internal server error: {str(e)}")
        raise HTTPException(500, detail=str(e))
