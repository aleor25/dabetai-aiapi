from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.crud import crud_device
from app.services.notifications import send_notification

router = APIRouter()


class DeviceRegisterIn(BaseModel):
    token: str


class SendTestIn(BaseModel):
    token: str
    title: str = "Test"
    body: str = "This is a test"


@router.post('/register')
def register_device(payload: DeviceRegisterIn, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    token = payload.token
    if not token:
        raise HTTPException(status_code=400, detail='token required')
    device = crud_device.create_device_token(db, current_user.id, token)
    return {"id": device.id, "token": device.token}


@router.post('/send_test')
def send_test_notification(payload: SendTestIn, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    token = payload.token
    title = payload.title
    body = payload.body
    if not token:
        raise HTTPException(status_code=400, detail='token required')
    result = send_notification(token, title, body, data_message={"from": "dabetai"})
    return {"result": result}
