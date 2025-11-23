from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.crud import crud_misc
from app.schemas.misc import NotificationOut

router = APIRouter()


@router.get('/', response_model=list[NotificationOut])
def list_notifications(tipo: str | None = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    items, total = crud_misc.list_notifications(db, current_user.id, tipo=tipo)
    return items


@router.post('/mark-all-as-read')
def mark_all(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    crud_misc.mark_all_notifications_read(db, current_user.id)
    return {"ok": True}


@router.get('/settings')
def get_notification_settings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    from app.models.models import ConfiguracionNotificaciones
    cfg = db.query(ConfiguracionNotificaciones).filter(ConfiguracionNotificaciones.doctor_id == current_user.id).first()
    if not cfg:
        return {}
    return cfg


@router.put('/settings')
def update_notification_settings(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    from app.models.models import ConfiguracionNotificaciones
    cfg = db.query(ConfiguracionNotificaciones).filter(ConfiguracionNotificaciones.doctor_id == current_user.id).first()
    if not cfg:
        cfg = ConfiguracionNotificaciones(doctor_id=current_user.id)
        db.add(cfg)
    for k, v in payload.items():
        if hasattr(cfg, k):
            setattr(cfg, k, v)
    db.add(cfg)
    db.commit()
    db.refresh(cfg)
    return cfg
