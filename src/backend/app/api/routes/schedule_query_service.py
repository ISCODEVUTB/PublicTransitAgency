from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.schedule import Schedule

app = APIRouter(prefix="/schedules", tags=["schedules"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_horarios(request: Request):
    """
    Lista todos los horarios y los renderiza en una plantilla HTML.
    """
    try:
        horarios = controller.read_all(Schedule)
        return templates.TemplateResponse("ListarHorarios.html", {"request": request, "horarios": horarios})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar los horarios: {str(e)}")

@app.get("/{id}", response_class=HTMLResponse)
def obtener_detalle_horario(id: int, request: Request):
    """
    Obtiene el detalle de un horario por su ID.
    """
    horario = controller.get_by_id(Schedule, id)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return templates.TemplateResponse("DetalleHorario.html", {"request": request, "horario": horario.to_dict()})
