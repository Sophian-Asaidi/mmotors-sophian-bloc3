from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_admin
from app.domain.models import User
from app.schemas.application import ApplicationStatusUpdate
from app.schemas.vehicle import VehicleCreate, VehicleModeUpdate, VehicleOut
from app.services.application_service import ApplicationWorkflowService
from app.services.vehicle_service import VehicleCatalogService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/applications")
def list_applications(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return ApplicationWorkflowService(db).list_all_for_admin()


@router.patch("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    payload: ApplicationStatusUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ApplicationWorkflowService(db).decide(application_id, payload)


@router.post("/vehicles", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
def create_vehicle(payload: VehicleCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return VehicleCatalogService(db).create_vehicle(payload)


@router.patch("/vehicles/{vehicle_id}/mode", response_model=VehicleOut)
def update_vehicle_mode(
    vehicle_id: int,
    payload: VehicleModeUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return VehicleCatalogService(db).change_mode(vehicle_id, payload)
