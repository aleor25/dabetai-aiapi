from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

router = APIRouter()

# --- Modelo de entrada para validación ---
class PatientInput(BaseModel):
    Edad: int
    Sexo: int
    IMC: float
    HbA1c: float
    Presion_Sistolica: int
    Presion_Diastolica: int
    Colesterol: int
    Glucosa_Antes_Comida: float
    Glucosa_Despues_Comida: float
    Duracion_Diabetes: int
    Actividad_Fisica: int
    Fuma: int
    Come_Sano: int
    Medicación_Regular: int
    Historial_Familiar: int

# --- Rutas y configuración de modelos ---
MODEL_PATHS = {
    "retinopathy": "../models/retinopathy_model.joblib",
    "nephropathy": "../models/nephropathy_model.joblib",
    "neuropathy": "../models/neuropathy_model.joblib",
    "diabetic_foot": "../models/diabetic_foot_model.joblib",
}

@router.post("/predict/{complication_name}")
def predict(complication_name: str, input_data: PatientInput):
    # Validar nombre de complicación
    if complication_name not in MODEL_PATHS:
        raise HTTPException(status_code=400, detail="Complicación no reconocida")

    model_path = MODEL_PATHS[complication_name]
    if not os.path.exists(model_path):
        raise HTTPException(status_code=500, detail="Modelo no disponible")

    # Cargar modelo
    model = joblib.load(model_path)

    # Convertir entrada en DataFrame
    df_input = pd.DataFrame([input_data.dict()])

    # Realizar predicción
    try:
        proba = model.predict_proba(df_input)[0][1]
        clase = int(proba >= 0.5)
        return {
            "complication": complication_name,
            "riesgo_probabilidad": round(proba, 4),
            "riesgo_clase": clase,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir: {str(e)}")
