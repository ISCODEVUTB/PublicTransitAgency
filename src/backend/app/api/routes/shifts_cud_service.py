from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import Shift
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/shifts", tags=["shifts"])
controller = UniversalController()

@app.post("/create")
def crear_turno(
    id: int = Form(...),
    tipoturno: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    turno = Shift(id=id, tipoturno=tipoturno)
    try:
        controller.add(turno)
        return {"message": "Turno creado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_turno(
    id: int = Form(...),
    tipoturno: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    turno = Shift(id=id, tipoturno=tipoturno)
    try:
        controller.update(turno)
        return {"message": "Turno actualizado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

@app.post("/delete")
def eliminar_turno(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    turno = Shift(id=id, tipoturno="")
    try:
        controller.delete(turno)
        return {"message": "Turno eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Turno no encontrado")