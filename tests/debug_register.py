from fastapi.testclient import TestClient
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

r = client.post('/api/register', json=payload)
print('STATUS', r.status_code)
print('BODY', r.text)
