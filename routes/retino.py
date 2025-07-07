# routes/retino.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import numpy as np
import joblib
import pandas as pd

from database.database import SessionLocal
from models.models import RetinopathyData

router = APIRouter()

# Esquema Pydantic con las 18 variables exactamente:
class RetinoInput(BaseModel):
    PtID: int
    Age: float
    Sex: int
    Duration_of_Diabetes: float
    IMC: float
    Has_Hypertension: int
    TotDlyIns: float
    Is_Pump_User: int
    Glucose_Mean: float
    Glucose_Std: float
    Glucose_CV: float
    Time_In_Range_70_180: float
    Time_Above_180: float
    Time_Above_250: float
    Time_Below_70: float
    Time_Below_54: float
    Education_Score: float
    Keeps_BG_High_Fear: float
    Not_Careful_Eating_Distress: float

# Cargamos el modelo
MODEL = joblib.load("models/retinopathy_model.joblib")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/simular/")
def simular_retino(data: RetinoInput, db: Session = Depends(get_db)):
    if db.query(RetinopathyData).filter_by(PtID=data.PtID).first():
        raise HTTPException(status_code=400, detail="Este PtID ya fue registrado")
    nuevo = RetinopathyData(**data.dict())
    db.add(nuevo)
    db.commit()
    return {"mensaje": "Datos de retinopatía simulados insertados correctamente"}

@router.post("/simular/preview")
def preview_riesgo(data: RetinoInput):
    arr = np.array([[...]])
    proba = MODEL.predict_proba(arr)[0, 1]
    nivel = ...
    return {"nivel_general": nivel, "probabilidad": round(proba, 4)}


@router.get("/predict/{ptid}")
def predict_retino(ptid: int, db: Session = Depends(get_db)):
    row = db.query(RetinopathyData).filter(RetinopathyData.PtID == ptid).first()
    if not row:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Monta el array para predicción
    arr = np.array([[ 
        row.Age, row.Sex, row.Duration_of_Diabetes, row.IMC,
        row.Has_Hypertension, row.TotDlyIns, row.Is_Pump_User,
        row.Glucose_Mean, row.Glucose_Std, row.Glucose_CV,
        row.Time_In_Range_70_180, row.Time_Above_180, row.Time_Above_250,
        row.Time_Below_70, row.Time_Below_54,
        row.Education_Score, row.Keeps_BG_High_Fear, row.Not_Careful_Eating_Distress
    ]])

    # Predicción
    proba = MODEL.predict_proba(arr)[0, 1]
    nivel = "Bajo" if proba < 0.3 else "Moderado" if proba < 0.7 else "Alto"

    # Datos simulados de tendencia (puedes ajustar si tienes históricos reales)
    tendencia = [
        {"time": t, "value": round(proba * factor, 4)}
        for t, factor in [(0, 0.7), (50, 0.85), (100, 1), (150, 0.95), (200, 0.9)]
    ]

    return {
        "nivel_general": nivel,
        "riesgo_retinopatia": nivel,
        "probabilidad": round(proba, 4),
        "tendencia": tendencia,

        # Datos del paciente
        "patient_data": {
            "PtID": row.PtID,
            "Age": row.Age,
            "Sex": row.Sex,
            "Duration_of_Diabetes": row.Duration_of_Diabetes,
            "IMC": row.IMC,
            "Has_Hypertension": row.Has_Hypertension,
            "TotDlyIns": row.TotDlyIns,
            "Is_Pump_User": row.Is_Pump_User,
            "Glucose_Mean": row.Glucose_Mean,
            "Glucose_Std": row.Glucose_Std,
            "Glucose_CV": row.Glucose_CV,
            "Time_In_Range_70_180": row.Time_In_Range_70_180,
            "Time_Above_180": row.Time_Above_180,
            "Time_Above_250": row.Time_Above_250,
            "Time_Below_70": row.Time_Below_70,
            "Time_Below_54": row.Time_Below_54,
            "Education_Score": row.Education_Score,
            "Keeps_BG_High_Fear": row.Keeps_BG_High_Fear,
            "Not_Careful_Eating_Distress": row.Not_Careful_Eating_Distress
        }
    }

