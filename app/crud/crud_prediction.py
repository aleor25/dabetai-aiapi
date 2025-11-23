from sqlalchemy.orm import Session
from app.models.models import Prediccion
from sqlalchemy import and_


def create_prediction(db: Session, pred_in):
    p = Prediccion(
        paciente_id=pred_in.paciente_id,
        complicacion=pred_in.complicacion,
        probabilidad=pred_in.probabilidad,
        nivel_riesgo=pred_in.nivel_riesgo,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def get_prediction(db: Session, pred_id: int):
    return db.query(Prediccion).filter(Prediccion.id == pred_id).first()


def list_predictions(db: Session, filters: dict = None, skip: int = 0, limit: int = 50):
    q = db.query(Prediccion)
    if filters:
        if 'paciente_id' in filters:
            q = q.filter(Prediccion.paciente_id == filters['paciente_id'])
        if 'complicacion' in filters:
            q = q.filter(Prediccion.complicacion == filters['complicacion'])
        if 'nivel_riesgo' in filters:
            q = q.filter(Prediccion.nivel_riesgo == filters['nivel_riesgo'])
    total = q.count()
    items = q.offset(skip).limit(limit).all()
    return items, total
