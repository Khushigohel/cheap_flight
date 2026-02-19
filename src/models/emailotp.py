from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.core.database import Base

class Emailotp(Base):
    __tablename__="email_otps"
    
    id=Column(Integer,primary_key=True,index=True)
    email = Column(String, unique=False)
    otp = Column(String)
    expires_at = Column(DateTime)
    verified = Column(Boolean, default=False)