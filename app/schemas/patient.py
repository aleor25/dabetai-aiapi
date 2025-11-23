from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class PatientBase(BaseModel):
    nombre_completo: str
    fecha_nacimiento: Optional[datetime] = None
    sexo: Optional[str] = None
    curp: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    sexo: Optional[str] = None
    curp: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class PatientOut(PatientBase):
    id: int
    doctor_id: int

    model_config = ConfigDict(from_attributes=True)
