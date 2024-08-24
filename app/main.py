from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import clear_database_if_needed
from entities.person_entity import Base
from routers.person_router import get_person_router
import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan context manager to handle startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup - checking if database should be cleared...")
    clear_database_if_needed(Base)
    logger.info("Database cleared and all tables recreated.")

    yield  # This is where the application runs

    logger.info("Application shutdown - performing cleanup...")

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(get_person_router())  # Using the dependency-injected router

# Add the middleware for logging
from utils.middleware import log_requests

app.middleware("http")(log_requests)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
