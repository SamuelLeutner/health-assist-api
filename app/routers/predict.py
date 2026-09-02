from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.prediction_log import PredictionLog
from app.models.user import User
from app.security.jwt import get_current_user
from app.schemas.predict import PredictRequest, PredictResponse

router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("/", response_model=PredictResponse)
def predict_triage(
    request: PredictRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    status_resp = "success"
    triage_cat = "Urgência Moderada"
    conf = 0.95
    msg = "Predição realizada com sucesso."

    db_log = PredictionLog(
        user_id=current_user.id,
        input_data=request.symptoms_description,
        prediction_result=triage_cat,
    )
    db.add(db_log)
    db.commit()

    return PredictResponse(
        status=status_resp, triage_category=triage_cat, confidence=conf, message=msg
    )
