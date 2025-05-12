import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.user import UserCreate, UserOut
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
    ID: int = Form(...),
    Identificacion: int = Form(...),
    Nombre: str = Form(...),
    Apellido: str = Form(...),
    Correo: str = Form(...),
    Contrasena: str = Form(...),
    IDRolUsuario: int = Form(...),
    IDTurno: int = Form(...),
    IDTarjeta: int = Form(...)
):

    try:
        # Verificar si el usuario ya existe
        existing_user = controller.get_by_column(UserOut, "Identificacion", Identificacion)  
        if existing_user:
            raise HTTPException(400, detail="El usuario ya existe con la misma identificación.")

        # Crear usuario
        if existing_user is None or not existing_user:
            new_user = UserCreate(ID=ID, Identificacion=Identificacion, Nombre=Nombre, Apellido=Apellido,
                                Correo=Correo, Contrasena=Contrasena, IDRolUsuario=IDRolUsuario, IDTurno=IDTurno,IDTarjeta=IDTarjeta)
            logger.info(f"Intentando insertar usuario con datos: {new_user.model_dump()}")
            controller.add(new_user)
            logger.info(f"Usuario insertado con ID: {new_user.ID}")  # Verifica si el ID se asigna
            logger.info(f"[POST /create] Usuario creado exitosamente con identificación {Identificacion}")
            return {
                "operation": "create",
                "success": True,
                "data": UserOut(ID=new_user.ID, Identificacion=new_user.Identificacion, Nombre=new_user.Nombre,
                                Apellido=new_user.Apellido,Correo=new_user.Correo,Contrasena=new_user.Contrasena,
                                IDRolUsuario=new_user.IDRolUsuario,IDTurno=new_user.IDTurno, IDTarjeta=new_user.IDTarjeta).model_dump(),
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
    ID: int = Form(...),
    Identificacion: int = Form(...),
    Nombre: str = Form(...),
    Apellido: str = Form(...),
    Correo: str = Form(...),
    Contrasena: str = Form(...),
    IDRolUsuario: int = Form(...),
    IDTurno: int = Form(...),
    IDTarjeta: int = Form(...)
):
    try:
        existing = controller.get_by_column(UserOut,"ID",ID)
        if existing is None or not existing:
            logger.warning(f"[POST /update] Usuario no encontrada: id={ID}")
            raise HTTPException(404, detail="User not found")

        updated_user = UserOut(ID=ID, Identificacion=Identificacion, Nombre=Nombre, Apellido=Apellido,
                       Correo=Correo, Contrasena=Contrasena, IDRolUsuario=IDRolUsuario, IDTurno=IDTurno, IDTarjeta =IDTarjeta)
        controller.update(updated_user)
        Logger.info(f"[POST /update] Usuario actualizada exitosamente: {updated_user}")
        return {
            "operation": "update",
            "success": True,
            "data": UserOut(ID=ID, Identificacion=updated_user.Identificacion, Nombre=updated_user.Nombre,
                            Apellido=updated_user.Apellido,Correo=updated_user.Correo,Contrasena=updated_user.Contrasena,
                            IDRolUsuario=updated_user.IDRolUsuario,IDTurno=updated_user.IDTurno,
                              IDTarjeta=updated_user.IDTarjeta).model_dump(),
            "message": f"User {ID} updated successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_user(
    ID: int = Form(...)
):
    try:
        existing = controller.get_by_column(UserOut,"ID",ID)
        if not existing or existing is None:
            logger.warning(f"[POST /delete] Usuario no encontrado en la base de datos: id={ID}")
            raise HTTPException(404, detail="User not found")

        logger.info(f"[POST /delete] Eliminando usuario con id={ID}")
        controller.delete(existing) 
        logger.info(f"[POST /delete] Usuario eliminada exitosamente: id={ID}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"User {ID} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
