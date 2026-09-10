from pydantic import BaseModel, ConfigDict, Field

class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symptoms_description: str = Field(
        ...,
        min_length=10,
        examples=["Febre alta contínua e dor de cabeça há 2 dias."],
    )
    patient_age: int = Field(..., ge=0, le=120, examples=[29])


class PredictResponse(BaseModel):
    status: str
    triage_category: str
    confidence: float
    message: str


class PredictionLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    input_data: str
    prediction_result: str
