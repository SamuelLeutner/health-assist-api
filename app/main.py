from fastapi import FastAPI
from app.routers import health, auth, predict
from app.database import engine, Base
from app.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API de Triagem Médica com foco em segurança LGPD e resiliência DoS.",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(predict.router)
