from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vehicle import VehicleOut
from app.services.vehicle_service import VehicleCatalogService

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("", response_model=list[VehicleOut])
def list_vehicles(mode: str | None = None, db: Session = Depends(get_db)):
    return VehicleCatalogService(db).list_vehicles(mode)


@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    return VehicleCatalogService(db).get_vehicle(vehicle_id)
