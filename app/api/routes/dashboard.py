from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models.models import Paciente, Prediccion, Notificacion

router = APIRouter()


@router.get('/summary')
def dashboard_summary(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Dashboard summary con agregaciones de datos del doctor actual.
    Retorna: contadores, pacientes en riesgo, control glucémico, actividad reciente.
    """
    doctor_id = current_user.id
    
    # Contadores
    total_patients = db.query(Paciente).filter(Paciente.doctor_id == doctor_id).count()
    
    # Pacientes en riesgo (predicciones con riesgo alto)
    high_risk_patients = db.query(Prediccion).filter(
        Prediccion.nivel_riesgo == 'High'
    ).count()
    
    # Notificaciones sin leer
    unread_notifications = db.query(Notificacion).filter(
        Notificacion.doctor_id == doctor_id,
        Notificacion.leida == False
    ).count()
    
    # Pacientes que requieren atención (ultimas predicciones con riesgo alto)
    patients_requiring_attention = db.query(Paciente, Prediccion).filter(
        Paciente.doctor_id == doctor_id,
        Prediccion.paciente_id == Paciente.id,
        Prediccion.nivel_riesgo == 'High'
    ).limit(5).all()
    
    attention_list = [
        {
            "patient_id": p[0].id,
            "patient_name": p[0].nombre_completo,
            "risk_level": p[1].nivel_riesgo,
            "complication": p[1].complicacion,
            "probability": p[1].probabilidad,
            "created_at": p[1].fecha.isoformat() if p[1].fecha else None
        }
        for p in patients_requiring_attention
    ]
    
    # Actividad reciente (ultimas notificaciones)
    recent_activity = db.query(Notificacion).filter(
        Notificacion.doctor_id == doctor_id
    ).order_by(Notificacion.timestamp.desc()).limit(10).all()
    
    activity_list = [
        {
            "id": n.id,
            "type": n.tipo,
            "message": n.mensaje,
            "is_read": n.leida,
            "timestamp": n.timestamp.isoformat() if n.timestamp else None
        }
        for n in recent_activity
    ]
    
    return {
        "summary_cards": {
            "patients_total": total_patients,
            "alerts_critical": high_risk_patients,
            "unread_notifications": unread_notifications
        },
        "patients_requiring_attention": attention_list,
        "recent_activity": activity_list,
        "charts": {
            "complication_distribution": {},
            "prediction_trend": []
        }
    }


@router.get('/')
def dashboard(db=Depends(get_db), current_user=Depends(get_current_user)):
    """Dashboard root endpoint (redirige a /summary)."""
    return dashboard_summary(db, current_user)
