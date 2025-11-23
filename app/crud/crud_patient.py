from sqlalchemy.orm import Session
from app.models.models import Paciente


def create_patient(db: Session, doctor_id: int, patient_in):
    patient = Paciente(
        doctor_id=doctor_id,
        nombre_completo=patient_in.nombre_completo,
        fecha_nacimiento=patient_in.fecha_nacimiento,
        sexo=patient_in.sexo,
        curp=patient_in.curp,
        telefono=patient_in.telefono,
        direccion=patient_in.direccion,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patient(db: Session, patient_id: int):
    return db.query(Paciente).filter(Paciente.id == patient_id).first()


def list_patients(db: Session, doctor_id: int, skip: int = 0, limit: int = 20, q: str = None):
    query = db.query(Paciente).filter(Paciente.doctor_id == doctor_id)
    if q:
        query = query.filter(Paciente.nombre_completo.ilike(f"%{q}%"))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total
