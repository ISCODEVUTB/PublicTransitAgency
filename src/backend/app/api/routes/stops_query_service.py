from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.stops import Parada
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/paradas", tags=["paradas"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_paradas(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operador"])
):
    """
    Lista todas las paradas.
    """
    try:
        paradas = controller.read_all(Parada)
        return templates.TemplateResponse("ListarParadas.html", {"request": request, "paradas": paradas})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id}", response_class=HTMLResponse)
def detalle_parada(
    id: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operador"])
):
    """
    Obtiene el detalle de una parada por su ID.
    """
    try:
        parada = controller.get_by_id(Parada, id)
        if not parada:
            raise HTTPException(status_code=404, detail="Parada no encontrada")
        return templates.TemplateResponse("DetalleParada.html", {"request": request, "parada": parada.to_dict()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
