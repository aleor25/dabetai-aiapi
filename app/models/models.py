from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
from sqlalchemy.orm import relationship
from app.services.database import Base


class RetinopathyData(Base):
    __tablename__ = "retinopathy_data"

    PtID = Column(Integer, primary_key=True, index=True)
    Age = Column(Float)
    Sex = Column(Integer)
    Duration_of_Diabetes = Column(Float)
    IMC = Column(Float)
    Has_Hypertension = Column(Integer)
    TotDlyIns = Column(Float)
    Is_Pump_User = Column(Integer)
    Glucose_Mean = Column(Float)
    Glucose_Std = Column(Float)
    Glucose_CV = Column(Float)
    Time_In_Range_70_180 = Column(Float)
    Time_Above_180 = Column(Float)
    Time_Above_250 = Column(Float)
    Time_Below_70 = Column(Float)
    Time_Below_54 = Column(Float)
    Education_Score = Column(Float)
    Keeps_BG_High_Fear = Column(Float)
    Not_Careful_Eating_Distress = Column(Float)


class UserMedicalData(Base):
    __tablename__ = "user_medical_data"

    user_id = Column(Integer, primary_key=True, index=True)
    age = Column(Float)
    glucose = Column(Float)
    blood_pressure = Column(Float)


class DeviceToken(Base):
    __tablename__ = "device_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    token = Column(String(512), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


# New domain models requested


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(128), nullable=False)
    apellido_paterno = Column(String(128), nullable=True)
    apellido_materno = Column(String(128), nullable=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    telefono = Column(String(64), nullable=True)
    cedula_profesional = Column(String(128), nullable=True)
    institucion_salud = Column(String(256), nullable=True)
    especialidad = Column(String(128), nullable=True)
    contraseña_hasheada = Column(String(256), nullable=False)
    foto_perfil_url = Column(String(512), nullable=True)
    idioma = Column(String(32), default='es')
    zona_horaria = Column(String(64), default='UTC')
    created_at = Column(DateTime, default=datetime.now)


class ConfiguracionNotificaciones(Base):
    __tablename__ = "configuracion_notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    recibir_alertas_criticas = Column(Boolean, default=True)
    recibir_alertas_incumplimiento = Column(Boolean, default=True)
    recibir_recordatorios_citas = Column(Boolean, default=True)
    recibir_informes_periodicos = Column(Boolean, default=True)

    doctor = relationship('Doctor')


class SesionActiva(Base):
    __tablename__ = "sesiones_activas"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    token = Column(String(512), nullable=False, index=True)
    dispositivo = Column(String(256), nullable=True)
    ubicacion = Column(String(256), nullable=True)
    fecha_inicio = Column(DateTime, default=datetime.now)

    doctor = relationship('Doctor')


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False, index=True)
    nombre_completo = Column(String(256), nullable=False)
    fecha_nacimiento = Column(DateTime, nullable=True)
    sexo = Column(String(8), nullable=True)
    curp = Column(String(32), nullable=True)
    telefono = Column(String(64), nullable=True)
    direccion = Column(Text, nullable=True)

    doctor = relationship('Doctor')


class MetricaSalud(Base):
    __tablename__ = "metricas_salud"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False, index=True)
    tipo_metrica = Column(String(64), nullable=False)
    valor = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    paciente = relationship('Paciente')


class Prediccion(Base):
    __tablename__ = "predicciones"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False, index=True)
    complicacion = Column(String(128), nullable=False)
    probabilidad = Column(Float, nullable=False)
    nivel_riesgo = Column(String(32), nullable=True)
    fecha = Column(DateTime, default=datetime.now)

    paciente = relationship('Paciente')


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False, index=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=True)
    tipo = Column(String(64), nullable=False)
    mensaje = Column(Text, nullable=False)
    leida = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.now)

    doctor = relationship('Doctor')
    paciente = relationship('Paciente')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True, nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
