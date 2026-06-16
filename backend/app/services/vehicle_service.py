from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate


MODE_ALIASES = {
    "achat": "sale",
    "purchase": "sale",
    "sale": "sale",
    "vente": "sale",
    "location": "rental",
    "rental": "rental",
}


def normalize_mode(mode: str | None) -> str | None:
    if mode is None:
        return None
    return MODE_ALIASES.get(mode.lower())


def list_vehicles(db: Session, mode: str | None = None, search: str | None = None) -> list[Vehicle]:
    query = db.query(Vehicle)
    normalized_mode = normalize_mode(mode)
    if normalized_mode:
        query = query.filter(Vehicle.mode == normalized_mode)
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(or_(Vehicle.brand.ilike(term), Vehicle.model.ilike(term), Vehicle.energy.ilike(term)))
    return query.order_by(Vehicle.created_at.desc(), Vehicle.id.desc()).all()


def get_vehicle(db: Session, vehicle_id: int) -> Vehicle | None:
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def create_vehicle(db: Session, payload: VehicleCreate) -> Vehicle:
    vehicle = Vehicle(**payload.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def switch_vehicle_mode(db: Session, vehicle: Vehicle) -> Vehicle:
    vehicle.mode = "rental" if vehicle.mode == "sale" else "sale"
    db.commit()
    db.refresh(vehicle)
    return vehicle

