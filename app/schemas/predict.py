from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    symptoms_description: str = Field(..., min_length=10, example="Febre alta contínua e dor de cabeça há 2 dias.")
    patient_age: int = Field(..., ge=0, le=120, example=29)

class PredictResponse(BaseModel):
    status: str
    triage_category: str
    confidence: float
    message: str
