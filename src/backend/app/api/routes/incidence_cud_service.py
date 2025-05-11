from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.incidence import Incidence
<<<<<<< HEAD
=======
from backend.app.models.transport import UnidadTransporte
from backend.app.core.auth import get_current_user
>>>>>>> 50e6569 (changes because of rubiano)

app = APIRouter(prefix="/incidences", tags=["incidences"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/create", response_class=HTMLResponse)
def crear_incidencia_form(request: Request):
    """
    Renderiza el formulario para crear una nueva incidencia.
    """
    return templates.TemplateResponse("CrearIncidencia.html", {"request": request})

@app.post("/create")
def crear_incidencia(
<<<<<<< HEAD
    ID: int = Form(...),
    IDTicket: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(...),
    IDUnidad: int = Form(...)
=======
    ID : int = Form(...),
    IDTicket: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(...),
    IDUnidad: str = Form(...),  # Cambiado a str
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
>>>>>>> 50e6569 (changes because of rubiano)
):
    """
    Crea una nueva incidencia.
    """
<<<<<<< HEAD
    incidencia = Incidence(ID = ID, IDTicket=IDTicket, Descripcion=Descripcion, Tipo=Tipo, IDUnidad=IDUnidad)
=======
    # Validar si la unidad de transporte existe

    incidencia = Incidence(ID=ID, IDTicket=IDTicket, Descripcion=Descripcion, Tipo=Tipo, IDUnidad=IDUnidad)
>>>>>>> 50e6569 (changes because of rubiano)
    try:
        controller.add(incidencia)
        return {"message": "Incidencia creada exitosamente.", "data": incidencia.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_incidencia_form(request: Request):
    """
    Renderiza el formulario para actualizar una incidencia.
    """
    return templates.TemplateResponse("ActualizarIncidencia.html", {"request": request})

@app.post("/update")
def actualizar_incidencia(
    ID: int = Form(...),
    IDTicket: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(...),
<<<<<<< HEAD
    IDUnidad: int = Form(...)
=======
    IDUnidad: str = Form(...),  # Cambiado a str
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
>>>>>>> 50e6569 (changes because of rubiano)
):
    """
    Actualiza una incidencia existente.
    """
    # Validar si la incidencia existe
    #existing_incidencia = controller.get_by_id(Incidence, ID)
    #if not existing_incidencia:
    #    raise HTTPException(status_code=404, detail="Incidencia no encontrada.")

    incidencia_actualizada = Incidence(ID=ID, IDTicket=IDTicket, Descripcion=Descripcion, Tipo=Tipo, IDUnidad=IDUnidad)
    try:
        controller.update(incidencia_actualizada)
        return {"message": "Incidencia actualizada exitosamente.", "data": incidencia_actualizada.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_incidencia_form(request: Request):
    """
    Renderiza el formulario para eliminar una incidencia.
    """
    return templates.TemplateResponse("EliminarIncidencia.html", {"request": request})

@app.post("/delete")
def eliminar_incidencia(ID: int = Form(...)):
    """
    Elimina una incidencia por su ID.
    """
    # Validar si la incidencia existe
    existing_incidencia = controller.get_by_id(Incidence, ID)
    if not existing_incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada.")

    try:
        controller.delete(existing_incidencia)
        return {"message": "Incidencia eliminada exitosamente."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
