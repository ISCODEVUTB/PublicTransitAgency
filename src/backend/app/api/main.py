from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.app.core.config import settings
from backend.app.core.middlewares import add_middlewares
from backend.app.logic.universal_controller_instance import universal_controller
from backend.app.api.routes import (
    incidence_cud_service,
    maintainance_status_query_service,
    login_service,
    incidence_query_service,
    ticket_cud_service,
    ticket_query_service,
    routes_cud_service,
    shifts_cud_service,
    shifts_query_service,
    stops_cud_service,
    stops_query_service,
    payment_cud_service,
    payment_query_service,
    maintainance_status_cud_service,
    transport_unit_cud_service,
    transport_unit_query_service,
    schedule_cud_service,
    schedule_query_service,
    routes_query_service,
    reporte,
    planificador,
    rutaparada_query_service
)
from backend.app.api.routes.card_service import (card_cud_service, card_query_service)
from backend.app.api.routes.maintainance_service import (maintance_cud_service, maintance_query_service)
from backend.app.api.routes.type_card_service import (type_card_cud_service, type_card_query_service)
from backend.app.api.routes.user_service import (user_CUD_service, user_query_service)
from backend.app.api.routes.movement_service import (movement_cud_service, movement_query_service)
from backend.app.api.routes.price_service import (price_cud_service, price_query_service)
from backend.app.api.routes.type_movement_service import (type_movement_cud_service, type_movement_query_service)
from backend.app.api.routes.type_transport_service import (type_transport_cud_service, type_transport_query_service)
from backend.app.api.routes.rol_user_service import (rol_user_cud_service, rol_user_query_service)
from backend.app.api.routes.pqr_service import (pqr_cud_service, pqr_query_service)
from backend.app.api.routes.asistance_service import (asistance_cud_service, asistance_query_service)
from backend.app.api.routes.behavior_service import (behavior_cud_service, behavior_query_service)


# Inicializar la aplicación FastAPI
api_router = FastAPI(title=settings.PROJECT_NAME)

# Añadir middlewares globales
add_middlewares(api_router)

# Configurar CORS
api_router.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
api_router.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Contexto asincrónico para el ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Conexión a la base de datos al iniciar la aplicación
        print("Conexión establecida con la base de datos")
        yield
    finally:
        # Cerrar la conexión al apagar la aplicación
        if universal_controller.conn:
            universal_controller.conn.close()
            print("Conexión cerrada correctamente")

# Asignar el ciclo de vida a la aplicación
api_router.router.lifespan = lifespan

# Incluir rutas de los microservicios
api_router.include_router(reporte.app)
api_router.include_router(planificador.app)
api_router.include_router(type_card_cud_service.app)
api_router.include_router(login_service.app)
api_router.include_router(card_cud_service.app)
api_router.include_router(card_query_service.app)
api_router.include_router(maintance_cud_service.app)
api_router.include_router(maintance_query_service.app)
api_router.include_router(type_card_query_service.app)
api_router.include_router(user_CUD_service.app)
api_router.include_router(type_movement_cud_service.app)
api_router.include_router(type_transport_cud_service.app)
api_router.include_router(rol_user_cud_service.app)
api_router.include_router(movement_cud_service.app)
api_router.include_router(maintainance_status_query_service.app)
api_router.include_router(incidence_cud_service.app)
api_router.include_router(price_cud_service.app)
api_router.include_router(incidence_query_service.app)
api_router.include_router(ticket_cud_service.app)
api_router.include_router(ticket_query_service.app)
api_router.include_router(routes_cud_service.app)
api_router.include_router(shifts_cud_service.app)
api_router.include_router(shifts_query_service.app)
api_router.include_router(stops_cud_service.app)
api_router.include_router(stops_query_service.app)
api_router.include_router(movement_query_service.app)
api_router.include_router(payment_cud_service.app)
api_router.include_router(payment_query_service.app)
api_router.include_router(maintainance_status_cud_service.app)
api_router.include_router(transport_unit_cud_service.app)
api_router.include_router(transport_unit_query_service.app)
api_router.include_router(schedule_cud_service.app)
api_router.include_router(schedule_query_service.app)
api_router.include_router(routes_query_service.app)
api_router.include_router(user_query_service.app)
api_router.include_router(price_query_service.app)
api_router.include_router(type_movement_query_service.app)
api_router.include_router(type_transport_query_service.app)
api_router.include_router(rol_user_query_service.app)
api_router.include_router(pqr_query_service.app)
api_router.include_router(pqr_cud_service.app)
api_router.include_router(asistance_cud_service.app)
api_router.include_router(asistance_query_service.app)
api_router.include_router(behavior_cud_service.app)
api_router.include_router(behavior_query_service.app)
api_router.include_router(rutaparada_query_service.app)