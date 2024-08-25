import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import logging
from entities.user_entity import Base as UserBase
from entities.person_entity import Base as PersonBase

# Load environment variables from .env file
load_dotenv()

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clear_database(Base):
    """Function to clear and recreate the database tables."""
    logger.info("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database cleared and all tables recreated.")

def clear_database_if_needed():
    """Clear the database on startup if the CLEAR_DB_ON_STARTUP environment variable is set to true."""
    if os.getenv("CLEAR_DB_ON_STARTUP") == "true":
        logger.info("CLEAR_DB_ON_STARTUP is true. Clearing database...")
        # Create all tables for all entity bases
        clear_database(UserBase)
        clear_database(PersonBase)
    else:
        logger.info("CLEAR_DB_ON_STARTUP is false. Skipping database clearing.")
