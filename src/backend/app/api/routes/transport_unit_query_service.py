from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.transport import Transport

app = APIRouter(prefix="/transports", tags=["transports"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
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