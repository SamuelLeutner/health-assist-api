from fastapi import APIRouter, Depends
from app.security.jwt import get_current_user
from app.schemas.predict import PredictRequest, PredictResponse

router = APIRouter(prefix="/predict", tags=["Triage Prediction"])

@router.post("", response_model=PredictResponse)
def predict_triage(payload: PredictRequest, current_user: str = Depends(get_current_user)):
    return PredictResponse(
        status="success",
        triage_category="Atendimento Geral (Placeholder)",
        confidence=0.99,
        message=f"Requisição processada com sucesso para o operador autenticado: {current_user}"
    )
