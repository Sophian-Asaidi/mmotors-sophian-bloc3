from sqlalchemy import Column, DateTime, Float, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(80), nullable=False)
    model = Column(String(120), nullable=False)
    year = Column(Integer, nullable=False)
    mileage = Column(Integer, nullable=False)
    price = Column(Float, nullable=True)
    monthly_price = Column(Float, nullable=True)
    energy = Column(String(60), nullable=False)
    transmission = Column(String(60), nullable=False)
    mode = Column(String(20), nullable=False, default="sale")
    status = Column(String(30), nullable=False, default="available")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    applications = relationship("Application", back_populates="vehicle")

