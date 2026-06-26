from sqlalchemy.orm import Session, joinedload

from app.domain.models import Application, Document


class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, vehicle_id: int, offer_type: str, message: str) -> Application:
        application = Application(
            user_id=user_id,
            vehicle_id=vehicle_id,
            offer_type=offer_type,
            message=message or "",
            status="pending",
        )
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def add_document(self, application_id: int, filename: str, content_type: str, stored_path: str) -> Document:
        document = Document(
            application_id=application_id,
            filename=filename,
            content_type=content_type,
            stored_path=stored_path,
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def list_for_user(self, user_id: int) -> list[Application]:
        return (
            self.db.query(Application)
            .options(joinedload(Application.vehicle), joinedload(Application.documents))
            .filter(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
            .all()
        )

    def list_all(self) -> list[Application]:
        return (
            self.db.query(Application)
            .options(joinedload(Application.user), joinedload(Application.vehicle), joinedload(Application.documents))
            .order_by(Application.created_at.desc())
            .all()
        )

    def get(self, application_id: int) -> Application | None:
        return (
            self.db.query(Application)
            .options(joinedload(Application.user), joinedload(Application.vehicle), joinedload(Application.documents))
            .filter(Application.id == application_id)
            .first()
        )

    def get_document(self, document_id: int) -> Document | None:
        return (
            self.db.query(Document)
            .options(joinedload(Document.application))
            .filter(Document.id == document_id)
            .first()
        )

    def update_status(self, application: Application, status: str, admin_comment: str) -> Application:
        application.status = status
        application.admin_comment = admin_comment or ""
        self.db.commit()
        self.db.refresh(application)
        return application
    
    def update_internal_comment(self, application: Application, internal_comment: str) -> Application:
        application.internal_comment = internal_comment or ""
        self.db.commit()
        self.db.refresh(application)
        return application
    
    def update_client_comment(self, application: Application, admin_comment: str) -> Application:
        application.admin_comment = admin_comment or ""
        self.db.commit()
        self.db.refresh(application)
        return application