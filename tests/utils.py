from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings

VALID_PREDICT_PAYLOAD = {
    "symptoms_description": "Dor de cabeça forte e febre há dois dias.",
    "patient_age": 30,
}


def bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def forge_token(
    subject: str,
    *,
    key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
    expires_in: timedelta = timedelta(minutes=5),
) -> str:
    claims = {"sub": subject, "exp": datetime.now(timezone.utc) + expires_in}
    return jwt.encode(claims, key, algorithm=algorithm)