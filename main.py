# main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import joblib

from database.database import Base, engine, SessionLocal
from models.models import RetinopathyData, UserMedicalData

from routes.prediction import router as prediction_router
from routes.retino import router as retino_router  # Nuevo router específico

# 1) Crea la app y configura CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://127.0.0.1:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) Conecta tus routers
app.include_router(prediction_router, prefix="/api", tags=["Prediction"])       # router genérico
app.include_router(retino_router, prefix="/retinopathy", tags=["Retinopathy"])  # router custom

# 3) Crea tablas
Base.metadata.create_all(bind=engine)

# 4) Dependencia para DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
