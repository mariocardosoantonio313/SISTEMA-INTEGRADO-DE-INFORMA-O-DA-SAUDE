from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import Consultation, Patient
from server.schemas import PatientCreate, PatientHistoryResponse, PatientRead

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("", response_model=list[PatientRead])
def list_patients(db: Session = Depends(get_db), query: str | None = Query(default=None)):
    items = db.query(Patient)
    if query:
        items = items.filter(Patient.full_name.ilike(f"%{query}%"))
    return items.order_by(Patient.id.desc()).all()


@router.post("", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    if payload.full_name:
        existing = db.query(Patient).filter(Patient.full_name.ilike(payload.full_name)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Paciente já registado com este nome.")

    patient_identifier = f"PAT-{db.query(Patient).count()+1:06d}"
    patient = Patient(
        patient_identifier=patient_identifier,
        full_name=payload.full_name,
        birth_date=payload.birth_date,
        gender=payload.gender,
        identity_card=payload.identity_card,
        nif=payload.nif,
        contact=payload.contact,
        address=payload.address,
        health_unit_id=payload.health_unit_id,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    return patient


@router.get("/{patient_id}/history", response_model=PatientHistoryResponse)
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


@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(patient_id: int, payload: PatientCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    for field, value in payload.model_dump().items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient
