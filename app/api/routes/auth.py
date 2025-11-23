from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.doctor import DoctorCreate, DoctorOut
from app.core.security import verify_password, create_access_token
from app.crud.crud_doctor import get_doctor_by_email, create_doctor
from app.core.config import settings

router = APIRouter(tags=["auth"])


class TokenOut(dict):
    """Token response model"""
    pass


@router.post("/register", response_model=DoctorOut, status_code=201)
def register(doctor: DoctorCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo doctor."""
    existing = get_doctor_by_email(db, doctor.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado"
        )
    new_doctor = create_doctor(db, doctor)
    return new_doctor


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Obtener access token con credenciales."""
    doctor = get_doctor_by_email(db, form_data.username)
    if not doctor or not verify_password(form_data.password, doctor.contraseña_hasheada):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    token = create_access_token({"sub": str(doctor.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/google")
def google_login(token: dict = None, db: Session = Depends(get_db)):
    """
    Login con Google Sign-In.
    Espera: {"id_token": "..."}
    """
    if not token or "id_token" not in token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="id_token requerido"
        )
    
    if not settings.google_client_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google Client ID no configurado"
        )
    
    try:
        from google.auth.transport import requests
        from google.oauth2 import id_token
        
        # Verificar y decodificar el id_token
        idinfo = id_token.verify_oauth2_token(
            token["id_token"],
            requests.Request(),
            settings.google_client_id
        )
        
        # Extraer información del usuario
        email = idinfo.get("email")
        nombre = idinfo.get("given_name", "")
        apellido = idinfo.get("family_name", "")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email no encontrado en el token de Google"
            )
        
        # Buscar o crear el doctor
        doctor = get_doctor_by_email(db, email)
        if not doctor:
            # Crear nuevo doctor con información de Google
            doctor_in = DoctorCreate(
                email=email,
                nombre=nombre,
                apellido_paterno=apellido,
                apellido_materno="",
                contrasena="google-oauth-placeholder"  # No se usará para login tradicional
            )
            doctor = create_doctor(db, doctor_in)
        
        # Generar JWT token
        jwt_token = create_access_token({"sub": str(doctor.id)})
        return {"access_token": jwt_token, "token_type": "bearer"}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verificando token: {str(e)}"
        )


@router.post("/password-recovery/{email}")
def password_recovery(email: str, db: Session = Depends(get_db)):
    """
    Solicitar recuperación de contraseña.
    En producción, enviaría un email con un token de reseteo.
    """
    doctor = get_doctor_by_email(db, email)
    if not doctor:
        # No revelar si el email existe o no (seguridad)
        return {
            "message": "Si el email está registrado, recibirás instrucciones de recuperación"
        }
    
    # TODO: En producción:
    # 1. Generar token de reseteo con expiración
    # 2. Guardar token en BD (ej. en tabla PasswordResetToken)
    # 3. Enviar email con link: /reset-password?token=...
    
    return {
        "message": "Si el email está registrado, recibirás instrucciones de recuperación"
    }


@router.post("/reset-password")
def reset_password(
    email: str,
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """
    Resetear contraseña usando token de recuperación.
    """
    doctor = get_doctor_by_email(db, email)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # TODO: En producción:
    # 1. Verificar que el token sea válido y no haya expirado
    # 2. Validar token contra BD
    # 3. Actualizar contraseña
    
    from app.core.security import get_password_hash
    doctor.contraseña_hasheada = get_password_hash(new_password)
    db.commit()
    db.refresh(doctor)
    
    return {
        "message": "Contraseña actualizada exitosamente"
    }
