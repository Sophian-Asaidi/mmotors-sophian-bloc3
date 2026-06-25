from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(80), nullable=False)
    model = Column(String(80), nullable=False)
    year = Column(Integer, nullable=False)
    mileage = Column(Integer, nullable=False)
    energy = Column(String(50), nullable=False)
    transmission = Column(String(50), nullable=False)
    mode = Column(String(20), nullable=False)  # sale or rent
    price = Column(Float, nullable=True)
    monthly_price = Column(Float, nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    applications = relationship("Application", back_populates="vehicle")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    offer_type = Column(String(20), nullable=False)
    message = Column(Text, default="", nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    admin_comment = Column(Text, default="", nullable=False)
    internal_comment = Column(Text, default="", nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user = relationship("User", back_populates="applications")
    vehicle = relationship("Vehicle", back_populates="applications")
    documents = relationship("Document", back_populates="application", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(120), nullable=False)
    stored_path = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    application = relationship("Application", back_populates="documents")
