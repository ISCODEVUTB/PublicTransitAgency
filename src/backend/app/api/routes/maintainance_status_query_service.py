from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_estados(
    request: Request,
    ):
    """
    Lista todos los estados de mantenimiento.
    """
    try:
        estados = controller.read_all(MaintainanceStatus)
        return templates.TemplateResponse("ListaEstados.html", {"request": request, "estados": estados})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id:int}", response_class=HTMLResponse)
def detalle_estado(
    id: int,
    request: Request,
    ):
    """
    Obtiene el detalle de un estado de mantenimiento por su ID.
    """
    try:
        estado = controller.get_by_id(MaintainanceStatus, id)
        if not estado:
            # Si el estado no existe, devolver un error 404
            raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")
        return templates.TemplateResponse("DetalleEMantenimiento.html", {"request": request, "estado": estado.to_dict()})
    except HTTPException as e:
        # Re-lanzar excepciones HTTP para que sean manejadas correctamente
        raise e
    except Exception as e:
        # Manejar cualquier otro error como un error interno del servidor
        raise HTTPException(status_code=500, detail=str(e))
