#import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.rol_user import RolUserCreate, RolUserOut
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.auth import get_current_user

# Configuración de logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/roluser", tags=["roluser"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    #current_user: dict = Security(get_current_user,
        #scopes=["system", "administrador"])
):
    #logger.info(f"[GET /crear] Usuario: {current_user['user_id']} - Mostrando formulario de creación de rol de usuario")
    return templates.TemplateResponse("CrearRolUsuario.html", {"request": request})

@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /actualizar] Usuario: {current_user['user_id']} - Mostrando formulario de actualización de rol de usuario")
    return templates.TemplateResponse("ActualizarRolUsuario.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /eliminar] Usuario: {current_user['user_id']} - Mostrando formulario de eliminación de rol de usuario")
    return templates.TemplateResponse("EliminarRolUsuario.html", {"request": request})

#
@app.post("/create")
async def create_roluser(
    ID: int = Form(...),
    Rol: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /create] Usuario: {current_user['user_id']} - Intentando crear usuario de tipo {Rol}")

    try:
        # Verificar si el rol de usuario ya existe
        existing_user = controller.get_by_column(RolUserOut, "Rol", Rol)  
        if existing_user:
            logger.warning(f"[POST /create] Error de validación: El rol de usuario ya existe con ID {ID}")
            raise HTTPException(400, detail="El rol de usuario ya existe con la misma identificación.")

        # Crear usuario
        new_roluser = RolUserCreate(ID=ID, Rol=Rol)
        logger.info(f"Intentando insertar rol de usuario con datos: {new_roluser.model_dump()}")
        controller.add(new_roluser)
        logger.info(f"Rol de Usuario insertado con ID: {new_roluser.ID}")  # Verifica si el ID se asigna
        logger.info(f"[POST /create] Rol de Usuario creado exitosamente con identificación {ID}")
        return {
            "operation": "create",
            "success": True,
            "data": RolUserOut(ID=new_roluser.ID, Rol=new_roluser.Rol).model_dump(),
            "message": "RolUser created successfully."
        }
        
    except ValueError as e:
        #logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        #logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_roluser(
    ID: int = Form(...),
    Rol: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /update] Usuario: {current_user['user_id']} - Actualizando rol de usuario ID={ID}")
    try:
        existing = controller.get_by_id(RolUserOut, ID)
        if existing is None:
            logger.warning(f"[POST /update] Rol de Usuario no encontrada: ID={ID}")
            raise HTTPException(404, detail="RolUser not found")

        updated_roluser = RolUserOut(ID=ID, Rol=Rol)
        controller.update(updated_roluser)
        #logger.info(f"[POST /update] Usuario actualizada exitosamente: {updated_roluser}")
        return {
            "operation": "update",
            "success": True,
            "data": RolUserOut(ID=ID, Rol=updated_roluser.Rol).model_dump(),
            "message": f"RolUser {ID} updated successfully."
        }
    except ValueError as e:
        #logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_roluser(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /delete] Usuario: {current_user['user_id']} - Eliminando rol de usuario ID={ID}")
    try:
        existing = controller.get_by_id(RolUserOut, ID)
        if not existing:
            logger.warning(f"[POST /delete] Rol de Usuario no encontrado en la base de datos: ID={ID}")
            raise HTTPException(404, detail="RolUser not found")

        logger.info(f"[POST /delete] Eliminando rol de usuario con ID={ID}")
        controller.delete(existing) 
        logger.info(f"[POST /delete] Rol de Usuario eliminada exitosamente: ID={ID}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"RolUser {ID} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        #logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
