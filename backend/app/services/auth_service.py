from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import RegisterRequest, validate_exam_email
from app.security.password import hash_password, verify_password


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == validate_exam_email(email)).first()


def create_user(db: Session, payload: RegisterRequest, role: str = "user") -> User:
    email = validate_exam_email(payload.email)
    if get_user_by_email(db, email):
        raise ValueError("Email déjà utilisé")

    user = User(email=email, hashed_password=hash_password(payload.password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user

