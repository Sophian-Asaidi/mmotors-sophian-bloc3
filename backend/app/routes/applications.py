import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.application import Application
from app.models.user import User
from app.schemas.application import ApplicationRead, DocumentRead
from app.security.dependencies import get_current_user
from app.services.application_service import add_document, create_application, list_user_applications
from app.services.vehicle_service import get_vehicle


router = APIRouter(prefix="/applications", tags=["dossiers"])
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


def serialize_application(application: Application) -> ApplicationRead:
    vehicle = application.vehicle
    return ApplicationRead(
        id=application.id,
        vehicle_id=application.vehicle_id,
        vehicle_title=f"{vehicle.brand} {vehicle.model}" if vehicle else "Véhicule",
        application_type=application.application_type,
        status=application.status,
        message=application.message,
        admin_comment=application.admin_comment,
        user_email=application.user.email if application.user else None,
        documents=[
            DocumentRead(
                id=document.id,
                filename=document.filename,
                content_type=document.content_type,
                uploaded_at=document.uploaded_at,
            )
            for document in application.documents
        ],
        created_at=application.created_at,
        updated_at=application.updated_at,
    )


def _store_file(application: Application, uploaded_file: UploadFile, db: Session) -> None:
    original_name = Path(uploaded_file.filename or "document.pdf").name
    extension = Path(original_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Format de document non autorisé")

    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{application.id}_{uuid4().hex}{extension}"
    stored_path = settings.upload_dir / stored_name
    with stored_path.open("wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    add_document(
        db=db,
        application=application,
        filename=original_name,
        stored_path=str(stored_path),
        content_type=uploaded_file.content_type,
    )


@router.post("", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def submit_application(
    vehicle_id: int = Form(...),
    application_type: str = Form(...),
    message: str | None = Form(default=None),
    documents: list[UploadFile] | None = File(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApplicationRead:
    if application_type not in {"purchase", "rental"}:
        raise HTTPException(status_code=422, detail="Type de dossier invalide")

    vehicle = get_vehicle(db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")

    expected_mode = "sale" if application_type == "purchase" else "rental"
    if vehicle.mode != expected_mode:
        raise HTTPException(status_code=400, detail="Le type de dossier ne correspond pas au véhicule")

    application = create_application(db, current_user, vehicle, application_type, message)
    for uploaded_file in documents or []:
        _store_file(application, uploaded_file, db)

    db.refresh(application)
    return serialize_application(application)


@router.get("/me", response_model=list[ApplicationRead])
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ApplicationRead]:
    return [serialize_application(item) for item in list_user_applications(db, current_user)]


@router.get("/{application_id}", response_model=ApplicationRead)
def application_detail(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApplicationRead:
    application = db.query(Application).filter(Application.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Dossier introuvable")
    if application.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    return serialize_application(application)

