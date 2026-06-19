from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin, applications, auth, monitoring, vehicles
from app.core.database import Base, SessionLocal, engine
from app.core.settings import settings
from app.seed import seed_database
from app.services.monitoring import logger, metrics, now

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_database(db)

app = FastAPI(
    title="M-Motors API",
    description="API de gestion des véhicules, dossiers clients, sécurité et monitoring.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logger(request: Request, call_next):
    start = now()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        duration = now() - start
        metrics.record_request(request.method, request.url.path, status_code, duration)
        logger.info("%s %s status=%s duration=%.4fs", request.method, request.url.path, status_code, duration)


app.include_router(monitoring.router)
app.include_router(auth.router)
app.include_router(vehicles.router)
app.include_router(applications.router)
app.include_router(admin.router)
