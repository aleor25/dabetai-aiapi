from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class HealthMetricIn(BaseModel):
    paciente_id: int
    tipo_metrica: str
    valor: float
    timestamp: Optional[datetime] = None


class NotificationOut(BaseModel):
    id: int
    tipo: str
    mensaje: str
    leida: bool
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SessionOut(BaseModel):
    id: int
    dispositivo: Optional[str] = None
    ubicacion: Optional[str] = None
    fecha_inicio: datetime

    model_config = ConfigDict(from_attributes=True)
