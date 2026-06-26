from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.domain.models import User
from app.services.application_service import ApplicationWorkflowService, serialize_application

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_application(
    vehicle_id: int = Form(...),
    offer_type: str = Form(...),
    message: str = Form(""),
    documents: list[UploadFile] = File(default=[]),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    application = ApplicationWorkflowService(db).submit(current_user, vehicle_id, offer_type, message, documents)
    return serialize_application(application)


@router.get("/me")
def my_applications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ApplicationWorkflowService(db).list_for_user(current_user)


@router.post("/{application_id}/documents")
def add_documents_to_application(
    application_id: int,
    documents: list[UploadFile] = File(default=[]),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ApplicationWorkflowService(db).add_documents_for_user(
        user,
        application_id,
        documents,
    )