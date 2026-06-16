from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.vehicle import VehicleRead
from app.services.vehicle_service import get_vehicle, list_vehicles


router = APIRouter(prefix="/vehicles", tags=["véhicules"])


@router.get("", response_model=list[VehicleRead])
def vehicles(
    mode: str | None = Query(default=None),
    search: str | None = Query(default=None, max_length=80),
    db: Session = Depends(get_db),
) -> list[VehicleRead]:
    return list_vehicles(db, mode=mode, search=search)


@router.get("/{vehicle_id}", response_model=VehicleRead)
def vehicle_detail(vehicle_id: int, db: Session = Depends(get_db)) -> VehicleRead:
    vehicle = get_vehicle(db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")
    return vehicle

