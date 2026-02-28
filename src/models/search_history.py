from sqlalchemy import Column,Integer,String,ForeignKey,Date,Float,DateTime
from datetime import datetime
from src.core.database import Base

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    source = Column(String, nullable=False)
    destinations = Column(String, nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    budget = Column(Float, nullable=True)
    searched_at = Column(DateTime, default=datetime.utcnow)