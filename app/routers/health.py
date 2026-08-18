from fastapi import APIRouter

router = APIRouter(tags=["Health Check"])

@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "HealthAssist API"}
