import logging
from fastapi import Depends, HTTPException, status, Request, Security, Cookie
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError
from backend.app.core.config import settings
from typing import Dict, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login/token",
    scopes={
        "system": "Full system access",
        "administrador": "Permission to manage users",
        "pasajero": "Passenger permission",
        "supervisor": "Supervisor permission",
        "mantenimiento": "Maintenance permission",
        "operador": "Operator permission",
    }
)


def encode_token(payload: dict) -> str:
    """
    Encodes a JWT token using the given payload.

    Args:
        payload (dict): Data to encode in the token.

    Returns:
        str: Encoded JWT token.
    """
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    access_token_cookie: str = Cookie(default=None)
) -> Dict[str, str]:
    """
    Extracts and verifies the current authenticated user from a JWT token.
    """
    # Usar el token de la cookie si no está en el encabezado
    if not token and access_token_cookie:
        token = access_token_cookie

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    # Eliminar el prefijo "Bearer " si está presente
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        scope_string = payload.get("scope", "")
        token_scopes = scope_string.split()

        # Verificar los scopes requeridos
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required scope: {scope}",
                )

        return {
            "user_id": user_id,
            "scopes": token_scopes
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_role(allowed_roles: List[str]):
    """
    Dependency to verify if the current user has the required role(s).

    Args:
        allowed_roles (List[str]): List of roles allowed to access the route.

    Returns:
        Callable: A dependency function that returns the current user if authorized.

    Raises:
        HTTPException: If the user does not have the required role.
    """

    def _verify(current_user: dict = Depends(get_current_user)):
        if not any(scope in allowed_roles for scope in current_user["scopes"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this route",
            )
        return current_user

    return _verify


def set_access_token_cookie(response, token: str):
    """
    Sets the access token in an HTTP-only cookie.

    Args:
        response: The response object.
        token (str): The JWT token to set in the cookie.
    """
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)


def authenticate_user_from_cookie(
    access_token: str = Cookie(default=None),
    required_scopes: List[str] = None
) -> Dict[str, str]:
    """
    Authenticate the user by decoding the JWT token from the cookie and verifying scopes.

    Args:
        access_token (str): The JWT token from the cookie.
        required_scopes (List[str]): A list of scopes required to access the resource.

    Returns:
        Dict[str, str]: A dictionary containing user information (e.g., user_id, scopes).

    Raises:
        HTTPException: If the token is missing, invalid, or the user lacks the required scopes.
    """
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token is missing")

    # Eliminar el prefijo "Bearer " si está presente
    if access_token.startswith("Bearer "):
        access_token = access_token.replace("Bearer ", "")

    try:
        # Decodificar el token
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        scope_string = payload.get("scope", "")
        token_scopes = scope_string.split()  # Convertir la cadena de scopes en una lista

        # Verificar si el usuario tiene al menos un scope requerido
        if required_scopes and not any(scope in token_scopes for scope in required_scopes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required scope: at least one of {required_scopes}"
            )

        logger.info(f"User {user_id} authenticated with scopes: {token_scopes}")
        return {"user_id": user_id, "scopes": token_scopes}

    except JWTError as e:
        logger.error(f"Error decoding token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
def verify_token_and_scope(access_token: str, required_scopes: list[str]) -> str:
    """
    Verifica el token y los scopes requeridos.
    Retorna el ID del usuario si es válido.
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")

    if access_token.startswith("Bearer "):
        access_token = access_token.replace("Bearer ", "")

    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        scope_string = payload.get("scope", "")
        token_scopes = scope_string.split()

        if not any(scope in token_scopes for scope in required_scopes):
            raise HTTPException(
                status_code=403,
                detail=f"Missing required scope: at least one of {required_scopes}"
            )

        return user_id

    except JWTError as e:
        logger.error(f"[verify_token_and_scope] Error decoding token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")