from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import Consultation, HealthUnit, Patient, User

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    patients_count = db.query(func.count(Patient.id)).scalar() or 0
    units_count = db.query(func.count(HealthUnit.id)).scalar() or 0
    consultations_count = db.query(func.count(Consultation.id)).scalar() or 0
    users_count = db.query(func.count(User.id)).scalar() or 0

    return {
        "pacientes": patients_count,
        "unidades": units_count,
        "consultas": consultations_count,
        "utilizadores": users_count,
        "status": "ok",
        "unidade_saude": "Uíge Provincial",
        "ultimo_acesso": "agora",
    }
