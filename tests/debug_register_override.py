import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.database import Base
import app.api.deps as app_deps
from fastapi.testclient import TestClient
from app.main import app

TEST_DB = 'test_debug.db'
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
engine = create_engine(f'sqlite:///{TEST_DB}', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app_deps.get_db = override_get_db

client = TestClient(app)
payload = {
    "nombre": "Juan",
    "apellido_paterno": "Perez",
    "apellido_materno": "Lopez",
    "email": "juan-debug@example.com",
    "telefono": "123",
    "cedula_profesional": "ABC123",
    "institucion_salud": "Hospital",
    "especialidad": "Endocrinologia",
    "foto_perfil_url": None,
    "idioma": "es",
    "zona_horaria": "UTC",
    "contrasena": "secret123"
}

resp = client.post('/api/register', json=payload)
print('STATUS', resp.status_code)
print(resp.text)
