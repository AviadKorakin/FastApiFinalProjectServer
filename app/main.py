
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import clear_database_if_needed
from routers.avatar_image_router import get_avatar_image_router
from routers.found_pet_report_router import get_found_pet_report_router
from routers.lost_pet_report_router import get_lost_pet_report_router
from routers.medical_history_router import get_medical_history_router
from routers.pet_router import get_pet_router
from routers.provider_phone_router import get_provider_phone_router
from routers.service_provider_location_router import get_service_provider_location_router
from routers.service_provider_router import get_service_provider_router
from routers.user_provider_router import get_user_provider_router
from routers.user_router import get_user_router
import logging

from routers.working_hours_router import get_working_hours_router

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan context manager to handle startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup - checking if database should be cleared...")

    # Clear and create database tables if needed
    await clear_database_if_needed()

    yield  # This is where the application runs

    logger.info("Application shutdown - performing cleanup...")

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(get_user_router(),prefix="/users", tags=["Users"])  # Using the dependency-injected router
#app.include_router(get_person_router(),prefix="/persons",tags=["Persons"])  # Using the dependency-injected router
#app.include_router(get_image_router(),prefix="/images",tags=["Images"]) # Using the dependency-injected router
app.include_router(get_avatar_image_router(),prefix="/avatar_images",tags=["Avatar Images"])
app.include_router(get_pet_router(),prefix="/pets",tags=["Pets"])
app.include_router(get_lost_pet_report_router(), prefix="/lost_pet_reports", tags=["Lost Pet Reports"])
app.include_router(get_found_pet_report_router(),prefix="/found_pet_reports", tags=["Found Pet Reports"])
app.include_router(get_medical_history_router(),prefix="/medical_history",tags=["Medical History"])
app.include_router(get_service_provider_router(),prefix="/service_providers",tags=["Service Providers"])
app.include_router(get_working_hours_router(), prefix="/working_hours", tags=["Working Hours"])
app.include_router(get_provider_phone_router(),prefix="/provider_phones", tags=["Provider Phones"])
app.include_router(get_user_provider_router(),prefix="/users_providers",tags=["Users Providers"])
app.include_router(get_service_provider_location_router(),prefix="/service_provider_locations",tags=["Service Provider Locations"])

# Add the middleware for logging
from utils.middleware import log_requests
app.middleware("http")(log_requests)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
