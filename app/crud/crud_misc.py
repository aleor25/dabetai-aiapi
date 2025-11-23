from sqlalchemy.orm import Session
from app.models.models import MetricaSalud, Notificacion, SesionActiva


def create_metric(db: Session, metric_in):
    m = MetricaSalud(
        paciente_id=metric_in.paciente_id,
        tipo_metrica=metric_in.tipo_metrica,
        valor=metric_in.valor,
        timestamp=metric_in.timestamp,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


def create_notification(db: Session, doctor_id: int, tipo: str, mensaje: str, paciente_id: int = None):
    n = Notificacion(doctor_id=doctor_id, paciente_id=paciente_id, tipo=tipo, mensaje=mensaje)
    db.add(n)
    db.commit()
    db.refresh(n)
    return n


def list_notifications(db: Session, doctor_id: int, tipo: str = None, skip: int = 0, limit: int = 50):
    q = db.query(Notificacion).filter(Notificacion.doctor_id == doctor_id)
    if tipo:
        q = q.filter(Notificacion.tipo == tipo)
    total = q.count()
    items = q.offset(skip).limit(limit).all()
    return items, total


def mark_all_notifications_read(db: Session, doctor_id: int):
    db.query(Notificacion).filter(Notificacion.doctor_id == doctor_id).update({Notificacion.leida: True})
    db.commit()


def list_sessions(db: Session, doctor_id: int):
    return db.query(SesionActiva).filter(SesionActiva.doctor_id == doctor_id).all()


def delete_session(db: Session, session_id: int, doctor_id: int):
    s = db.query(SesionActiva).filter(SesionActiva.id == session_id, SesionActiva.doctor_id == doctor_id).first()
    if s:
        db.delete(s)
        db.commit()
        return True
    return False
