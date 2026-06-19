from pydantic import BaseModel, Field, model_validator


class VehicleCreate(BaseModel):
    brand: str = Field(min_length=1, max_length=80)
    model: str = Field(min_length=1, max_length=80)
    year: int = Field(ge=1990, le=2100)
    mileage: int = Field(ge=0)
    energy: str = Field(min_length=1, max_length=50)
    transmission: str = Field(min_length=1, max_length=50)
    mode: str = Field(pattern="^(sale|rent)$")
    price: float | None = Field(default=None, ge=0)
    monthly_price: float | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def check_price_by_mode(self):
        if self.mode == "sale" and self.price is None:
            raise ValueError("Un véhicule en vente doit avoir un prix")
        if self.mode == "rent" and self.monthly_price is None:
            raise ValueError("Un véhicule en location doit avoir une mensualité")
        return self


class VehicleModeUpdate(BaseModel):
    mode: str = Field(pattern="^(sale|rent)$")
    price: float | None = Field(default=None, ge=0)
    monthly_price: float | None = Field(default=None, ge=0)


class VehicleOut(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    mileage: int
    energy: str
    transmission: str
    mode: str
    price: float | None
    monthly_price: float | None
    is_available: bool
