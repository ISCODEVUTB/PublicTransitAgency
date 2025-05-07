from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.transport import Transport
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/transports", tags=["transports"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_unidades(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    List all transport units. Requires authentication.
    """
    unidades = controller.read_all(Transport)
    return templates.TemplateResponse("ListarTransports.html", {"request": request, "transports": unidades})

@app.get("/{id}", response_class=HTMLResponse)
def detalle_unidad(
    id: int,
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Get details of a specific transport unit by ID. Requires authentication.
    """
    unidad = controller.get_by_id(Transport, id)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada")
    return templates.TemplateResponse("DetalleTransport.html", {"request": request, "transports": [unidad]})