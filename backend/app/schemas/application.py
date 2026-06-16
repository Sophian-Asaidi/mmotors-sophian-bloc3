from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    vehicle_id: int = Field(gt=0)
    application_type: Literal["purchase", "rental"]
    message: str | None = Field(default=None, max_length=1000)


class DocumentRead(BaseModel):
    id: int
    filename: str
    content_type: str | None
    uploaded_at: datetime


class ApplicationRead(BaseModel):
    id: int
    vehicle_id: int
    vehicle_title: str
    application_type: str
    status: str
    message: str | None
    admin_comment: str | None
    user_email: str | None = None
    documents: list[DocumentRead] = []
    created_at: datetime
    updated_at: datetime


class ApplicationStatusUpdate(BaseModel):
    status: Literal["approved", "rejected"]
    admin_comment: str | None = Field(default=None, max_length=1000)

