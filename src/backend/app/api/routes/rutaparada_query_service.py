from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.rutaparada import RutaParada
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/rutaparada", tags=["rutaparada"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_rutaparadas(
    request: Request,
  #  current_user: dict = Security(get_current_user, scopes=["system", "rutas"])
):
    """
    Lista todas las relaciones entre rutas y paradas.
    """
    try:
        rutaparadas = controller.read_all(RutaParada)
        return templates.TemplateResponse("ListaRutaParadas.html", {"request": request, "rutaparadas": rutaparadas})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id}", response_class=HTMLResponse)
def detalle_rutaparada(
    id: int,
    request: Request,
   # current_user: dict = Security(get_current_user, scopes=["system", "rutas"])
):
    """
    Obtiene el detalle de una relación entre ruta y parada por su ID.
    """
    try:
        rutaparada = controller.get_by_id(RutaParada, id)
        if not rutaparada:
            raise HTTPException(status_code=404, detail="Relación ruta-parada no encontrada")
        return templates.TemplateResponse("DetalleRutaParada.html", {"request": request, "rutaparada": rutaparada.to_dict()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))