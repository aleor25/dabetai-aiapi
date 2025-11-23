from fastapi.testclient import TestClient
import sys
sys.path.insert(0, r'C:\Users\AleMa\Documents\Ale - UTCV\IDGS\9noCuatrimestre\dabetai-aiapi')
from app.main import app

client = TestClient(app)
payload = {
    "nombre": "Juan",
    "apellido_paterno": "Perez",
    "apellido_materno": "Lopez",
    "email": "juan@example.com",
    "telefono": "123",
    "cedula_profesional": "ABC123",
    "institucion_salud": "Hospital",
    "especialidad": "Endocrinologia",
    "foto_perfil_url": None,
    "idioma": "es",
    "zona_horaria": "UTC",
    "contraseña": "secret123"
}

resp = client.post('/api/register', json=payload)
print('STATUS', resp.status_code)
try:
    print('JSON:', resp.json())
except Exception:
    print('TEXT:', resp.text)
