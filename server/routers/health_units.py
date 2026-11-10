from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import HealthUnit
from server.schemas import HealthUnitCreate, HealthUnitRead

router = APIRouter(prefix="/api/health-units", tags=["health-units"])


@router.get("", response_model=list[HealthUnitRead])
def list_units(db: Session = Depends(get_db)):
    return db.query(HealthUnit).all()


@router.post("", response_model=HealthUnitRead, status_code=status.HTTP_201_CREATED)
def create_unit(payload: HealthUnitCreate, db: Session = Depends(get_db)):
    unit = HealthUnit(**payload.model_dump())
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


@router.get("/{unit_id}", response_model=HealthUnitRead)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(HealthUnit).filter(HealthUnit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unidade não encontrada.")
    return unit


@router.put("/{unit_id}", response_model=HealthUnitRead)
def update_unit(unit_id: int, payload: HealthUnitCreate, db: Session = Depends(get_db)):
    unit = db.query(HealthUnit).filter(HealthUnit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unidade não encontrada.")

    for field, value in payload.model_dump().items():
        setattr(unit, field, value)

    db.commit()
    db.refresh(unit)
    return unit


@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(HealthUnit).filter(HealthUnit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unidade não encontrada.")

    unit.status = "inactive"
    db.commit()
    return None
