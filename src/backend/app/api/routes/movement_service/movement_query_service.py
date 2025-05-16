#movement_query_service.py
# # This file contains the query service for the Movement model using FastAPI.
# # It includes routes for retrieving all movements and fetching a specific movement by ID.
import logging
from fastapi import FastAPI, HTTPException, APIRouter, Form, Request, status, Query, Security, Path
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#from backend.app.core.auth import get_current_user
from backend.app.models.movement import MovementOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize the controller to handle database operations
app = APIRouter(prefix="/movement", tags=["movement"])
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar/administrador", response_class=HTMLResponse)
def consultar(
    request: Request
):
    """
    Render the 'ConsultarMovimiento.html' template for the movement consultation page.
    """
    return templates.TemplateResponse("ConsultarAdministradorMovimiento.html", {"request": request})


# Route to get all the movement from the database
@app.get("/pasajero/movements")
async def get_all( request:Request):
    """
    Returns all the movement records from the database.
    """
    movimientos = controller.read_all(MovementOut)
    #logger.info(f"[GET /movements] Número de Movimientos encontradas: {len(movimientos)}")
    if movimientos:
        # Si hay varias asistencias, iterar sobre ellas
        context = {
            "request": request,
            "movimientos": movimientos,  # Lista de behaviors
        }
    else:
        logger.warning(f"[GET /movements] No se encontraron usuarios registrados")
        context = {
            "request": request,
            "movimientos": movimientos # Si no se encontraron usuarios
        }
    return templates.TemplateResponse("PasajeroMovements.html", context)


# Route to get all the movement from the database
@app.get("/administrador/movements")
async def get_all(request: Request):
    """
    Returns all the movement records from the database.
    """
    movimientos = controller.read_all(MovementOut)
    #logger.info(f"[GET /movements] Número de Movimientos encontradas: {len(movimientos)}")
    if movimientos:
        # Si hay varias asistencias, iterar sobre ellas
        context = {
            "request": request,
            "movimientos": movimientos,  # Lista de behaviors
        }
    else:
        logger.warning(f"[GET /movements] No se encontraron usuarios registrados")
        context = {
            "request": request,
            "movimientos": movimientos # Si no se encontraron usuarios
        }
    return templates.TemplateResponse("AdministradorMovements.html", context)



# Route to view a specific user by its ID and render the 'movement.html' template
@app.get("/administrador/byid", response_class=HTMLResponse)
def get_by_id(
    request: Request,
    ID: int=Query(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Fetches a price by its ID and renders its details on 'movimiento.html'.
    If no price is found, returns 'None' for the details.
    """
    #logger.info(f"[GET /movement] Usuario: {current_user['user_id']} - Consultando movimiento con id={ID}")
    result = controller.get_by_column(MovementOut,"ID", ID)

    if result:
        logger.info(f"[GET /movement] Movimiento encontrada: {result.ID}, Tipo: {result.IDTipoMovimiento}, Monto: {result.Monto}")
    else:
        logger.warning(f"[GET /movement] No se encontró movimiento con id={ID}")
    
    context = {
        "request": request,
        "ID": result.ID if result else "None",
        "IDTipoMovimiento": result.IDTipoMovimiento if result else "None",
        "Monto": result.Monto if result else "None",
    }
    return templates.TemplateResponse(request,"movimiento.html", context)

