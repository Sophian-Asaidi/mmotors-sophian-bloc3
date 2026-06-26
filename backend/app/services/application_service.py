from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.domain.models import User
from app.repositories.applications import ApplicationRepository
from app.repositories.vehicles import VehicleRepository
from app.schemas.application import ApplicationStatusUpdate
from app.utils.files import store_upload


def serialize_vehicle(vehicle):
    return {
        "id": vehicle.id,
        "brand": vehicle.brand,
        "model": vehicle.model,
        "year": vehicle.year,
        "mileage": vehicle.mileage,
        "energy": vehicle.energy,
        "transmission": vehicle.transmission,
        "mode": vehicle.mode,
        "price": vehicle.price,
        "monthly_price": vehicle.monthly_price,
        "is_available": vehicle.is_available,
    }


def serialize_document(document):
    return {
        "id": document.id,
        "filename": document.filename,
        "content_type": document.content_type,
    }


def serialize_application(application, include_user: bool = False):
    data = {
        "id": application.id,
        "offer_type": application.offer_type,
        "message": application.message,
        "status": application.status,
        "admin_comment": application.admin_comment,
        "vehicle": serialize_vehicle(application.vehicle),
        "documents": [serialize_document(doc) for doc in application.documents],
    }

    if include_user:
        data["user"] = {
            "id": application.user.id,
            "email": application.user.email,
            "role": application.user.role,
        }
        data["internal_comment"] = application.internal_comment

    return data


class ApplicationWorkflowService:
    def __init__(self, db: Session):
        self.db = db
        self.applications = ApplicationRepository(db)
        self.vehicles = VehicleRepository(db)

    def submit(self, user: User, vehicle_id: int, offer_type: str, message: str, documents: list[UploadFile]):
        vehicle = self.vehicles.get(vehicle_id)

        if not vehicle or not vehicle.is_available:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Véhicule introuvable")

        if offer_type not in {"sale", "rent"}:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Type de dossier invalide")

        if offer_type != vehicle.mode:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le type de dossier ne correspond pas au véhicule",
            )

        application = self.applications.create(user.id, vehicle.id, offer_type, message)

        for document in documents or []:
            original_name, stored_path = store_upload(document, application.id)
            self.applications.add_document(
                application.id,
                original_name,
                document.content_type or "application/octet-stream",
                stored_path,
            )

        return self.applications.get(application.id)

    def list_for_user(self, user: User):
        return [serialize_application(app) for app in self.applications.list_for_user(user.id)]

    def list_all_for_admin(self):
        return [serialize_application(app, include_user=True) for app in self.applications.list_all()]

    def get_for_admin(self, application_id: int):
        application = self.applications.get(application_id)

        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dossier introuvable")

        return serialize_application(application, include_user=True)

    def get_document_for_admin(self, document_id: int):
        document = self.applications.get_document(document_id)

        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document introuvable")

        return document

    def decide(self, application_id: int, data: ApplicationStatusUpdate):
        application = self.applications.get(application_id)

        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dossier introuvable")

        updated = self.applications.update_status(application, data.status, data.admin_comment)

        return serialize_application(updated, include_user=True)
    
    def update_internal_comment(self, application_id: int, internal_comment: str):
        application = self.applications.get(application_id)

        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dossier introuvable")

        updated = self.applications.update_internal_comment(application, internal_comment)

        return serialize_application(updated, include_user=True)
    
    def update_client_comment(self, application_id: int, admin_comment: str):
        application = self.applications.get(application_id)

        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dossier introuvable")

        updated = self.applications.update_client_comment(application, admin_comment)

        return serialize_application(updated, include_user=True)


    def add_documents_for_user(self, user: User, application_id: int, documents: list[UploadFile]):
        application = self.applications.get(application_id)

        if not application or application.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dossier introuvable")

        if application.status != "pending":
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible d’ajouter des documents à un dossier déjà traité",
        )

        if not documents:
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Aucun document envoyé",
        )

        for document in documents:
            original_name, stored_path = store_upload(document, application.id)
            self.applications.add_document(
                application.id,
                original_name,
                document.content_type or "application/octet-stream",
                stored_path,
        )

        return serialize_application(self.applications.get(application.id))