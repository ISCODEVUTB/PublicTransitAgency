from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.incidence import Incidence

app = APIRouter(prefix="/incidences", tags=["incidences"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_incidencias(request: Request):
    """
    Lista todas las incidencias.
    """
    try:
        incidencias = controller.read_all(Incidence)
        return templates.TemplateResponse("ListarIncidencia.html", {"request": request, "incidencias": incidencias})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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