import pytest
from app.schemas.doctor import DoctorCreate


def test_smoke_docs(client):
    r = client.get('/docs')
    assert r.status_code == 200


def test_register_login_and_protected(client):
    payload = {
        "nombre": "Juan",
        "apellido_paterno": "Perez",
        "apellido_materno": "Lopez",
        "email": "juan@example.com",
        "telefono": "1234567890",
        "cedula_profesional": "ABC123",
        "institucion_salud": "Hospital",
        "especialidad": "Endocrinologia",
        "idioma": "es",
        "zona_horaria": "UTC",
        "contrasena": "secret123"
    }
    r = client.post('/api/auth/register', json=payload)
    assert r.status_code in [200, 201], f"Register failed: {r.text}"
    data = r.json()
    assert data['email'] == "juan@example.com"

    # login
    r2 = client.post('/api/auth/token', data={"username": "juan@example.com", "password": "secret123"})
    assert r2.status_code == 200, f"Login failed: {r2.text}"
    token = r2.json()['access_token']

    # access protected
    r3 = client.get('/api/users/me', headers={"Authorization": f"Bearer {token}"})
    assert r3.status_code == 200
    assert r3.json()['email'] == 'juan@example.com'


def test_register_duplicate_email(client):
    payload = {
        "nombre": "Marta",
        "apellido_paterno": "Gomez",
        "apellido_materno": "Lopez",
        "email": "marta@example.com",
        "telefono": "1234567890",
        "cedula_profesional": "CDE456",
        "institucion_salud": "Clinica",
        "especialidad": "General",
        "idioma": "es",
        "zona_horaria": "UTC",
        "contrasena": "secret123"
    }
    r = client.post('/api/auth/register', json=payload)
    assert r.status_code in [200, 201]
    r2 = client.post('/api/auth/register', json=payload)
    assert r2.status_code in [400, 409]


def test_protected_without_token(client):
    r = client.get('/api/users/me')
    assert r.status_code == 401


def test_patient_crud_and_not_found(client):
    # register and login
    payload = {
        "nombre": "Ana",
        "apellido_paterno": "Lopez",
        "apellido_materno": "Ruiz",
        "email": "ana@example.com",
        "telefono": "1234567890",
        "cedula_profesional": "ZZZ789",
        "institucion_salud": "Clinica",
        "especialidad": "General",
        "idioma": "es",
        "zona_horaria": "UTC",
        "contrasena": "secret123"
    }
    r = client.post('/api/auth/register', json=payload)
    assert r.status_code in [200, 201]
    
    r = client.post('/api/auth/token', data={"username": "ana@example.com", "password": "secret123"})
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json()['access_token']

    # create patient
    patient = {"nombre_completo": "Paciente Uno", "fecha_nacimiento": "1980-01-01", "sexo": "F", "curp": "CURP1"}
    r2 = client.post('/api/patients', json=patient, headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code in [200, 201], f"Create patient failed: {r2.text}"
    pid = r2.json()['id']

    # get patients list
    r3 = client.get('/api/patients', headers={"Authorization": f"Bearer {token}"})
    assert r3.status_code == 200

    # get existing
    r4 = client.get(f'/api/patients/{pid}', headers={"Authorization": f"Bearer {token}"})
    assert r4.status_code == 200

    # get non-existent
    r5 = client.get('/api/patients/99999', headers={"Authorization": f"Bearer {token}"})
    assert r5.status_code == 404


def test_dashboard_structure(client):
    # register and login
    payload = {
        "nombre": "Diego",
        "apellido_paterno": "Sanchez",
        "apellido_materno": "Ortiz",
        "email": "diego@example.com",
        "telefono": "1234567890",
        "cedula_profesional": "AAA111",
        "institucion_salud": "Hospital",
        "especialidad": "General",
        "idioma": "es",
        "zona_horaria": "UTC",
        "contrasena": "secret123"
    }
    r = client.post('/api/auth/register', json=payload)
    assert r.status_code in [200, 201]
    
    r = client.post('/api/auth/token', data={"username": "diego@example.com", "password": "secret123"})
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json()['access_token']
    r2 = client.get('/api/dashboard', headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    body = r2.json()
    assert isinstance(body, dict)
