from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import Consultation, Patient
from server.schemas import ConsultationCreate, ConsultationRead

router = APIRouter(prefix="/api/consultations", tags=["consultations"])


def serialize_consultation(consultation: Consultation):
    patient = consultation.patient
    return {
        "id": consultation.id,
        "patient_id": consultation.patient_id,
        "patient_name": patient.full_name if patient else None,
        "professional_name": consultation.professional_name,
        "health_unit_id": consultation.health_unit_id,
        "consultation_datetime": consultation.consultation_datetime,
        "diagnosis": consultation.diagnosis,
        "observations": consultation.observations,
        "created_at": consultation.created_at,
    }


@router.get("", response_model=list[ConsultationRead])
def list_consultations(
    db: Session = Depends(get_db),
    patient_id: int | None = Query(default=None),
):
    items = db.query(Consultation)
    if patient_id is not None:
        items = items.filter(Consultation.patient_id == patient_id)
    rows = items.order_by(Consultation.consultation_datetime.desc()).all()
    return [serialize_consultation(item) for item in rows]


@router.post("", response_model=ConsultationRead, status_code=status.HTTP_201_CREATED)
def create_consultation(payload: ConsultationCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    consultation = Consultation(
        patient_id=payload.patient_id,
        professional_name=payload.professional_name,
        health_unit_id=payload.health_unit_id,
        consultation_datetime=payload.consultation_datetime,
        diagnosis=payload.diagnosis,
        observations=payload.observations,
    )
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    return serialize_consultation(consultation)


@router.get("/{consultation_id}", response_model=ConsultationRead)
def get_consultation(consultation_id: int, db: Session = Depends(get_db)):
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    return serialize_consultation(consultation)
