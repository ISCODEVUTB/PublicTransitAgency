from fastapi import APIRouter, Form, HTTPException
from backend.app.models.rutaparada import RutaParada
from backend.app.logic.universal_controller_sqlserver import UniversalController
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = APIRouter(prefix="/rutaparada", tags=["rutaparada"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_rutaparada_form(request: Request):
    return templates.TemplateResponse("CrearRutaParada.html", {"request": request})

@app.get("/update", response_class=HTMLResponse)
def actualizar_rutaparada_form(request: Request):
    return templates.TemplateResponse("ActualizarRutaParada.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_rutaparada_form(request: Request):
    return templates.TemplateResponse("EliminarRutaParada.html", {"request": request})

@app.post("/create")
def crear_rutaparada(
    IDParada: int = Form(...),
    IDRuta: int = Form(...)
):
    """
    Endpoint para crear una relación Ruta-Parada.
    """
    rutaparada = RutaParada(IDParada=IDParada, IDRuta=IDRuta)
    try:
        controller.add(rutaparada)
        return {"message": "Relación Ruta-Parada creada exitosamente.", "data": rutaparada.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_rutaparada(
    IDParada: int = Form(...),
    IDRuta: int = Form(...)
):
    """
    Endpoint para actualizar una relación Ruta-Parada existente.
    """
    existing_rutaparada = controller.get_by_id(RutaParada, IDParada)
    if not existing_rutaparada:
        raise HTTPException(status_code=404, detail="Relación Ruta-Parada no encontrada")

    updated_rutaparada = RutaParada(IDParada=IDParada, IDRuta=IDRuta)
    try:
        controller.update(updated_rutaparada)
        return {"message": "Relación Ruta-Parada actualizada exitosamente.", "data": updated_rutaparada.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_rutaparada(
    IDParada: int = Form(...)
):
    """
    Endpoint para eliminar una relación Ruta-Parada por su IDParada.
    """
    existing_rutaparada = controller.get_by_id(RutaParada, IDParada)
    if not existing_rutaparada:
        raise HTTPException(status_code=404, detail="Relación Ruta-Parada no encontrada")

    try:
        controller.delete(existing_rutaparada)
        return {"message": "Relación Ruta-Parada eliminada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
