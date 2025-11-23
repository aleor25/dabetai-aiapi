from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_doctor
from app.schemas.doctor import DoctorOut, DoctorUpdate
from app.schemas.misc import SessionOut
from app.api.deps import get_db, get_current_user
from app.core.security import verify_password, get_password_hash

router = APIRouter()


@router.get('/users/me', response_model=DoctorOut)
def me(current_user=Depends(get_current_user)):
    return current_user


@router.put('/users/me', response_model=DoctorOut)
def update_me(data: DoctorUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # simple patch-style update
    user = crud_doctor.get_doctor(db, current_user.id)
    for k, v in data.dict(exclude_unset=True).items():
        setattr(user, k, v)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put('/users/me/password')
def change_password(old_password: str, new_password: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = crud_doctor.get_doctor(db, current_user.id)
    if not verify_password(old_password, user.contraseña_hasheada):
        raise HTTPException(status_code=400, detail='Old password incorrect')
    user.contraseña_hasheada = get_password_hash(new_password)
    db.add(user)
    db.commit()
    return {"ok": True}


@router.post('/users/forgot-password')
def forgot_password(email: str, db: Session = Depends(get_db)):
    # token generation and email sending omitted; placeholder
    user = crud_doctor.get_doctor_by_email(db, email)
    if not user:
        # don't reveal user existence
        return {"ok": True}
    # TODO: generate token, store and send email
    return {"ok": True}


@router.post('/users/reset-password')
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    # placeholder: validate token and reset
    return {"ok": True}


@router.get('/users/me/sessions', response_model=list[SessionOut])
def list_sessions(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    from app.crud.crud_misc import list_sessions
    sessions = list_sessions(db, current_user.id)
    return sessions


@router.delete('/users/me/sessions/{session_id}')
def delete_session(session_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    from app.crud.crud_misc import delete_session
    ok = delete_session(db, session_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail='Session not found')
    return {"ok": True}
