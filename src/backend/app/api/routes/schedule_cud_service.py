from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.models.schedule import Schedule
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()

@app.post("/create")
def crear_horario(
    id: int = Form(...),
    llegada: str = Form(...),
    salida: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "schedules"])
):
    schedule = Schedule(id=id, llegada=llegada, salida=salida)
    try:
        controller.add(schedule)
        return {
            "message": "Horario creado exitosamente.",
            "data": schedule.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_horario(
    id: int = Form(...),
    llegada: str = Form(...),
    salida: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "schedules"])
):
    # Validar si el horario existe antes de actualizar
    existing_schedule = controller.get_by_id(Schedule, id)
    if not existing_schedule:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    schedule = Schedule(id=id, llegada=llegada, salida=salida)
    try:
        controller.update(schedule)
        return {
            "message": "Horario actualizado exitosamente.",
            "data": schedule.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_horario(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "schedules"])
):
    # Validar si el horario existe antes de intentar eliminarlo
    existing_schedule = controller.get_by_id(Schedule, id)
    if not existing_schedule:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    schedule = Schedule(id=id, llegada="", salida="")
    try:
        controller.delete(schedule)
        return {"message": "Horario eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))