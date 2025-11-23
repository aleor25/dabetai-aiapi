
# dabetai AI API - API de inteligencia artificial para predicción de complicaciones diabéticas

API REST que expone los modelos de machine learning para la predicción de complicaciones diabéticas tipo 1 (retinopatía, nefropatía, neuropatía, pie diabético).

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python version">
  <img src="https://img.shields.io/badge/FastAPI-0.95-green?logo=fastapi" alt="FastAPI version">
  <img src="https://img.shields.io/badge/PyTorch-2.x-red?logo=pytorch" alt="PyTorch version">
  <img src="https://img.shields.io/badge/scikit-learn-1.3-blue?logo=scikitlearn" alt="scikit-learn version">
  <img src="https://img.shields.io/badge/Uvicorn-0.23-green?logo=uvicorn" alt="Uvicorn version">
</p>

---

## 🧠 ¿Qué es dabetai AI API?

**dabetai AI API** es la API que ofrece los servicios de inteligencia artificial para la plataforma dabetai, brindando predicciones de riesgo para complicaciones diabéticas tipo 1, basados en modelos de machine learning entrenados con datos clínicos y biomédicos.

---

## ✨ Funcionalidades

- ⚡ **Predicciones rápidas** mediante endpoints REST  
- 🤖 Modelos basados en **scikit-learn** y **PyTorch**  
- 🔒 Seguridad básica con autenticación (por implementar o configurar)  
- 🧪 Endpoints para pruebas y validación de modelos  
- 📊 Respuesta en JSON con métricas y probabilidades de riesgo  

---

## 🛠 Tecnologías

- **Python 3.11+**  
- **FastAPI** para API REST rápida y moderna  
- **scikit-learn** para modelos clásicos de machine learning  
- **PyTorch** para modelos deep learning  
- **Uvicorn** como servidor ASGI rápido y eficiente  

---

## ⚡ Instalación rápida

### Prerrequisitos

- **Python 3.11+**  
- **pip** (gestor de paquetes Python)  

### Pasos

1. **Clonar repositorio**

```bash
git clone https://github.com/aleor25/dabetai-aiapi.git
cd dabetai-aiapi
````

2. **Crear entorno virtual**

```bash
python -m venv env
```

3. **Activar entorno virtual**

* En Windows (PowerShell):

```powershell
.\env\Scripts\Activate.ps1
```

* En Windows (cmd):

```cmd
.\env\Scripts\activate.bat
```

* En Linux/macOS:

```bash
source env/bin/activate
```

4. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

5. **Ejecutar servidor (modo desarrollo)**

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

---

## 🏗 Ecosistema dabetai: nuestros repositorios

dabetai está compuesto por múltiples repositorios especializados:

| Repositorio                                                             | Propósito                   | Estado          |
| ----------------------------------------------------------------------- | --------------------------- | --------------- |
| **[dabetai-mobileapp](https://github.com/Fermin-Cardenas/dabetai-mobileapp)** | App para pacientes          | ✅ En desarrollo |
| **[dabetai-webapp](https://github.com/chrisdev-ts/dabetai-webapp)**     | App web para médicos        | ✅ En desarrollo |
| **[dabetai-aiapi](https://github.com/aleor25/dabetai-aiapi)**           | API de IA y predicciones    | ✅ En desarrollo |
| **[dabetai-aimodels](https://github.com/chrisdev-ts/dabetai-aimodels)** | Modelos de machine learning | ✅ En desarrollo |
| **[dabetai-landing](https://github.com/chrisdev-ts/dabetai-landing)**   | Página de aterrizaje        | ✅ En desarrollo |
| **[dabetai-api](https://github.com/chrisdev-ts/dabetai-api)**                                                         | API principal del backend   | ✅ En desarrollo |

---

## 🤝 Colaboración interna

Seguimos convenciones específicas para mantener consistencia - consulta [CONTRIBUTING.MD](CONTRIBUTING.MD).

---

## 🤝 Reconocimientos

Este proyecto fue desarrollado por el equipo de autores:

* Cardenas Cabal Fermín
* Ortiz Pérez Alejandro
* Serrano Puertos Jorge Christian

Con la asesoría y guía conceptual de:

* Guarneros Nolasco Luis Rolando
* Cruz Ramos Nancy Aracely

Y con el apoyo académico de la

* Universidad Tecnológica del Centro de Veracruz
