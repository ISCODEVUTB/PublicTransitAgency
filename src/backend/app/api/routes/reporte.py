import logging
from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from backend.app.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger("reporte_logger")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Crear el enrutador para los endpoints de reporte
app = APIRouter(prefix="/reporte", tags=["Reporte"])

# Inicializar el controlador universal

# Configuración del motor de plantillas Jinja2
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/supervisor", response_class=HTMLResponse)
async def get_supervisor_report(request: Request):
    try:
        # Obtener datos desde el controlador
        report_data = {
            "total_movimientos": controller.total_movimientos(),
            "total_usuarios": controller.total_usuarios(),
            "promedio_horas_trabajadas": controller.promedio_horas_trabajadas(),
        }
        logger.info("Reporte de supervisor generado exitosamente.")
        return templates.TemplateResponse("reporte_supervisor.html", {"request": request, **report_data})
    except Exception as e:
        # Log de error con detalles
        logger.error(f"Error al generar el reporte de supervisor: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Ocurrió un error al generar el reporte de supervisor."}
        )

@app.get("/alert-tec", response_class=HTMLResponse)
async def get_technical_alert_report(request: Request):
    try:
        # Obtener datos desde el controlador
        report_data = {
            "mantenimientos_atrasados": controller.alerta_mantenimiento_atrasados(),
            "mantenimientos_proximos": controller.alerta_mantenimiento_proximos(),
        }
        logger.info("Reporte técnico generado exitosamente.")
        return templates.TemplateResponse("reporte_tecnico.html", {"request": request, **report_data})
    except Exception as e:
        # Log de error con detalles
        logger.error(f"Error al generar el reporte técnico: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Ocurrió un error al generar el reporte técnico."}
        )
