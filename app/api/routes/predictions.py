from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db, get_current_user
from app.crud import crud_prediction
from app.schemas.prediction import PredictionOut, PredictionList
from app.models.models import Prediccion, Paciente
from typing import Optional

router = APIRouter()


@router.get('/', response_model=PredictionList)
def list_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    paciente_id: Optional[int] = None,
    complicacion: Optional[str] = None,
    nivel_riesgo: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """List predictions with optional filters."""
    filters = {}
    if paciente_id:
        filters['paciente_id'] = paciente_id
    if complicacion:
        filters['complicacion'] = complicacion
    if nivel_riesgo:
        filters['nivel_riesgo'] = nivel_riesgo
    items, total = crud_prediction.list_predictions(db, filters=filters, skip=skip, limit=limit)
    return {"items": items, "total": total}


@router.get('/{prediction_id}', response_model=PredictionOut)
def get_prediction(prediction_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Get a specific prediction by ID."""
    p = crud_prediction.get_prediction(db, prediction_id)
    if not p:
        raise HTTPException(status_code=404, detail='Prediction not found')
    return p


@router.get('/stats', tags=["Predictions"])
def prediction_stats(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get aggregated statistics of predictions.
    Returns distribution of complications and risk levels.
    """
    # Get predictions for current doctor's patients
    doctor_patients = db.query(Paciente).filter(Paciente.doctor_id == current_user.id).all()
    patient_ids = [p.id for p in doctor_patients]
    
    if not patient_ids:
        return {
            "by_complication": {},
            "by_risk_level": {},
            "total_predictions": 0
        }
    
    # Count by complication
    complication_stats = db.query(
        Prediccion.complicacion,
        func.count(Prediccion.id).label('count')
    ).filter(Prediccion.paciente_id.in_(patient_ids)).group_by(Prediccion.complicacion).all()
    
    by_complication = {stat[0]: stat[1] for stat in complication_stats}
    
    # Count by risk level
    risk_stats = db.query(
        Prediccion.nivel_riesgo,
        func.count(Prediccion.id).label('count')
    ).filter(Prediccion.paciente_id.in_(patient_ids)).group_by(Prediccion.nivel_riesgo).all()
    
    by_risk_level = {stat[0]: stat[1] for stat in risk_stats}
    
    total = db.query(Prediccion).filter(Prediccion.paciente_id.in_(patient_ids)).count()
    
    return {
        "by_complication": by_complication,
        "by_risk_level": by_risk_level,
        "total_predictions": total
    }
