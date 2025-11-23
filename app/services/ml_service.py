import os
import joblib
from typing import Any, Dict
from app.core.config import settings

_MODELS: Dict[str, Any] = {}


def model_path(name: str) -> str:
    return os.path.join(settings.ml_models_dir, f"{name}_model.joblib")


def load_model(name: str):
    path = model_path(name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    _MODELS[name] = joblib.load(path)
    return _MODELS[name]


def get_model(name: str):
    return _MODELS.get(name)


def predict(name: str, X):
    model = get_model(name)
    if model is None:
        model = load_model(name)
    return model.predict_proba(X)
