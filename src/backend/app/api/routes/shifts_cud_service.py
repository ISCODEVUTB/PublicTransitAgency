from fastapi import APIRouter, Form, HTTPException, Security, Request
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.shift import Shift
from backend.app.core.auth import get_current_user
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = APIRouter(prefix="/shifts", tags=["shifts"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_turno_form(request: Request):
    return templates.TemplateResponse("CrearTurno.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_turno_form(request: Request):
    return templates.TemplateResponse("EliminarTurno.html", {"request": request})

@app.get("/update", response_class=HTMLResponse)
def actualizar_turno_form(request: Request):
    return templates.TemplateResponse("ActualizarTurno.html", {"request": request})

@app.post("/create")
def crear_turno(
    id: int = Form(...),
    TipoTurno: str = Form(...),
):
    """
    Crea un turno con los datos proporcionados.
    """
    turno = Shift(ID=id, TipoTurno=TipoTurno)
    try:
        controller.add(turno)
        return {"message": "Turno creado exitosamente.", "data": turno.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_turno(
    id: int = Form(...),  # Asegurarse de que el campo 'id' sea obligatorio
    TipoTurno: str = Form(...),
):
    """
    Actualiza la información de un turno existente.
    """
    # Verificar si el turno existe
    existing_turno = controller.get_by_id(Shift, id)
    if not existing_turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    # Crear un nuevo objeto Shift con los datos actualizados
    turno_actualizado = Shift(ID=id, TipoTurno=TipoTurno)
    try:
        controller.update(turno_actualizado)
        return {"message": "Turno actualizado exitosamente.", "data": turno_actualizado.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_turno(
    id: int = Form(...),
):
    """
    Elimina un turno existente por su ID.
    """
    existing_turno = controller.get_by_id(Shift, id)
    if not existing_turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    try:
        controller.delete(existing_turno)
        return {"message": "Turno eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
