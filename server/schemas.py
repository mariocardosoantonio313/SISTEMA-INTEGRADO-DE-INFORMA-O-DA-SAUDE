from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class HealthUnitCreate(BaseModel):
    name: str = Field(..., min_length=2)
    unit_type: str = Field(..., min_length=2)
    municipality: str = Field(..., min_length=2)
    address: Optional[str] = None
    contact: Optional[str] = None
    status: str = "active"


class HealthUnitRead(BaseModel):
    id: int
    name: str
    unit_type: str
    municipality: str
    address: Optional[str] = None
    contact: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None


class PatientCreate(BaseModel):
    full_name: str = Field(..., min_length=2)
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    identity_card: Optional[str] = None
    nif: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    health_unit_id: Optional[int] = None


class PatientRead(BaseModel):
    id: int
    patient_identifier: str
    full_name: str
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    identity_card: Optional[str] = None
    nif: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    health_unit_id: Optional[int] = None
    created_at: Optional[datetime] = None


class ConsultationCreate(BaseModel):
    patient_id: int
    professional_name: str
    health_unit_id: int
    consultation_datetime: datetime
    diagnosis: Optional[str] = None
    observations: Optional[str] = None


class ConsultationRead(BaseModel):
    id: int
    patient_id: int
    patient_name: Optional[str] = None
    professional_name: str
    health_unit_id: int
    consultation_datetime: datetime
    diagnosis: Optional[str] = None
    observations: Optional[str] = None
    created_at: Optional[datetime] = None


class PatientHistoryResponse(BaseModel):
    patient: PatientRead
    consultations: list[ConsultationRead]


class UserCreate(BaseModel):
    full_name: str
    username: str
    password: str
    profile: str
    health_unit_id: Optional[int] = None
    status: str = "active"


class UserRead(BaseModel):
    id: int
    full_name: str
    username: str
    profile: str
    health_unit_id: Optional[int] = None
    status: str
    created_at: Optional[datetime] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    profile: str
