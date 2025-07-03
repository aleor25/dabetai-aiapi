from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración CORS (después de crear app)
origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    # agrega más orígenes si usas otros puertos/dominios
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo (ajusta la ruta según tu proyecto)
model = joblib.load("models/retinopathy_model.joblib")

# Definir esquema de entrada para los datos que realmente usarás
class PatientData(BaseModel):
    age: float
    glucose: float
    blood_pressure: float
    # agrega más campos si los necesitas

@app.post("/Prediction")
def Prediction(data: PatientData):
    features = np.array([[data.age, data.glucose, data.blood_pressure]])
    
    risk_proba = model.predict_proba(features)[0, 1]

    if risk_proba < 0.3:
        nivel_general = "Bajo"
    elif risk_proba < 0.7:
        nivel_general = "Moderado"
    else:
        nivel_general = "Alto"

    tendencia = [
        {"time": 0, "value": risk_proba * 0.7},
        {"time": 50, "value": risk_proba * 0.85},
        {"time": 100, "value": risk_proba},
        {"time": 150, "value": risk_proba * 0.95},
        {"time": 200, "value": risk_proba * 0.9},
    ]

    return {
        "nivel_general": nivel_general,
        "riesgo_retinopatia": nivel_general,
        "tendencia": tendencia,
        "probabilidad": round(risk_proba, 4)
    }
