import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.card import CardCreate, CardOut
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/planificador", tags=["Planificador"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Ruta GET para cargar la página del planificador
@app.get("/consultar", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse(request,"PlanificarViaje.html", {"request": request})

# Ruta POST para manejar las ubicaciones
@app.post("/ubicaciones", response_class=HTMLResponse)
def planificador(request: Request, ubicacion_entrada: str = Form(...), ubicacion_final: str = Form(...)):
    try:
        # Intentamos obtener el resultado de la interconexión
        resultado = controller.obtener_ruta_con_interconexion(ubicacion_entrada, ubicacion_final)
        
        # Verificamos si el resultado es vacío o None, y gestionamos el error
        if not resultado:
            logger.error(f"No se encontraron interconexiones para {ubicacion_entrada} y {ubicacion_final}.")
            return templates.TemplateResponse("PlanificadorResultado.html", {"request": request, "planif": "No se encontraron interconexiones."})

        # Si todo está bien, retornamos el resultado a la plantilla
        return templates.TemplateResponse("PlanificadorResultado.html", {"request": request, "planif": resultado})

    except Exception as e:
        # Logueamos el error si algo falla
        logger.error(f"Error al obtener las rutas con interconexión: {str(e)}")
        # Retornamos un mensaje de error al usuario
        return templates.TemplateResponse("PlanificadorResultado.html", {"request": request, "planif": "Hubo un error al procesar la solicitud. Por favor, intente nuevamente."})
