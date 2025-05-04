import logging
from fastapi import APIRouter, HTTPException, Cookie
from backend.app.logic.mantainment_controller import Controller
from backend.app.core.auth import verify_token_and_scope

# Initialize the maintenance controller
controller_maintenance = Controller()

# Create the APIRouter instance
app = APIRouter(prefix="/maintainance", tags=["maintainance"])

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.get("/maintainancements", response_model=list[dict])
def get_all(access_token: str = Cookie(default=None)):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "administrador", "tecnico"])
    logger.info(f"[GET /maintainancements] Usuario {user_id} accede a todos los registros de mantenimiento.")

    try:
        records = controller_maintenance.get_all()
        logger.info(f"[GET /maintainancements] Se han recuperado {len(records)} registros de mantenimiento.")
        return records
    except Exception as e:
        logger.error(f"[GET /maintainancements] Error al obtener los registros: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/{id}")
def get_by_id(id: int, access_token: str = Cookie(default=None)):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "administrador", "tecnico"])
    logger.info(f"[GET /{id}] Usuario {user_id} busca el mantenimiento con ID {id}.")

    result = controller_maintenance.get_by_id(id)
    if not result:
        logger.warning(f"[GET /{id}] Mantenimiento con ID {id} no encontrado.")
        raise HTTPException(status_code=404, detail="Not found")

    logger.info(f"[GET /{id}] Se ha encontrado el mantenimiento con ID {id}.")
    return result.to_dict()


@app.get("/unit/{unit_id}")
def get_by_unit(unit_id: int, access_token: str = Cookie(default=None)):
    user_id = verify_token_and_scope(access_token, required_scopes=["system", "administrador", "tecnico"])
    logger.info(f"[GET /unit/{unit_id}] Usuario {user_id} busca mantenimientos de la unidad {unit_id}.")

    try:
        records = controller_maintenance.get_by_unit(unit_id)
        logger.info(f"[GET /unit/{unit_id}] Recuperados {len(records)} registros para la unidad {unit_id}.")
        return records
    except Exception as e:
        logger.error(f"[GET /unit/{unit_id}] Error al obtener registros: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
