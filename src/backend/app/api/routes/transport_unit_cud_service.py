from fastapi import APIRouter, Form, HTTPException, Security, Request
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.routes import Route
from backend.app.models.type_transport import TypeTransportCreate
from backend.app.models.transport import UnidadTransporte
from backend.app.core.auth import get_current_user
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = APIRouter(prefix="/transport_units", tags=["transport_units"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_unidad_form(request: Request):
    return templates.TemplateResponse("CrearTransport.html", {"request": request})

@app.get("/update", response_class=HTMLResponse)
def actualizar_unidad_form(request: Request):
    return templates.TemplateResponse("ActualizarTransport.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_unidad_form(request: Request):
    return templates.TemplateResponse("EliminarTransport.html", {"request": request})

@app.post("/create")
def crear_unidad_transporte(
    Ubicacion: str = Form(...),
    Capacidad: int = Form(...),
    IDRuta: int = Form(...),
    IDTipo: int = Form(...),
    ID: str = Form("EMPTY"),
):
    """
    Crea una nueva unidad de transporte.
    """
    unidad = UnidadTransporte(Ubicacion=Ubicacion, Capacidad=Capacidad, IDRuta=IDRuta, IDTipo=IDTipo, ID=ID)
    try:
        controller.add(unidad)
        return {"message": "Unidad de transporte creada exitosamente.", "data": unidad.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_unidad_transporte(
    ID: str = Form(...),
    Ubicacion: str = Form(...),
    Capacidad: int = Form(...),
    IDRuta: int = Form(...),
    IDTipo: int = Form(...)
):
    """
    Actualiza una unidad de transporte existente.
    """
    # Validar si la unidad de transporte existe
    existing_unidad = controller.get_by_id(UnidadTransporte, ID)
    if not existing_unidad:
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")

    unidad_actualizada = UnidadTransporte(Ubicacion=Ubicacion, Capacidad=Capacidad, IDRuta=IDRuta, IDTipo=IDTipo, ID=ID)
    try:
        controller.update(unidad_actualizada)
        return {"message": "Unidad de transporte actualizada exitosamente.", "data": unidad_actualizada.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_unidad_transporte(
    ID: str = Form(...),
):
    """
    Elimina una unidad de transporte por su ID.
    """
    # Validar si la unidad de transporte existe
    existing_unidad = controller.get_by_id(UnidadTransporte, ID)
    if not existing_unidad:
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")

    try:
        controller.delete(existing_unidad)
        return {"message": "Unidad de transporte eliminada exitosamente."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
