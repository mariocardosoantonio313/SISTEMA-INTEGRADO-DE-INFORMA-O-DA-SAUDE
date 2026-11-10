from .auth import router as auth_router
from .consultations import router as consultations_router
from .dashboard import router as dashboard_router
from .health_units import router as health_units_router
from .patients import router as patients_router

__all__ = [
    "auth_router",
    "consultations_router",
    "dashboard_router",
    "health_units_router",
    "patients_router",
]
