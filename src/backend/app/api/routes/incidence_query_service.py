from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/incidences", tags=["incidences"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_incidencias(
    request: Request,
   # current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    List all incidences. Requires authentication.
    """
    incidencias = controller.read_all(Incidence)
    return templates.TemplateResponse("ListarIncidencia.html", {"request": request, "incidencias": incidencias})

@app.get("/{id}", response_class=HTMLResponse)
def detalle_incidencia(
    id: int,
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Get details of a specific incidence by ID. Requires authentication.
    """
    incidencia = controller.get_by_id(Incidence, id)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return templates.TemplateResponse("DetalleIncidencia.html", {"request": request, "incidencia": incidencia})