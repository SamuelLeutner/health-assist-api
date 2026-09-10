from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.database import init_db
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.routers import auth, health, predict
from app.security.rate_limit import limiter

init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API de Triagem Médica com foco em segurança LGPD e resiliência DoS.",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(SlowAPIMiddleware)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(predict.router)
