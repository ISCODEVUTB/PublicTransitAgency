from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.rutaparada import RutaParada

app = APIRouter(prefix="/rutaparada", tags=["rutaparada"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_rutaparada(request: Request):
    """
    Lista todas las relaciones Ruta-Parada.
    """
    rutaparadas = controller.read_all(RutaParada)
    return templates.TemplateResponse("ListarRutaParada.html", {"request": request, "rutaparadas": rutaparadas})

@app.get("/{IDParada}", response_class=HTMLResponse)
def detalle_rutaparada(IDParada: int, request: Request):
    """
    Obtiene el detalle de una relación Ruta-Parada por su IDParada.
    """
    rutaparada = controller.get_by_id(RutaParada, IDParada)
    if not rutaparada:
        raise HTTPException(status_code=404, detail="Relación Ruta-Parada no encontrada")
    return templates.TemplateResponse("DetalleRutaParada.html", {"request": request, "rutaparada": rutaparada.to_dict()})