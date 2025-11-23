from sqlalchemy.orm import Session
from app.models.models import Doctor, ConfiguracionNotificaciones
from app.core.security import get_password_hash


def get_doctor_by_email(db: Session, email: str):
    return db.query(Doctor).filter(Doctor.email == email).first()


def get_doctor(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def create_doctor(db: Session, doctor_in):
    # doctor_in uses 'contrasena' as the field
    hashed = get_password_hash(getattr(doctor_in, 'contrasena', None))
    doctor = Doctor(
        nombre=doctor_in.nombre,
        apellido_paterno=doctor_in.apellido_paterno,
        apellido_materno=doctor_in.apellido_materno,
        email=doctor_in.email,
        telefono=doctor_in.telefono,
        cedula_profesional=doctor_in.cedula_profesional,
        institucion_salud=doctor_in.institucion_salud,
        especialidad=doctor_in.especialidad,
        contraseña_hasheada=hashed,
        foto_perfil_url=str(doctor_in.foto_perfil_url) if doctor_in.foto_perfil_url else None,
        idioma=doctor_in.idioma,
        zona_horaria=doctor_in.zona_horaria,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    # create default notification settings
    cfg = ConfiguracionNotificaciones(doctor_id=doctor.id)
    db.add(cfg)
    db.commit()
    return doctor
