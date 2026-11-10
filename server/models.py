from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class HealthUnit(Base):
    __tablename__ = "health_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    unit_type: Mapped[str] = mapped_column(String(80), nullable=False)
    municipality: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    patients: Mapped[list["Patient"]] = relationship(back_populates="health_unit")
    users: Mapped[list["User"]] = relationship(back_populates="health_unit")
    consultations: Mapped[list["Consultation"]] = relationship(back_populates="health_unit")


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_identifier: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    identity_card: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    nif: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    contact: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    health_unit_id: Mapped[Optional[int]] = mapped_column(ForeignKey("health_units.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    health_unit: Mapped[Optional[HealthUnit]] = relationship(back_populates="patients")
    consultations: Mapped[list["Consultation"]] = relationship(back_populates="patient")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    profile: Mapped[str] = mapped_column(String(50), nullable=False)
    health_unit_id: Mapped[Optional[int]] = mapped_column(ForeignKey("health_units.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    health_unit: Mapped[Optional[HealthUnit]] = relationship(back_populates="users")


class Consultation(Base):
    __tablename__ = "consultations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    professional_name: Mapped[str] = mapped_column(String(255), nullable=False)
    health_unit_id: Mapped[int] = mapped_column(ForeignKey("health_units.id"), nullable=False)
    consultation_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    diagnosis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    observations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    patient: Mapped[Patient] = relationship(back_populates="consultations")
    health_unit: Mapped[HealthUnit] = relationship(back_populates="consultations")


class DataShare(Base):
    __tablename__ = "data_shares"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_unit_id: Mapped[Optional[int]] = mapped_column(ForeignKey("health_units.id"), nullable=True)
    target_unit_id: Mapped[Optional[int]] = mapped_column(ForeignKey("health_units.id"), nullable=True)
    patient_id: Mapped[Optional[int]] = mapped_column(ForeignKey("patients.id"), nullable=True)
    shared_by: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    share_type: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    permission_level: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
