from pydantic import BaseModel, Field

from app.schemas.auth import UserOut
from app.schemas.vehicle import VehicleOut


class ApplicationStatusUpdate(BaseModel):
    status: str = Field(pattern="^(approved|rejected)$")
    admin_comment: str = Field(default="", max_length=1000)


class DocumentOut(BaseModel):
    id: int
    filename: str
    content_type: str


class ApplicationOut(BaseModel):
    id: int
    offer_type: str
    message: str
    status: str
    admin_comment: str
    vehicle: VehicleOut
    documents: list[DocumentOut]


class AdminApplicationOut(ApplicationOut):
    user: UserOut


class ApplicationInternalCommentUpdate(BaseModel):
    internal_comment: str = Field(default="", max_length=1000)