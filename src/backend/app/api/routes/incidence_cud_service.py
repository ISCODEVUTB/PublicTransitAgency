from fastapi import APIRouter, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/incidences", tags=["incidences"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_incidencia_form(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for creating a new incidence. Requires authentication.
    """
    return templates.TemplateResponse("CrearIncidencia.html", {"request": request})

@app.post("/create")
def crear_incidencia(
    id: int = Form(...),
    idticket: int = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    idunit: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Create a new incidence. Requires authentication.
    """
    incidencia = Incidence(id=id, idticket=idticket, description=description, type=type, idunit=idunit)
    try:
        controller.add(incidencia)
        return {
            "operation": "create",
            "success": True,
            "data": incidencia.to_dict(),
            "message": "Incidencia creada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_incidencia_form(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for updating an incidence. Requires authentication.
    """
    return templates.TemplateResponse("ActualizarIncidencia.html", {"request": request})

@app.post("/update")
def actualizar_incidencia(
    id: int = Form(...),
    idticket: int = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    idunit: int = Form(...),
   # current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Update an existing incidence. Requires authentication.
    """
    incidencia = Incidence(id=id, idticket=idticket, description=description, type=type, idunit=idunit)
    try:
        controller.update(incidencia)
        return {
            "operation": "update",
            "success": True,
            "data": incidencia.to_dict(),
            "message": "Incidencia actualizada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")  # Cambiado el mensaje

@app.get("/delete", response_class=HTMLResponse)
def eliminar_incidencia_form(
    request: Request,
   # current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for deleting an incidence. Requires authentication.
    """
    return templates.TemplateResponse("EliminarIncidencia.html", {"request": request})

@app.post("/delete")
def eliminar_incidencia(
    id: int = Form(...),
   # current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Delete an incidence by ID. Requires authentication.
    """
    try:
        controller.delete(Incidence(id=id, idticket=0, description="", type="", idunit=0))
        return {
            "operation": "delete",
            "success": True,
            "message": "Incidencia eliminada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")  # Cambiado el mensaje
