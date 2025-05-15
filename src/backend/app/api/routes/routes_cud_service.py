from fastapi import Request, APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.routes import Route

app = APIRouter(prefix="/routes", tags=["routes"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_ruta_form(request: Request):
    """
    Renderiza el formulario para crear una nueva ruta.
    """
    return templates.TemplateResponse("CrearRuta.html", {"request": request})

@app.post("/create")
def crear_ruta(
    ID: int = Form(...),
    IDHorario: int = Form(...),
    Nombre: str = Form(...)
):
    """
    Crea una nueva ruta.
    """
    ruta = Route(ID=ID, IDHorario=IDHorario, Nombre=Nombre)
    try:
        controller.add(ruta)
        return {"message": "Ruta creada exitosamente.", "data": ruta.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear la ruta: {str(e)}")

@app.get("/update", response_class=HTMLResponse)
def actualizar_ruta_form(request: Request):
    """
    Renderiza el formulario para actualizar una ruta.
    """
    return templates.TemplateResponse("ActualizarRuta.html", {"request": request})

@app.post("/update")
def actualizar_ruta(
    ID: int = Form(...),
    IDHorario: int = Form(...),
    Nombre: str = Form(...)
):
    """
    Actualiza una ruta existente.
    """
    existing_route = controller.get_by_id(Route, ID)
    if not existing_route:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    ruta_actualizada = Route(ID=ID, IDHorario=IDHorario, Nombre=Nombre)
    try:
        controller.update(ruta_actualizada)
        return {"message": "Ruta actualizada exitosamente.", "data": ruta_actualizada.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar la ruta: {str(e)}")

@app.get("/delete", response_class=HTMLResponse)
def eliminar_ruta_form(request: Request):
    """
    Renderiza el formulario para eliminar una ruta.
    """
    return templates.TemplateResponse("EliminarRuta.html", {"request": request})

@app.post("/delete")
def eliminar_ruta(ID: int = Form(...)):
    """
    Elimina una ruta por su ID.
    """
    existing_route = controller.get_by_id(Route, ID)
    if not existing_route:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    try:
        controller.delete(existing_route)
        return {"message": "Ruta eliminada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar la ruta: {str(e)}")
