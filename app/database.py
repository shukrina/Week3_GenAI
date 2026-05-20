import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .logging_config import logger
from sqlalchemy import text

# 1. Load the .env file
load_dotenv()

# 2. Get the URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Define these constants OUTSIDE the try block so they are always exportable
Base = declarative_base()
SessionLocal = None
engine = None

if SQLALCHEMY_DATABASE_URL is None:
    logger.error("DATABASE_URL not found in environment variables. Check your .env file.")
else:
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("Database engine created successfully.")
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")

# Dependency to get DB session
def get_db():
    if SessionLocal is None:
        logger.error("SessionLocal is not initialized. Database connection is missing.")
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def execute_raw_sql(query: str, db):
    """Executes a raw SQL string and returns results as a list of dicts."""
    try:
        result = db.execute(text(query))
        # Handle cases where there is no result (like an error or empty return)
        if result.returns_rows:
            return [dict(row._mapping) for row in result.all()]
        return []
    except Exception as e:
        raise e