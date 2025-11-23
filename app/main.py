from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.predictions import router as predictions_router
from app.api.routes.retino import router as retino_router
from app.api.routes.auth import router as auth_router
from app.api.routes.notifications import router as notifications_router
from app.api.routes.users import router as users_router
from app.api.routes.patients import router as patients_router
from app.api.routes.dashboard import router as dashboard_router

from app.services.database import Base, engine
from app.services import ml_service
from app.core.config import settings

app = FastAPI(title="DABETAI-AIAPI", version="1.0.0", docs_url="/docs", redoc_url="/redoc")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://127.0.0.1:8081", "http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok", "message": "DABETAI API is running"}

app.include_router(predictions_router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(retino_router, prefix="/retinopathy", tags=["Retinopathy"])  
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"]) 
app.include_router(notifications_router, prefix="/api/notifications", tags=["Notifications"]) 
app.include_router(users_router, prefix="/api", tags=["Users"]) 
app.include_router(patients_router, prefix="/api/patients", tags=["Patients"]) 
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"]) 

Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def startup_events():
    # Preload commonly used models to reduce latency on first request
    for name in ["retinopathy"]:
        try:
            ml_service.load_model(name)
        except Exception:
            # no-op: model may be missing during development
            pass

def get_db():
    from app.services.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
