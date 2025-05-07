from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/tickets", tags=["tickets"])
controller = UniversalController()

@app.post("/create")
def crear_ticket(
    id: int = Form(...),
    estadoincidencia: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    ticket = Ticket(id=id, estadoincidencia=estadoincidencia)
    try:
        controller.add(ticket)
        return {"message": "Ticket creado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_ticket(
    id: int = Form(...),
    estadoincidencia: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    ticket = Ticket(id=id, estadoincidencia=estadoincidencia)
    try:
        controller.update(ticket)
        return {"message": "Ticket actualizado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

@app.post("/delete")
def eliminar_ticket(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    ticket = Ticket(id=id, estadoincidencia="")
    try:
        controller.delete(ticket)
        return {"message": "Ticket eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")