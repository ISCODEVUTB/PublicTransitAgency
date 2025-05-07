from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.models.stops import Parada
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/paradas", tags=["paradas"])
controller = UniversalController()

@app.post("/create")
def crear_parada(
    id: int = Form(...),
    name: str = Form(...),
    ubication: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    parada = Parada(id=id, name=name, ubication=ubication)
    try:
        controller.add(parada)
        return {"message": "Parada creada exitosamente.", "data": parada.dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_parada(
    id: int = Form(...),
    name: str = Form(...),
    ubication: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    parada = Parada(id=id, name=name, ubication=ubication)
    existing_parada = controller.get_by_id(Parada, id)
    if not existing_parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")

    try:
        controller.update(parada)
        return {"message": "Parada actualizada exitosamente.", "data": parada.dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_parada(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    existing_parada = controller.get_by_id(Parada, id)
    if not existing_parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")

    try:
        controller.delete(existing_parada)
        return {"message": "Parada eliminada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))