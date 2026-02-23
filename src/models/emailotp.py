from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from src.core.database import Base

class Emailotp(Base):
    __tablename__="email_otps"
    
    id=Column(Integer,primary_key=True,index=True)
    email = Column(String, unique=False)
    otp = Column(String)
    expires_at = Column(DateTime)
    verified = Column(Boolean, default=False)
    
    user_id=Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"))