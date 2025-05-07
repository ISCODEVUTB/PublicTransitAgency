from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.schedule import Schedule
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_horarios(
    request: Request
):
    horarios = controller.read_all(Schedule)
    return templates.TemplateResponse("ListarHorarios.html", {"request": request, "horarios": horarios})

@app.get("/{id}", response_class=HTMLResponse)
def obtener_detalle_horario(
    id: int,
    request: Request
):
    horario = controller.get_by_id(Schedule, id)
    if not horario:
        raise HTTPException(status_code=404, detail="El horario no fue encontrado.")
    return templates.TemplateResponse("DetalleHorario.html", {"request": request, "horario": horario.dict()})