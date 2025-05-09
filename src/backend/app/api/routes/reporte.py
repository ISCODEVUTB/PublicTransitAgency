import logging
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.card import CardOut
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.deps import (
    alerta_mantenimiento_atrasados, alerta_mantenimiento_proximos, total_movimientos,total_buses_activos,promedio_horas_trabajadas,total_usuarios,total_buses_inactivos
)
# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for card-related endpoints
app = APIRouter(prefix="/reporte", tags=["Reporte"])

# Initialize universal controller instance
controller = UniversalController()

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/supervisor", response_class=HTMLResponse)
async def get_supervisor_report(request: Request):
    return templates.TemplateResponse("reporte_supervisor.html", {
        "request": request,
        "total_movimientos": total_movimientos(),
        "total_usuarios": total_usuarios(),
        "total_buses_activos": total_buses_activos(),
        "total_buses_inactivos": total_buses_inactivos(),
        "promedio_horas_trabajadas": promedio_horas_trabajadas()
    })
@app.get("/alert-tec", response_class=HTMLResponse)
async def get_supervisor_report(request: Request,):
    return templates.TemplateResponse("reporte_tecnico.html", {"request": request, "mantenimientos_atrasados":alerta_mantenimiento_atrasados(),"mantenimientos_proximos":alerta_mantenimiento_proximos() })