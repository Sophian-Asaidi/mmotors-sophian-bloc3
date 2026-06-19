from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.core.settings import settings

ALLOWED_CONTENT_TYPES = {"application/pdf", "image/png", "image/jpeg"}
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


def validate_upload(file: UploadFile) -> None:
    suffix = Path(file.filename or "").suffix.lower()
    if file.content_type not in ALLOWED_CONTENT_TYPES or suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format de fichier non autorisé",
        )


def store_upload(file: UploadFile, application_id: int) -> tuple[str, str]:
    validate_upload(file)
    folder = Path(settings.upload_dir) / f"application-{application_id}"
    folder.mkdir(parents=True, exist_ok=True)
    safe_name = f"{uuid4().hex}{Path(file.filename or '').suffix.lower()}"
    destination = folder / safe_name
    with destination.open("wb") as output:
        output.write(file.file.read())
    return file.filename or safe_name, str(destination)
