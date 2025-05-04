from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.middlewares import add_middlewares
from backend.app.api.routes import (
    card_cud_service,
    card_query_service,
    incidence_CUD_service,
    maintainance_status_query_service,
    maintance_cud_service,
    maintance_query_service,
    type_card_query_service,
    type_card_cud_service,
    user_CUD_service,
    type_movement_cud_service,
    type_transport_cud_service,
    rol_user_cud_service,
    movement_cud_service,
    login_service,
    transport_unit_CUD_service,
    transport_unit_query_service
)

# Initialize the FastAPI app
api_router = FastAPI(title=settings.PROJECT_NAME,debug=True)

# Add global middlewares
add_middlewares(api_router)

# Configure CORS middleware
#api_router.add_middleware(
#    CORSMiddleware,
#    allow_origins=settings.ALLOWED_ORIGINS,  # Allow specific origins
#    allow_credentials=True,
#    allow_methods=["*"],  # Allow all HTTP methods
#    allow_headers=["*"],  # Allow all headers
#)

# Serve static files from the frontend directory
api_router.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Include API service routes
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
api_router.include_router(incidence_CUD_service.app)

# Placeholder for non-functional routes, commented out for now
# api_router.include_router(price_cud_service.app)
# api_router.include_router(incidence_query_service.app)
# api_router.include_router(ticket_cud_service.app)
# api_router.include_router(ticket_query_service.app)
# api_router.include_router(routes_cud_service.app)
# api_router.include_router(shifts_cud_service.app)
# api_router.include_router(shifts_query_service.app)
# api_router.include_router(stops_cud_service.app)
# api_router.include_router(stops_query_service.app)
# api_router.include_router(movement_query_service.app)
# api_router.include_router(payment_cud_service.app)
# api_router.include_router(payment_query_service.app)
# api_router.include_router(maintainance_status_cud_service.app)
api_router.include_router(transport_unit_CUD_service.app)
api_router.include_router(transport_unit_query_service.app)
# api_router.include_router(schedule_cud_service.app)
# api_router.include_router(schedule_query_service.app)
# api_router.include_router(price_query_service.app)
# api_router.include_router(type_transport_query_service.app)
# api_router.include_router(user_query_service.app)
# api_router.include_router(type_movement_query_service.app)
# api_router.include_router(type_card_cud_service.app)
