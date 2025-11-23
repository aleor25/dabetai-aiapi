"""Routes package for app.api."""

from .predictions import router as predictions_router
from .retino import router as retino_router
from .auth import router as auth_router

__all__ = ["predictions_router", "retino_router", "auth_router"]
