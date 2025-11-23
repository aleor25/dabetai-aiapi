from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class PredictionBase(BaseModel):
    paciente_id: int
    complicacion: str
    probabilidad: float
    nivel_riesgo: Optional[str] = None


class PredictionCreate(PredictionBase):
    pass


class PredictionOut(PredictionBase):
    id: int
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)


class PredictionList(BaseModel):
    items: List[PredictionOut]
    total: int
