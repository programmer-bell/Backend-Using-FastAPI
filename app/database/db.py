from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Use a synchronous 
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace("+asyncpg", "")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

# Synchronous dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()