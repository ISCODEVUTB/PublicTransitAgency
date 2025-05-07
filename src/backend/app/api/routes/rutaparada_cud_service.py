from fastapi import Request
from fastapi import APIRouter, Form, HTTPException, Security
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.rutaparada import RutaParada
from backend.app.core.auth import get_current_user

# Initialize the API router with prefix and tags for route-stop relationships
app = APIRouter(prefix="/rutaparada", tags=["rutaparada"])
# Create a controller instance for database operations
controller = UniversalController()
# Set up the templates directory for HTML rendering
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=Jinja2Templates)
def crear_rutaparada_form(request: Request):
    """
    Renders the form for creating a new route-stop relationship.

    Args:
        request: The incoming HTTP request

    Returns:
        TemplateResponse: The HTML template for creating a route-stop relationship
    """
    return templates.TemplateResponse("CrearRutaParada.html", {"request": request})

@app.get("/update", response_class=Jinja2Templates)
def actualizar_rutaparada_form(request: Request):
    """
    Renders the form for updating an existing route-stop relationship.

    Args:
        request: The incoming HTTP request

    Returns:
        TemplateResponse: The HTML template for updating a route-stop relationship
    """
    return templates.TemplateResponse("ActualizarRutaParada.html", {"request": request})

@app.get("/delete", response_class=Jinja2Templates)
def eliminar_rutaparada_form(request: Request):
    """
    Renders the form for deleting a route-stop relationship.

    Args:
        request: The incoming HTTP request

    Returns:
        TemplateResponse: The HTML template for deleting a route-stop relationship
    """
    return templates.TemplateResponse("EliminarRutaParada.html", {"request": request})

@app.post("/create")
def crear_rutaparada(
    id: int = Form(...),
    idruta: int = Form(...),
    idparada: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "rutas"])
):
    """
    Creates a new relationship between a route and a stop.

    Args:
        id: The ID for the new relationship
        idruta: The ID of the route
        idparada: The ID of the stop

    Returns:
        dict: A message indicating success and the created data

    Raises:
        HTTPException: If there's an error during creation
    """
    # Create a new RutaParada object with the provided data
    rutaparada = RutaParada(id=id, idruta=idruta, idparada=idparada)
    try:
        # Add the new relationship to the database
        controller.add(rutaparada)
        return {"message": "Relación ruta-parada creada exitosamente.", "data": rutaparada.to_dict()}
    except Exception as e:
        # Handle any errors that occur during creation
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_rutaparada(
    id: int = Form(...),
    idruta: int = Form(...),
    idparada: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "rutas"])
):
    """
    Updates an existing relationship between a route and a stop.

    Args:
        id: The ID of the relationship to update
        idruta: The new route ID
        idparada: The new stop ID

    Returns:
        dict: A message indicating success and the updated data

    Raises:
        HTTPException: If the relationship doesn't exist or there's an error during update
    """
    # Check if the relationship exists
    existing_rutaparada = controller.get_by_id(RutaParada, id)
    if not existing_rutaparada:
        raise HTTPException(status_code=404, detail="Relación ruta-parada no encontrada")

    # Create an updated RutaParada object
    rutaparada_actualizada = RutaParada(id=id, idruta=idruta, idparada=idparada)
    try:
        # Update the relationship in the database
        controller.update(rutaparada_actualizada)
        return {"message": "Relación ruta-parada actualizada exitosamente.", "data": rutaparada_actualizada.to_dict()}
    except Exception as e:
        # Handle any errors that occur during update
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_rutaparada(
    id: int = Form(...),
    # current_user: dict = Security(get_current_user, scopes=["system", "rutas"])
):
    """
    Deletes a relationship between a route and a stop by its ID.

    Args:
        id: The ID of the relationship to delete

    Returns:
        dict: A message indicating successful deletion

    Raises:
        HTTPException: If the relationship doesn't exist or there's an error during deletion
    """
    # Check if the relationship exists
    existing_rutaparada = controller.get_by_id(RutaParada, id)
    if not existing_rutaparada:
        raise HTTPException(status_code=404, detail="Relación ruta-parada no encontrada")

    try:
        # Delete the relationship from the database
        controller.delete(existing_rutaparada)
        return {"message": "Relación ruta-parada eliminada exitosamente."}
    except Exception as e:
        # Handle any errors that occur during deletion
        raise HTTPException(status_code=400, detail=str(e))
