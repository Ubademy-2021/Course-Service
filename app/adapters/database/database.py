from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL, POSTGRES_SERVER
from app.core.logger import logger


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

SQLALCHEMY_DATABASE_URL = DATABASE_URL


def get_database_url(database_url: str) -> str:
    uri = database_url
    if uri.startswith("postgres://"):
        return uri.replace("postgres://", "postgresql://", 1)
    return uri


logger.info("logged into the following database: " + POSTGRES_SERVER)

engine = create_engine(get_database_url(SQLALCHEMY_DATABASE_URL))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
