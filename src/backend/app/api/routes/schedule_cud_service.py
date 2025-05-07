from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.models.schedule import Schedule
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.auth import get_current_user
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_horario_form(request: Request):
    return templates.TemplateResponse("CrearHorario.html", {"request": request})


@app.get("/update", response_class=HTMLResponse)
def actualizar_horario_form(request: Request):
    return templates.TemplateResponse("ActualizarHorario.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_horario_form(request: Request):
    return templates.TemplateResponse("EliminarHorario.html", {"request": request})

@app.post("/create")
def crear_horario(
    id: int = Form(...),
    llegada: str = Form(...),
    salida: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "schedules"])
):
    schedule = Schedule(id=id, llegada=llegada, salida=salida)
    try:
        controller.add(schedule)
        return {
            "message": "Horario creado exitosamente.",
            "data": schedule.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_horario(
    id: int = Form(...),
    llegada: str = Form(...),
    salida: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "schedules"])
):
    try:
        existing_schedule = controller.get_by_id(Schedule, id)
        if not existing_schedule:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        updated_schedule = Schedule(id=id, llegada=llegada, salida=salida)
        controller.update(updated_schedule)
        return {
            "message": "Horario actualizado exitosamente.",
            "data": updated_schedule.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_horario(
    id: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "schedules"])
):
    try:
        existing_schedule = controller.get_by_id(Schedule, id)
        if not existing_schedule:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        controller.delete(Schedule(id=id, llegada="", salida=""))
        return {"message": "Horario eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))