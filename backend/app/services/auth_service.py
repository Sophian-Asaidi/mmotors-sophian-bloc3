from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.users import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.users = UserRepository(db)

    def register(self, email: str, password: str):
        if self.users.find_by_email(email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email déjà utilisé")
        return self.users.create(email=email, password_hash=hash_password(password), role="user")

    def login(self, email: str, password: str):
        user = self.users.find_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants incorrects")
        token = create_access_token(subject=user.email, role=user.role)
        return token, user
