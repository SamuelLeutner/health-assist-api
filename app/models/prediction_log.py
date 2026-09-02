from sqlalchemy import Column, Integer, String
from app.database import Base


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    input_data = Column(String)
    prediction_result = Column(String)
