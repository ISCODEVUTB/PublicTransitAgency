from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.incidence import Incidence

app = APIRouter(prefix="/incidences", tags=["incidences"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_incidencias(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Lista todas las incidencias.
    """
    incidencias = controller.read_all(Incidence)
    return templates.TemplateResponse("ListarIncidencias.html", {"request": request, "incidencias": incidencias})

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_incidencia(
    ID: int,
    request: Request,
   # current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Obtiene el detalle de una incidencia por su ID.
    """
    incidencia = controller.get_by_id(Incidence, ID)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada.")
    return templates.TemplateResponse("DetalleIncidencia.html", {"request": request, "incidencia": incidencia.to_dict()})