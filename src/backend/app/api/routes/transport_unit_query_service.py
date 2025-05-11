from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
<<<<<<< HEAD
from backend.app.models.transport import Transport
=======
from backend.app.models.transport import UnidadTransporte
from backend.app.core.auth import get_current_user
>>>>>>> 50e6569 (changes because of rubiano)

app = APIRouter(prefix="/transport_units", tags=["transport_units"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
<<<<<<< HEAD
def listar_unidades(request: Request):
    """
    Lista todas las unidades de transporte.
    """
    unidades = controller.read_all(Transport)
    return templates.TemplateResponse("ListarTransports.html", {"request": request, "transports": unidades})

@app.get("/{ID}", response_class=HTMLResponse)
def obtener_detalle_unidad(ID: int, request: Request):
    """
    Obtiene el detalle de una unidad de transporte por su ID.
    """
    unidad = controller.get_by_id(Transport, ID)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada")
    return templates.TemplateResponse("DetalleTransport.html", {"request": request, "transport": unidad.to_dict()})
=======
def listar_unidades_transporte(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor", "operador"])
):
    """
    Lista todas las unidades de transporte.
    """
    unidades = controller.read_all(UnidadTransporte)
    return templates.TemplateResponse("ListarTransports.html", {"request": request, "unidades": unidades})

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_unidad_transporte(
    ID: str,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor", "operador"])
):
    """
    Obtiene el detalle de una unidad de transporte por su ID.
    """
    unidad = controller.get_by_id(UnidadTransporte, ID)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")
    return templates.TemplateResponse("DetalleTransport.html", {"request": request, "unidad": unidad.to_dict()})
>>>>>>> 50e6569 (changes because of rubiano)
