import logging
from fastapi import APIRouter, HTTPException, Security
from fastapi import status
from backend.app.models.type_card import TypeCardOut
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.auth import get_current_user

# Initialize the controller for Tipo card operations
controller = UniversalController()

# Create the router with prefix and tags
app = APIRouter(prefix="/typecard", tags=["Type Card"])

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.get("/typecards/")
def read_all():
    """
    Fetches all records of TypeCard.

    Args:
        current_user (dict): The current user, validated via security.
    
    Returns:
        List of TypeCard records.
    """
    try:
        typecards = controller.read_all(TypeCardOut)
        logger.info(f"[GET /typecards/] Successfully fetched {len(typecards)} TypeCard records.")
        return typecards
    except Exception as e:
        logger.error(f"[GET /typecards/] Error occurred while fetching TypeCard records: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@app.get("/{ID}")

def get_by_id(
    ID: int, 
    
):
    """
    Fetches a TypeCard record by its ID.

    Args:
        ID (int): The ID of the TypeCard to retrieve.
        current_user (dict): The current user, validated via security.
    
    Raises:
        HTTPException: If the TypeCard is not found (404).
    
    Returns:
        TypeCard record details as a dictionary.
    """
    try:
        result = controller.get_by_id(TypeCardOut, ID)
        if not result:
            logger.warning(f"[GET /{ID}] TypeCard with ID {ID} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="TypeCard not found"
            )
        logger.info(f"[GET /{ID}] Successfully fetched TypeCard with ID {ID}.")
        return result.to_dict()
    except HTTPException as e:
        raise e  # Deja pasar los HTTPException
    except Exception as e:
        logger.error(f"[GET /{ID}] Error occurred while fetching TypeCard with ID {ID}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")