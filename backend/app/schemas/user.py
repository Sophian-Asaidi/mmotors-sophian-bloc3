from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def validate_exam_email(value: str) -> str:
    email = value.strip().lower()
    if "@" not in email or " " in email or len(email) < 5:
        raise ValueError("Email invalide")
    return email


class RegisterRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def email_format(cls, value: str) -> str:
        return validate_exam_email(value)


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def email_format(cls, value: str) -> str:
        return validate_exam_email(value)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

