from __future__ import annotations

from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .config import APP_ENV, APP_NAME, SERVER_HOST, SERVER_PORT
from .database import Base, SessionLocal, engine, get_db
from .models import Consultation, Patient, User
from .routers.auth import router as auth_router
from .routers.dashboard import router as dashboard_router
from .routers.health_units import router as health_units_router
from .routers.patients import router as patients_router
from .security import hash_password

Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def ensure_default_users():
    db: Session = SessionLocal()
    try:
        default_users = [
            {
                "username": "admin",
                "password": "Admin@2026",
                "full_name": "Administrador do Sistema",
                "profile": "Administrador",
            },
            {
                "username": "mario",
                "password": "mario123@",
                "full_name": "Mário da Silva",
                "profile": "Operador",
            },
        ]

        for user_data in default_users:
            if not db.query(User).filter(User.username == user_data["username"]).first():
                db.add(
                    User(
                        full_name=user_data["full_name"],
                        username=user_data["username"],
                        password_hash=hash_password(user_data["password"]),
                        profile=user_data["profile"],
                        status="active",
                    )
                )
        db.commit()
    finally:
        db.close()


ensure_default_users()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    ensure_default_users()


@app.get("/health")
def health_check():
    return {"status": "ok", "app": APP_NAME, "environment": APP_ENV}


@app.get("/api/patients/{patient_id}/history")
def get_patient_history(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    consultations = (
        db.query(Consultation)
        .filter(Consultation.patient_id == patient_id)
        .order_by(Consultation.consultation_datetime.desc())
        .all()
    )
    return {"patient": patient, "consultations": consultations}


@app.get("/api/consultations")
def list_consultations(db: Session = Depends(get_db), patient_id: int | None = None):
    items = db.query(Consultation)
    if patient_id is not None:
        items = items.filter(Consultation.patient_id == patient_id)
    return items.order_by(Consultation.consultation_datetime.desc()).all()


@app.get("/api/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.asc()).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "profile": user.profile,
            "status": user.status,
        }
        for user in users
    ]


@app.post("/api/users", status_code=201)
def create_user(payload: dict, db: Session = Depends(get_db)):
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username e password são obrigatórios.")

    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Este utilizador já existe.")

    user = User(
        full_name=payload.get("full_name") or username,
        username=username,
        password_hash=hash_password(password),
        profile=payload.get("profile") or "Operador",
        status=payload.get("status") or "active",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "profile": user.profile,
        "status": user.status,
    }


@app.post("/api/consultations", status_code=201)
def create_consultation(payload: dict, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == payload["patient_id"]).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    consultation_datetime = payload["consultation_datetime"]
    if isinstance(consultation_datetime, str):
        consultation_datetime = datetime.fromisoformat(consultation_datetime)

    consultation = Consultation(
        patient_id=payload["patient_id"],
        professional_name=payload["professional_name"],
        health_unit_id=payload["health_unit_id"],
        consultation_datetime=consultation_datetime,
        diagnosis=payload.get("diagnosis"),
        observations=payload.get("observations"),
    )
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    return consultation


@app.get("/api/consultations/{consultation_id}")
def get_consultation(consultation_id: int, db: Session = Depends(get_db)):
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    return consultation


app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(health_units_router)
app.include_router(patients_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server.main:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
