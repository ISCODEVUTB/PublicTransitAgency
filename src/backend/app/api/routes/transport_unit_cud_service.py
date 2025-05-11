<<<<<<< HEAD
from fastapi import APIRouter, Form, HTTPException
from backend.app.models.transport import Transport
from backend.app.logic.universal_controller_sqlserver import UniversalController
=======
from fastapi import APIRouter, Form, HTTPException, Security, Request
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.routes import Route
from backend.app.models.type_transport import TypeTransportCreate
from backend.app.models.transport import UnidadTransporte
from backend.app.core.auth import get_current_user
>>>>>>> 50e6569 (changes because of rubiano)
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = APIRouter(prefix="/transport_units", tags=["transport_units"])
controller = UniversalController()
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
<<<<<<< HEAD
    IDTipo: int = Form(...)
):
    """
    Endpoint para crear una unidad de transporte.
=======
    IDTipo: int = Form(...),
    ID: str = Form("EMPTY"),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Crea una nueva unidad de transporte.
>>>>>>> 50e6569 (changes because of rubiano)
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
<<<<<<< HEAD
    Endpoint para actualizar una unidad de transporte existente.
=======
    Actualiza una unidad de transporte existente.
>>>>>>> 50e6569 (changes because of rubiano)
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
<<<<<<< HEAD
def eliminar_unidad(
    ID: int = Form(...)
):
    """
    Endpoint para eliminar una unidad de transporte por su ID.
=======
def eliminar_unidad_transporte(
    ID: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Elimina una unidad de transporte por su ID.
>>>>>>> 50e6569 (changes because of rubiano)
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
