"""CRUD operations for device tokens."""
from sqlalchemy.orm import Session
from app.models.models import DeviceToken


def get_device_by_token(db: Session, token: str):
    return db.query(DeviceToken).filter(DeviceToken.token == token).first()


def create_device_token(db: Session, user_id: int, token: str):
    existing = get_device_by_token(db, token)
    if existing:
        return existing
    device = DeviceToken(user_id=user_id, token=token)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def list_devices_for_user(db: Session, user_id: int):
    return db.query(DeviceToken).filter(DeviceToken.user_id == user_id).all()
