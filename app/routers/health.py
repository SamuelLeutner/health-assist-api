from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health Check"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Verifica se a API está operacional",
)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy", service="HealthAssist API")