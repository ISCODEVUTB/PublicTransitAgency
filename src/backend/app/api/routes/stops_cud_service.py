<<<<<<< HEAD
from fastapi import APIRouter, Form, HTTPException
=======
from fastapi import APIRouter, Form, HTTPException, Security, Request
>>>>>>> a8980fb (Corrections on test)
from backend.app.models.stops import Parada
from backend.app.logic.universal_controller_sqlserver import UniversalController
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
<<<<<<< HEAD
from fastapi import Request
=======
from backend.app.core.auth import get_current_user
>>>>>>> a8980fb (Corrections on test)

app = APIRouter(prefix="/paradas", tags=["paradas"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
<<<<<<< HEAD
def crear_parada_form(request: Request):
    return templates.TemplateResponse("CrearParada.html", {"request": request})

@app.get("/update", response_class=HTMLResponse)
def actualizar_parada_form(request: Request):
    return templates.TemplateResponse("ActualizarParada.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_parada_form(request: Request):
    return templates.TemplateResponse("EliminarParada.html", {"request": request})

=======
def crear_parada_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Renderiza el formulario para crear una parada.
    """
    return templates.TemplateResponse("CrearParada.html", {"request": request})

>>>>>>> a8980fb (Corrections on test)
@app.post("/create")
def crear_parada(
    id: int = Form(...),
    Nombre: str = Form(...),
<<<<<<< HEAD
    Ubicacion: str = Form(...)
=======
    Ubicacion: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
>>>>>>> a8980fb (Corrections on test)
):
    """
    Endpoint para crear una parada.
    """
    parada = Parada(ID=id, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.add(parada)
        return {"message": "Parada creada exitosamente.", "data": parada.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
<<<<<<< HEAD
=======

@app.get("/update", response_class=HTMLResponse)
def actualizar_parada_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Renderiza el formulario para actualizar una parada.
    """
    return templates.TemplateResponse("ActualizarParada.html", {"request": request})
>>>>>>> a8980fb (Corrections on test)

@app.post("/update")
def actualizar_parada(
    id: int = Form(...),
    Nombre: str = Form(...),
<<<<<<< HEAD
    Ubicacion: str = Form(...)
=======
    Ubicacion: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
>>>>>>> a8980fb (Corrections on test)
):
    """
    Endpoint para actualizar una parada existente.
    """
    existing_parada = controller.get_by_id(Parada, id)
    if not existing_parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")

<<<<<<< HEAD
    parada = Parada(ID=id, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.update(parada)
        return {"message": "Parada actualizada exitosamente.", "data": parada.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_parada(
    id: int = Form(...)
=======
    updated_parada = Parada(ID=ID, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.update(updated_parada)
        return {"message": "Parada actualizada exitosamente.", "data": updated_parada.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_parada_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Renderiza el formulario para eliminar una parada.
    """
    return templates.TemplateResponse("EliminarParada.html", {"request": request})

@app.post("/delete")
def eliminar_parada(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
>>>>>>> a8980fb (Corrections on test)
):
    """
    Endpoint para eliminar una parada por su ID.
    """
    existing_parada = controller.get_by_id(Parada, id)
    if not existing_parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")

    try:
        controller.delete(existing_parada)
        return {"message": "Parada eliminada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
