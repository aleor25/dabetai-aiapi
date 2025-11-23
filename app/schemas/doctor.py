from pydantic import BaseModel, EmailStr, HttpUrl, Field, ConfigDict
from typing import Optional
from datetime import datetime


class DoctorBase(BaseModel):
    nombre: str
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None
    cedula_profesional: Optional[str] = None
    institucion_salud: Optional[str] = None
    especialidad: Optional[str] = None
    foto_perfil_url: Optional[HttpUrl] = None
    idioma: Optional[str] = 'es'
    zona_horaria: Optional[str] = 'UTC'


class DoctorCreate(DoctorBase):
    contrasena: str


class DoctorUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    telefono: Optional[str] = None
    institucion_salud: Optional[str] = None
    especialidad: Optional[str] = None
    foto_perfil_url: Optional[HttpUrl] = None
    idioma: Optional[str] = None
    zona_horaria: Optional[str] = None


class DoctorOut(DoctorBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
