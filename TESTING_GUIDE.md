# DABETAI-AIAPI - Guía de Pruebas y Setup

## Tabla de Contenidos
1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación](#instalación)
3. [Ejecutar Tests Automatizados](#ejecutar-tests-automatizados)
4. [Ejecutar el Servidor](#ejecutar-el-servidor)
5. [Probar Endpoints Manualmente](#probar-endpoints-manualmente)
6. [Troubleshooting](#troubleshooting)

---

## Requisitos del Sistema

- **Python**: 3.10 o superior
- **pip**: Gestor de paquetes de Python (incluido con Python)
- **Git**: (opcional, para clonar el repositorio)
- **Postman o curl**: (opcional, para pruebas manuales)

Verificar versiones:
```bash
python --version
pip --version
```

---

## Instalación

### 1. Clonar el Repositorio (si aún no lo has hecho)

```bash
git clone https://github.com/aleor25/dabetai-aiapi.git
cd dabetai-aiapi
```

### 2. Crear Virtual Environment (Recomendado)

**En Windows (cmd o PowerShell):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**En macOS/Linux (bash o zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Deberías ver `(.venv)` al inicio de tu terminal.

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Contenido de requirements.txt:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pytest==7.4.3
httpx==0.25.2
google-auth==2.25.2
pyfcm==1.4.7
```

Verificar instalación:
```bash
pip list
```

---

## Ejecutar Tests Automatizados

### Opción 1: Ejecutar todos los tests

```bash
python -m pytest tests/ -v
```

**Salida esperada:**
```
tests/test_api.py::test_smoke_docs PASSED                    [ 16%]
tests/test_api.py::test_register_login_and_protected PASSED  [ 33%]
tests/test_api.py::test_register_duplicate_email PASSED      [ 50%]
tests/test_api.py::test_protected_without_token PASSED       [ 66%]
tests/test_api.py::test_patient_crud_and_not_found PASSED    [ 83%]
tests/test_api.py::test_dashboard_structure PASSED           [100%]

======================== 6 passed in 0.37s ========================
```

### Opción 2: Ejecutar un test específico

```bash
# Solo test de autenticación
python -m pytest tests/test_api.py::test_register_login_and_protected -v

# Solo test de pacientes
python -m pytest tests/test_api.py::test_patient_crud_and_not_found -v

# Solo test de dashboard
python -m pytest tests/test_api.py::test_dashboard_structure -v
```

### Opción 3: Ejecutar con cobertura (si tienes coverage instalado)

```bash
pip install pytest-cov
python -m pytest tests/ --cov=app --cov-report=html
```

---

## Ejecutar el Servidor

### 1. Iniciar Uvicorn

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Salida esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
```

### 2. Acceder a la Documentación Interactiva

**Swagger UI (Recomendado):**
```
http://localhost:8000/docs
```

**ReDoc (Alternativa):**
```
http://localhost:8000/redoc
```

---

## Probar Endpoints Manualmente

### Opción A: Usando curl (Terminal)

#### 1. Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

**Respuesta esperada:**
```json
{"status":"ok","message":"DABETAI API is running"}
```

#### 2. Registrar un Doctor

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido_paterno": "Perez",
    "apellido_materno": "Garcia",
    "email": "juan@example.com",
    "telefono": "1234567890",
    "cedula_profesional": "ABC123",
    "institucion_salud": "Hospital Central",
    "especialidad": "Endocrinologia",
    "contrasena": "password123"
  }'
```

**Respuesta esperada (201 Created):**
```json
{
  "id": 1,
  "nombre": "Juan",
  "email": "juan@example.com",
  "created_at": "2025-11-23T10:30:00"
}
```

#### 3. Login (Obtener Token)

```bash
curl -X POST "http://localhost:8000/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=juan@example.com&password=password123"
```

**Respuesta esperada (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Guarda el `access_token` para los siguientes requests.**

#### 4. Obtener Perfil (Requiere Token)

```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer {access_token}"
```

Reemplaza `{access_token}` con el token obtenido en el paso anterior.

**Respuesta esperada (200 OK):**
```json
{
  "id": 1,
  "nombre": "Juan",
  "email": "juan@example.com",
  "telefono": "1234567890"
}
```

#### 5. Crear un Paciente (Requiere Token)

```bash
curl -X POST "http://localhost:8000/api/patients" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_completo": "Maria Rodriguez",
    "fecha_nacimiento": "1990-05-15",
    "sexo": "F",
    "curp": "RODM900515MDFXXX00",
    "telefono": "9876543210",
    "direccion": "Calle Principal 123"
  }'
```

**Respuesta esperada (201 Created):**
```json
{
  "id": 1,
  "nombre_completo": "Maria Rodriguez",
  "doctor_id": 1,
  "sexo": "F"
}
```

#### 6. Listar Pacientes (Paginado)

```bash
curl -X GET "http://localhost:8000/api/patients?skip=0&limit=10" \
  -H "Authorization: Bearer {access_token}"
```

**Respuesta esperada:**
```json
{
  "items": [
    {
      "id": 1,
      "nombre_completo": "Maria Rodriguez",
      "doctor_id": 1
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

#### 7. Dashboard Summary

```bash
curl -X GET "http://localhost:8000/api/dashboard/summary" \
  -H "Authorization: Bearer {access_token}"
```

**Respuesta esperada:**
```json
{
  "summary_cards": {
    "patients_total": 1,
    "alerts_critical": 0,
    "unread_notifications": 0
  },
  "patients_requiring_attention": [],
  "recent_activity": [],
  "charts": {
    "complication_distribution": {},
    "prediction_trend": []
  }
}
```

#### 8. Predictions Stats

```bash
curl -X GET "http://localhost:8000/api/predictions/stats" \
  -H "Authorization: Bearer {access_token}"
```

**Respuesta esperada:**
```json
{
  "by_complication": {},
  "by_risk_level": {},
  "total_predictions": 0
}
```

---

### Opción B: Usando Postman

1. **Descargar Postman** desde https://www.postman.com/downloads/
2. **Crear una nueva Colección** para DABETAI
3. **Crear requests** con los URLs anteriores

**Variables útiles en Postman:**
```
{{base_url}} = http://localhost:8000
{{token}} = (pega el access_token aquí)
```

---

### Opción C: Usando Thunder Client (Extensión VS Code)

1. Instalar extensión "Thunder Client" en VS Code
2. Crear requests con interfaz similar a Postman
3. Reutilizar el mismo flujo de curl

---

## Flujo Completo de Prueba (Sin código)

### Test Manual Step-by-Step:

1. **Iniciar servidor:** `python -m uvicorn app.main:app --reload`
2. **Ir a:** http://localhost:8000/docs
3. **Probar Health Check:**
   - Click en GET /health
   - Click "Try it out"
   - Click "Execute"
   - Verificar respuesta 200 OK

4. **Registrar Doctor:**
   - Scroll a POST /api/auth/register
   - Click "Try it out"
   - Llenar formulario con datos de ejemplo
   - Click "Execute"
   - Copiar el `id` de respuesta

5. **Hacer Login:**
   - Scroll a POST /api/auth/token
   - Click "Try it out"
   - Ingresar: username=email, password=contraseña
   - Click "Execute"
   - **Copiar el access_token completo**

6. **Autorizar en Swagger:**
   - Click botón Authorize (arriba a la derecha)
   - Pegar: Bearer {access_token}
   - Click "Authorize"

7. **Probar endpoints protegidos:**
   - GET /api/users/me → Debe retornar 200
   - POST /api/patients → Crear paciente
   - GET /api/patients → Ver lista paginada
   - GET /api/dashboard/summary → Ver dashboard

8. **Verificar errores de acceso:**
   - Hacer click en Logout en Authorize
   - Intentar GET /api/users/me → Debe retornar 401

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"

**Solución:**
```bash
# Asegúrate de estar en la carpeta raíz del proyecto
cd dabetai-aiapi
# Verifica que .venv esté activado
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

### Error: "Port 8000 is already in use"

**Solución:**
```bash
# Usar puerto diferente
python -m uvicorn app.main:app --reload --port 8001
```

### Error: "database is locked"

**Solución:**
```bash
# Eliminar la base de datos de desarrollo
rm dabetai.db
# O en Windows:
del dabetai.db
# Reiniciar el servidor
```

### Error: "No module named 'passlib'"

**Solución:**
```bash
pip install -r requirements.txt
# O instalar individualmente
pip install passlib[bcrypt] python-jose[cryptography]
```

### Tests fallan con "no such table"

**Solución:**
```bash
# Limpiar cache de pytest y reintentar
rm -rf .pytest_cache
python -m pytest tests/ -v
```

### Error de CORS

**Solución:** Si usas frontend en puerto diferente, editar `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://localhost:3000"],  # Agregar tu puerto
    ...
)
```

---

## Recursos Adicionales

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **Pydantic Docs**: https://docs.pydantic.dev
- **JWT Tokens**: https://python-jose.readthedocs.io

---

## Checklist de Validación

Marca cada punto después de verificar:

- [ ] Python 3.10+ instalado
- [ ] Virtual environment activado
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] Tests pasan: `pytest tests/ -v` (6/6 OK)
- [ ] Servidor inicia sin errores
- [ ] `/health` retorna 200 OK
- [ ] `/docs` carga Swagger UI
- [ ] Puedes registrar un doctor
- [ ] Puedes hacer login y obtener token
- [ ] Puedes acceder a endpoints protegidos
- [ ] Dashboard retorna datos correctos

---

## Resumen Rápido

```bash
# 1. Setup (Una sola vez)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 2. Ejecutar tests
python -m pytest tests/ -v

# 3. Iniciar servidor
python -m uvicorn app.main:app --reload

# 4. Abrir en navegador
# http://localhost:8000/docs
```
