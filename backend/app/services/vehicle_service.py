from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.vehicles import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleModeUpdate


class VehicleCatalogService:
    def __init__(self, db: Session):
        self.vehicles = VehicleRepository(db)

    def list_vehicles(self, mode: str | None = None):
        if mode and mode not in {"sale", "rent"}:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Mode invalide")
        return self.vehicles.list_available(mode)

    def get_vehicle(self, vehicle_id: int):
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Véhicule introuvable")
        return vehicle

    def create_vehicle(self, data: VehicleCreate):
        return self.vehicles.create(data)

    def change_mode(self, vehicle_id: int, data: VehicleModeUpdate):
        vehicle = self.get_vehicle(vehicle_id)
        return self.vehicles.update_mode(vehicle, data.mode, data.price, data.monthly_price)
