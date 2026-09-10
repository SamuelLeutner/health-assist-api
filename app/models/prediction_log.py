from typing import Optional

from sqlmodel import Field, SQLModel

class PredictionLog(SQLModel, table=True):
    __tablename__ = "prediction_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    input_data: str
    prediction_result: str
