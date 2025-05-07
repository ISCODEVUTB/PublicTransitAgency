from fastapi import APIRouter, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.payments import Payment
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/payments", tags=["payments"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_pago_form(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for creating a new payment. Requires authentication.
    """
    return templates.TemplateResponse("CrearPago.html", {"request": request})

@app.post("/create")
def crear_pago(
    id: int = Form(...),
    iduser: int = Form(...),
    amount: float = Form(...),
    idmovement: int = Form(...),
    idtransportunit: int = Form(...),
    idcard: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Create a new payment. Requires authentication.
    """
    pago = Payment(
        id=id,
        iduser=iduser,
        amount=amount,
        idmovement=idmovement,
        idtransportunit=idtransportunit,
        idcard=idcard
    )
    try:
        controller.add(pago)
        return {
            "operation": "create",
            "success": True,
            "data": pago,
            "message": "Pago creado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_pago_form(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for updating a payment. Requires authentication.
    """
    return templates.TemplateResponse("ActualizarPago.html", {"request": request})

@app.post("/update")
def actualizar_pago(
    id: int = Form(...),
    iduser: int = Form(...),
    amount: float = Form(...),
    idmovement: int = Form(...),
    idtransportunit: int = Form(...),
    idcard: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Update an existing payment. Requires authentication.
    """
    pago = Payment(
        id=id,
        iduser=iduser,
        amount=amount,
        idmovement=idmovement,
        idtransportunit=idtransportunit,
        idcard=idcard
    )
    try:
        controller.update(pago)
        return {
            "operation": "update",
            "success": True,
            "data": pago,
            "message": "Pago actualizado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

@app.get("/delete", response_class=HTMLResponse)
def eliminar_pago_form(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for deleting a payment. Requires authentication.
    """
    return templates.TemplateResponse("EliminarPago.html", {"request": request})

@app.post("/delete")
def eliminar_pago(
    id: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Delete a payment by ID. Requires authentication.
    """
    pago = Payment(id=id)
    try:
        controller.delete(pago)
        return {
            "operation": "delete",
            "success": True,
            "message": "Pago eliminado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
