from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_estados(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Lista todos los estados de mantenimiento.
    """
    try:
        estados = controller.read_all(MaintainanceStatus)
        return templates.TemplateResponse("ListaEstados.html", {"request": request, "estados": estados})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id}", response_class=HTMLResponse)
def detalle_estado(
    id: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Obtiene el detalle de un estado de mantenimiento por su ID.
    """
    try:
        estado = controller.get_by_id(MaintainanceStatus, id)
        if not estado:
            raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")
        return templates.TemplateResponse("DetalleEstado.html", {"request": request, "estado": estado.dict()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))