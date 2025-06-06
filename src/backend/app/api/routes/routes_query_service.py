import logging
from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse
from backend.app.models.routes import Ruta
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/routes", tags=["routes"])

@app.get("/", response_class=JSONResponse)
def listar_rutas(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"])
):
    """
    Lista todas las rutas.
    """
    try:
        rutas = controller.read_all(Ruta)
        logger.info(f"[GET /routes/] Se listaron {len(rutas)} rutas.")
        rutas_json = [
            r.model_dump() if hasattr(r, "model_dump")
            else r.dict() if hasattr(r, "dict")
            else r
            for r in rutas
        ]
        return rutas_json
    except Exception as e:
        logger.error(f"[GET /routes/] Error al listar rutas: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno al listar rutas."}
        )

@app.get("/{ID}", response_class=JSONResponse)
def detalle_ruta(
    ID: int,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"])
):
    """
    Obtiene el detalle de una ruta por su ID.
    """
    try:
        ruta = controller.get_by_id(Ruta, ID)
        if not ruta:
            logger.warning(f"[GET /routes/{ID}] Ruta no encontrada.")
            return JSONResponse(
                status_code=404,
                content={"detail": "No se encontró la ruta especificada."}
            )
        logger.info(f"[GET /routes/{ID}] Se consultó la ruta con ID={ID}.")
        if hasattr(ruta, "model_dump"):
            return {"data": ruta.model_dump()}
        elif hasattr(ruta, "dict"):
            return {"data": ruta.dict()}
        else:
            return {"data": ruta}
    except Exception as e:
        logger.error(f"[GET /routes/{ID}] Error al consultar ruta: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error interno al consultar ruta: {str(e)}"}
        )