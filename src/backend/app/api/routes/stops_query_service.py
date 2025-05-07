from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.stops import Parada
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/paradas", tags=["paradas"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_paradas(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    paradas = controller.read_all(Parada)
    return templates.TemplateResponse("ListarParadas.html", {"request": request, "paradas": paradas})

@app.get("/{id}", response_class=HTMLResponse)
def detalle_parada(
    id: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    parada = controller.get_by_id(Parada, id)
    if not parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")
    return templates.TemplateResponse("DetalleParada.html", {"request": request, "parada": parada})