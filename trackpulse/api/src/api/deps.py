import os
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from src.config import get_settings

# Get FastAPI settings
settings = get_settings()
# Create SQLAlchemy engine using environment variable
engine = create_engine(settings.qdb_database_url, echo=True, connect_args={"check_same_thread": False})
# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create Base class for declarative models
Base = declarative_base()

def get_db() -> Session:
  """Dependency function that yields database sessions"""
  db = SessionLocal()
  try: yield db
  finally: db.close()

SessionDeps = Annotated[Session, Depends(get_db)]
