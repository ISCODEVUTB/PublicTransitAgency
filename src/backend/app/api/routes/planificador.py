import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.card import CardCreate, CardOut
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.auth import get_current_user
from backend.app.core.deps import obtener_ruta_con_interconexion
# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/planificador", tags=["Planificador"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse(request,"PlanificarViaje.html", {"request": request})

@app.post("/ubicaciones", response_class=HTMLResponse)
def planificador(request: Request, ubicacion_entrada: str = Form(...), ubicacion_final: str = Form(...)):
    resultado = obtener_ruta_con_interconexion(ubicacion_entrada, ubicacion_final)
    return templates.TemplateResponse(request,"PlanificadorResultado.html", {"request": request, "planif": resultado})