from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Form, HTTPException, Security
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.routes import Route
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/routes", tags=["routes"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_ruta_form(request: Request):
    return templates.TemplateResponse("CrearRuta.html", {"request": request})

@app.get("/update", response_class=HTMLResponse)
def actualizar_ruta_form(request: Request):
    return templates.TemplateResponse("ActualizarRuta.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_ruta_form(request: Request):
    return templates.TemplateResponse("EliminarRuta.html", {"request": request})

@app.post("/create")
def crear_ruta(
    id: int = Form(...),
    idhorario: int = Form(...),
    name: str = Form(...),
   # current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Crea una nueva ruta.
    """
    ruta = Route(id=id, idhorario=idhorario, name=name)
    try:
        controller.add(ruta)
        return {"message": "Ruta creada exitosamente.", "data": ruta.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_ruta(
    id: int = Form(...),
    idhorario: int = Form(...),
    name: str = Form(...),
   # current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Actualiza una ruta existente.
    """
    existing_route = controller.get_by_id(Route, id)
    if not existing_route:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    ruta_actualizada = Route(id=id, idhorario=idhorario, name=name)
    try:
        controller.update(ruta_actualizada)
        return {"message": "Ruta actualizada exitosamente.", "data": ruta_actualizada.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_ruta(
    id: int = Form(...),
   # current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Elimina una ruta por su ID.
    """
    existing_route = controller.get_by_id(Route, id)
    if not existing_route:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    try:
        controller.delete(existing_route)
        return {"message": "Ruta eliminada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))