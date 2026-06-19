from sqlalchemy.orm import Session

from app.domain.models import Vehicle
from app.schemas.vehicle import VehicleCreate


class VehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_available(self, mode: str | None = None) -> list[Vehicle]:
        query = self.db.query(Vehicle).filter(Vehicle.is_available.is_(True))
        if mode:
            query = query.filter(Vehicle.mode == mode)
        return query.order_by(Vehicle.created_at.desc()).all()

    def get(self, vehicle_id: int) -> Vehicle | None:
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def create(self, data: VehicleCreate) -> Vehicle:
        vehicle = Vehicle(**data.model_dump())
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def update_mode(self, vehicle: Vehicle, mode: str, price: float | None, monthly_price: float | None) -> Vehicle:
        vehicle.mode = mode
        if mode == "sale":
            vehicle.price = price if price is not None else vehicle.price or 0
            vehicle.monthly_price = None
        else:
            vehicle.monthly_price = monthly_price if monthly_price is not None else vehicle.monthly_price or 0
            vehicle.price = None
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle
