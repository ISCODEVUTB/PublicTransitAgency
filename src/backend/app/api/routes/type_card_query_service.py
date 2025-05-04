import logging
from fastapi import APIRouter, HTTPException, Cookie
from fastapi import status

from backend.app.models.type_card import TypeCardOut
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.auth import verify_token_and_scope

# Initialize the controller
controller = UniversalController()

# Create router
app = APIRouter(prefix="/typecard", tags=["Type Card"])

# Logging config
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.get("/typecards/")
def read_all(access_token: str = Cookie(default=None)):
    """
    Fetches all records of TypeCard.
    """
    user_id = verify_token_and_scope(access_token, ["system", "administrador"])
    try:
        logger.info(f"[GET /typecards/] User {user_id} is fetching all TypeCard records.")
        typecards = controller.read_all(TypeCardOut)
        logger.info(f"[GET /typecards/] Successfully fetched {len(typecards)} TypeCard records.")
        return typecards
    except Exception as e:
        logger.error(f"[GET /typecards/] Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.get("/{id}")
def get_by_id(id: int, access_token: str = Cookie(default=None)):
    """
    Fetches a TypeCard record by its ID.
    """
    user_id = verify_token_and_scope(access_token, ["system", "administrador"])
    try:
        logger.info(f"[GET /{id}] User {user_id} is fetching TypeCard with ID {id}.")
        result = controller.get_by_id(TypeCardOut, id)
        if not result:
            logger.warning(f"[GET /{id}] TypeCard with ID {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeCard not found")
        logger.info(f"[GET /{id}] Successfully fetched TypeCard with ID {id}.")
        return result.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[GET /{id}] Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")