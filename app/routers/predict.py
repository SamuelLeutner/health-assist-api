from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_db
from app.models.prediction_log import PredictionLog
from app.models.user import User
from app.schemas.predict import PredictionLogResponse, PredictRequest, PredictResponse
from app.security.jwt import get_current_user

router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("/", response_model=PredictResponse)
def predict_triage(
    request: PredictRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    triage_category = "Urgência Moderada"

    db_log = PredictionLog(
        user_id=current_user.id,
        input_data=request.symptoms_description,
        prediction_result=triage_category,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return PredictResponse(
        status="success",
        triage_category=triage_category,
        confidence=0.95,
        message="Predição realizada com sucesso.",
    )


@router.get("/{log_id}", response_model=PredictionLogResponse)
def get_prediction_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    log = db.get(PredictionLog, log_id)

    if log is None or log.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction log not found",
        )

    return log
