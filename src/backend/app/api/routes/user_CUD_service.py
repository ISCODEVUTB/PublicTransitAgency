import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.user import UserCreate, UserOut
from backend.app.logic.universal_controller_sql import UniversalController
#from backend.app.core.auth import get_current_user

# Configuración de logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/user", tags=["user"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def index_create(
    request: Request
):
    return templates.TemplateResponse("CrearUsuario.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request
):
    return templates.TemplateResponse("ActualizarUsuario.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request
):
    return templates.TemplateResponse("EliminarUsuario.html", {"request": request})


@app.post("/create")
async def create_user(
    id: int = Form(...),
    identification: int = Form(...),
    name: str = Form(...),
    lastname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    idtype_user: int = Form(...),
    idturn: int = Form(...)
):

    try:
        # Verificar si el usuario ya existe
        existing_user = controller.get_by_column(UserOut, "identification", identification)  
        if existing_user:
            raise HTTPException(400, detail="El usuario ya existe con la misma identificación.")

        # Crear usuario
        new_user = UserCreate(id=id, identification=identification, name=name, lastname=lastname,
                              email=email, password=password, idtype_user=idtype_user, idturn=idturn)
        logger.info(f"Intentando insertar usuario con datos: {new_user.model_dump()}")
        controller.add(new_user)
        logger.info(f"Usuario insertado con ID: {new_user.id}")  # Verifica si el ID se asigna
        logger.info(f"[POST /create] Usuario creado exitosamente con identificación {identification}")
        return {
            "operation": "create",
            "success": True,
            "data": UserOut(id=new_user.id, identification=new_user.identification, name=new_user.name,
                            lastname=new_user.lastname,email=new_user.email,password=new_user.password,
                            idtype_user=new_user.idtype_user,idturn=new_user.idturn).model_dump(),
            "message": "User created successfully."
        }
        
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_user(
    id: int = Form(...),
    identification: int = Form(...),
    name: str = Form(...),
    lastname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    idtype_user: int = Form(...),
    idturn: int = Form(...)
):
    try:
        existing = controller.get_by_id(UserOut, id)
        if existing is None:
            logger.warning(f"[POST /update] Usuario no encontrada: id={id}")
            raise HTTPException(404, detail="User not found")

        updated_user = UserOut(id=id, identification=identification, name=name, lastname=lastname,
                       email=email, password=password, idtype_user=idtype_user, idturn=idturn)
        controller.update(updated_user)
        logger.info(f"[POST /update] Usuario actualizada exitosamente: {updated_user}")
        return {
            "operation": "update",
            "success": True,
            "data": UserOut(id=id, identification=updated_user.identification, name=updated_user.name,
                            lastname=updated_user.lastname,email=updated_user.email,password=updated_user.password,
                            idtype_user=updated_user.idtype_user,idturn=updated_user.idturn).model_dump(),
            "message": f"User {id} updated successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_user(
    id: int = Form(...)
):
    try:
        existing = controller.get_by_id(UserOut, id)
        if not existing:
            logger.warning(f"[POST /delete] Usuario no encontrado en la base de datos: id={id}")
            raise HTTPException(404, detail="User not found")

        logger.info(f"[POST /delete] Eliminando usuario con id={id}")
        controller.delete(existing) 
        logger.info(f"[POST /delete] Usuario eliminada exitosamente: id={id}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"User {id} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
