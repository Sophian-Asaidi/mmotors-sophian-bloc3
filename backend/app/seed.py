from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.domain.models import Application, User, Vehicle

ADMIN_EMAIL = "admin.so@mmotors.fr"
ADMIN_PASSWORD = "AdminSo2026!"
USER_EMAIL = "client.so@mmotors.fr"
USER_PASSWORD = "ClientSo2026!"


def seed_database(db: Session) -> None:
    if not db.query(User).filter(User.email == ADMIN_EMAIL).first():
        db.add(User(email=ADMIN_EMAIL, password_hash=hash_password(ADMIN_PASSWORD), role="admin"))
    if not db.query(User).filter(User.email == USER_EMAIL).first():
        db.add(User(email=USER_EMAIL, password_hash=hash_password(USER_PASSWORD), role="user"))
    db.commit()

    if db.query(Vehicle).count() == 0:
        db.add_all([
            Vehicle(brand="Peugeot", model="308", year=2021, mileage=42000, energy="Essence", transmission="Manuelle", mode="sale", price=16490),
            Vehicle(brand="Renault", model="Clio", year=2022, mileage=18000, energy="Hybride", transmission="Automatique", mode="rent", monthly_price=249),
            Vehicle(brand="Tesla", model="Model 3", year=2020, mileage=52000, energy="Électrique", transmission="Automatique", mode="sale", price=29900),
            Vehicle(brand="Volkswagen", model="Golf", year=2023, mileage=12000, energy="Diesel", transmission="Automatique", mode="rent", monthly_price=329),
            Vehicle(brand="Toyota", model="Yaris", year=2021, mileage=35000, energy="Hybride", transmission="Automatique", mode="sale", price=15900),
        ])
        db.commit()

    client = db.query(User).filter(User.email == USER_EMAIL).first()
    first_vehicle = db.query(Vehicle).first()
    if client and first_vehicle and db.query(Application).count() == 0:
        db.add(Application(user_id=client.id, vehicle_id=first_vehicle.id, offer_type=first_vehicle.mode, message="Dossier de démonstration", status="pending"))
        db.commit()
