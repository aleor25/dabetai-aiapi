# database/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. URL de la base de datos (SQLite para demo rápida)
SQLALCHEMY_DATABASE_URL = "sqlite:///./dabetai.db"

# 2. Crear el engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Declarative base
Base = declarative_base()
