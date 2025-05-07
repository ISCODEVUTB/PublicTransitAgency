from fastapi import Request

from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import Shift
from backend.app.core.auth import get_current_user
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = APIRouter(prefix="/shifts", tags=["shifts"])
controller = UniversalController()
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
    tipoturno: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Crea un turno con los datos proporcionados.
    """
    turno = Shift(id=id, tipoturno=tipoturno)
    try:
        controller.add(turno)
        return {"message": "Turno creado exitosamente.", "data": turno.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_turno(
    id: int = Form(...),
    tipoturno: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Actualiza la información de un turno existente.
    """
    existing_turno = controller.get_by_id(Shift, id)
    if not existing_turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    turno = Shift(id=id, tipoturno=tipoturno)
    try:
        controller.update(turno)
        return {"message": "Turno actualizado exitosamente.", "data": turno.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_turno(
    id: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
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