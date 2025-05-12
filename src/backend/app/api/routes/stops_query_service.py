from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.stops import Parada

app = APIRouter(prefix="/stops", tags=["stops"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
<<<<<<< HEAD
def listar_paradas(request: Request):
=======
def listar_paradas(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador", "operador"])
):
>>>>>>> a8980fb (Corrections on test)
    """
    Lista todas las paradas.
    """
    paradas = controller.read_all(Parada)
    return templates.TemplateResponse("ListarParadas.html", {"request": request, "paradas": paradas})

@app.get("/{id}", response_class=HTMLResponse)
<<<<<<< HEAD
def detalle_parada(id: int, request: Request):
=======
def obtener_detalle_parada(
    id: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador", "operador"])
):
>>>>>>> a8980fb (Corrections on test)
    """
    Obtiene el detalle de una parada por su ID.
    """
    parada = controller.get_by_id(Parada, id)
    if not parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")
    return templates.TemplateResponse("DetalleParada.html", {"request": request, "parada": parada.to_dict()})
