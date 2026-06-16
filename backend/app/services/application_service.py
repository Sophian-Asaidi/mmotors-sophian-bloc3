from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.document import Document
from app.models.user import User
from app.models.vehicle import Vehicle


def create_application(
    db: Session,
    user: User,
    vehicle: Vehicle,
    application_type: str,
    message: str | None = None,
) -> Application:
    application = Application(
        user_id=user.id,
        vehicle_id=vehicle.id,
        application_type=application_type,
        status="pending",
        message=message,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def add_document(
    db: Session,
    application: Application,
    filename: str,
    stored_path: str,
    content_type: str | None,
) -> Document:
    document = Document(
        application_id=application.id,
        filename=filename,
        stored_path=stored_path,
        content_type=content_type,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def list_user_applications(db: Session, user: User) -> list[Application]:
    return (
        db.query(Application)
        .filter(Application.user_id == user.id)
        .order_by(Application.created_at.desc(), Application.id.desc())
        .all()
    )


def list_all_applications(db: Session) -> list[Application]:
    return db.query(Application).order_by(Application.created_at.desc(), Application.id.desc()).all()


def update_application_status(
    db: Session,
    application: Application,
    status: str,
    admin_comment: str | None,
) -> Application:
    application.status = status
    application.admin_comment = admin_comment
    db.commit()
    db.refresh(application)
    return application

