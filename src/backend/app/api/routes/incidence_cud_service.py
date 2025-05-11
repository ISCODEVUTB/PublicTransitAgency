from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.incidence import Incidence

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
    ID: int = Form(...),
    IDTicket: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(...),
    IDUnidad: int = Form(...)
):
    """
    Crea una nueva incidencia.
    """
    incidencia = Incidence(ID = ID, IDTicket=IDTicket, Descripcion=Descripcion, Tipo=Tipo, IDUnidad=IDUnidad)
    try:
        controller.add(incidencia)
        return {"message": "Incidencia creada exitosamente.", "data": incidencia.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_incidencia(ID: int, request: Request):
    """
    Obtiene el detalle de una incidencia por su ID.
    """
    try:
        incidencia = controller.get_by_id(Incidence, ID)
        if not incidencia:
            raise HTTPException(status_code=404, detail="Incidencia no encontrada")
        return templates.TemplateResponse("DetalleIncidencia.html", {"request": request, "incidencia": incidencia.to_dict()})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    IDUnidad: int = Form(...)
):
    """
    Actualiza una incidencia existente.
    """
    incidencia = Incidence(ID=ID, IDTicket=IDTicket, Descripcion=Descripcion, Tipo=Tipo, IDUnidad=IDUnidad)
    try:
        controller.update(incidencia)
        return {"message": "Incidencia actualizada exitosamente.", "data": incidencia.to_dict()}
    except ValueError:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")

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
    try:
        controller.delete(Incidence(ID=ID))
        return {"message": "Incidencia eliminada exitosamente."}
    except ValueError:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
