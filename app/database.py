import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker  # <-- This is the correct sessionmaker for async usage
from dotenv import load_dotenv
import logging
from entities.base import Base

# Load environment variables from .env file
load_dotenv()

# THESE IMPORTS ARE USED FOR Base.metadata.create_all(bind=engine) don't remove them!
from entities.user_entity import UserEntity
from entities.person_entity import Person
from entities.image_entity import ImageEntity
from entities.pet_entity import PetEntity
from entities.notification_entity import NotificationEntity
from entities.pet_image_entity import PetImageEntity
from entities.avatar_image_entity import AvatarImageEntity
from entities.found_pet_image_entity import FoundPetImageEntity
from entities.lost_pet_report_entity import LostPetReportEntity
from entities.provider_phone_entity import ProviderPhoneEntity
from entities.working_hours_entity import WorkingHoursEntity
from entities.found_pet_report_entity import FoundPetReportEntity
from entities.medical_history_entity import MedicalHistoryEntity
from entities.service_provider_entity import ServiceProviderEntity
from entities.service_request_entity import ServiceRequestEntity
from entities.user_provider_association_entity import UserProviderAssociationEntity
from entities.service_provider_location_entity import ServiceProviderLocationEntity
from entities.service_provider_image_entity import ServiceProviderImageEntity

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve the async database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the async SQLAlchemy engine with connection pooling
async_engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,         # Number of database connections to maintain in the pool
    max_overflow=10,      # How many connections can be added beyond the pool size
    pool_pre_ping=True,   # Check if connections are alive before using them
    pool_timeout=30,      # Timeout for acquiring a connection from the pool
)

# Create an async session factory using async_sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,  # Disable session expiration on commit
    autoflush=False
)

# Dependency to get a new async database session
async def get_db() -> AsyncSession:
    """Dependency to get a new asynchronous database session."""
    async with AsyncSessionLocal() as session:
        yield session

# Function to clear and recreate the database tables asynchronously
async def clear_database(Base):
    """Function to clear and recreate the database tables asynchronously."""
    logger.info("Dropping all tables asynchronously...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Creating all tables asynchronously...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database cleared and all tables recreated asynchronously.")

# Function to check if database clearing is needed and execute the clear operation
async def clear_database_if_needed():
    """Clear the database on startup if the CLEAR_DB_ON_STARTUP environment variable is set to true."""
    if os.getenv("CLEAR_DB_ON_STARTUP") == "true":
        logger.info("CLEAR_DB_ON_STARTUP is true. Clearing database asynchronously...")
        await clear_database(Base)
    else:
        logger.info("CLEAR_DB_ON_STARTUP is false. Skipping database clearing.")
