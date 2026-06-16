from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.user import User
from app.models.vehicle import Vehicle
from app.security.password import hash_password
from app.services.auth_service import get_user_by_email


ADMIN_EMAIL = "adminlocal@motors"
ADMIN_PASSWORD = "AdminMot1!"
USER_EMAIL = "userlocal@motors"
USER_PASSWORD = "UserMot1!"


def _create_user_if_missing(db: Session, email: str, password: str, role: str) -> User:
    user = get_user_by_email(db, email)
    if user:
        return user
    user = User(email=email, hashed_password=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _seed_vehicles(db: Session) -> None:
    if db.query(Vehicle).count() > 0:
        return

    vehicles = [
        Vehicle(
            brand="Peugeot",
            model="208 PureTech",
            year=2021,
            mileage=38500,
            price=13990,
            monthly_price=None,
            energy="Essence",
            transmission="Manuelle",
            mode="sale",
        ),
        Vehicle(
            brand="Renault",
            model="Clio E-Tech",
            year=2022,
            mileage=24500,
            price=None,
            monthly_price=289,
            energy="Hybride",
            transmission="Automatique",
            mode="rental",
        ),
        Vehicle(
            brand="Tesla",
            model="Model 3",
            year=2020,
            mileage=61200,
            price=27900,
            monthly_price=None,
            energy="Electrique",
            transmission="Automatique",
            mode="sale",
        ),
        Vehicle(
            brand="Citroen",
            model="C3 Aircross",
            year=2023,
            mileage=15300,
            price=None,
            monthly_price=319,
            energy="Diesel",
            transmission="Manuelle",
            mode="rental",
        ),
    ]
    db.add_all(vehicles)
    db.commit()


def _seed_application(db: Session, user: User) -> None:
    if db.query(Application).count() > 0:
        return
    vehicle = db.query(Vehicle).filter(Vehicle.mode == "rental").first()
    if vehicle is None:
        return
    db.add(
        Application(
            user_id=user.id,
            vehicle_id=vehicle.id,
            application_type="rental",
            status="pending",
            message="Dossier de démonstration créé automatiquement.",
        )
    )
    db.commit()


def seed_database(db: Session) -> None:
    admin = _create_user_if_missing(db, ADMIN_EMAIL, ADMIN_PASSWORD, "admin")
    user = _create_user_if_missing(db, USER_EMAIL, USER_PASSWORD, "user")
    _seed_vehicles(db)
    _seed_application(db, user)
    _ = admin

