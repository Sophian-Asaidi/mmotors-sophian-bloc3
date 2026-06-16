from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class VehicleBase(BaseModel):
    brand: str = Field(min_length=2, max_length=80)
    model: str = Field(min_length=1, max_length=120)
    year: int = Field(ge=1990, le=2035)
    mileage: int = Field(ge=0, le=500000)
    price: float | None = Field(default=None, ge=0)
    monthly_price: float | None = Field(default=None, ge=0)
    energy: str = Field(min_length=2, max_length=60)
    transmission: str = Field(min_length=2, max_length=60)
    mode: Literal["sale", "rental"]
    status: Literal["available", "reserved", "sold"] = "available"

    @field_validator("brand", "model", "energy", "transmission")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return value.strip()


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    brand: str | None = Field(default=None, min_length=2, max_length=80)
    model: str | None = Field(default=None, min_length=1, max_length=120)
    year: int | None = Field(default=None, ge=1990, le=2035)
    mileage: int | None = Field(default=None, ge=0, le=500000)
    price: float | None = Field(default=None, ge=0)
    monthly_price: float | None = Field(default=None, ge=0)
    energy: str | None = Field(default=None, min_length=2, max_length=60)
    transmission: str | None = Field(default=None, min_length=2, max_length=60)
    mode: Literal["sale", "rental"] | None = None
    status: Literal["available", "reserved", "sold"] | None = None


class VehicleRead(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

