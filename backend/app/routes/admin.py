from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.routes.applications import serialize_application
from app.schemas.application import ApplicationRead, ApplicationStatusUpdate
from app.schemas.vehicle import VehicleCreate, VehicleRead
from app.security.dependencies import get_current_admin
from app.services.application_service import list_all_applications, update_application_status
from app.services.vehicle_service import create_vehicle, get_vehicle, switch_vehicle_mode


router = APIRouter(prefix="/admin", tags=["administration"])


@router.post("/vehicles", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
def admin_create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
) -> VehicleRead:
    return create_vehicle(db, payload)


@router.patch("/vehicles/{vehicle_id}/switch", response_model=VehicleRead)
def admin_switch_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
) -> VehicleRead:
    vehicle = get_vehicle(db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")
    return switch_vehicle_mode(db, vehicle)


@router.get("/applications", response_model=list[ApplicationRead])
def admin_applications(
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
) -> list[ApplicationRead]:
    return [serialize_application(item) for item in list_all_applications(db)]


@router.patch("/applications/{application_id}/status", response_model=ApplicationRead)
def admin_update_application(
    application_id: int,
    payload: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
) -> ApplicationRead:
    application = db.query(Application).filter(Application.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Dossier introuvable")
    return serialize_application(
        update_application_status(db, application, payload.status, payload.admin_comment)
    )

