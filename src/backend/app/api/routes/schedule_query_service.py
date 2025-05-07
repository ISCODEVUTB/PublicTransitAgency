from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.schedule import Schedule

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_horarios(request: Request):
    try:
        horarios = controller.read_all(Schedule)
        return templates.TemplateResponse("ListarHorarios.html", {"request": request, "horarios": horarios})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id}", response_class=HTMLResponse)
def obtener_detalle_horario(id: int, request: Request):
    try:
        horario = controller.get_by_id(Schedule, id)
        if not horario:
            raise HTTPException(status_code=404, detail="El horario no fue encontrado.")
        return templates.TemplateResponse("DetalleHorario.html", {"request": request, "horario": horario.to_dict()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))