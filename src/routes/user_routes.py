from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from src.crud.user_registration import create_user
from src.schemas.user import UserCreate,UserResponse
from src.core.database import SessionLocal
import random
from src.utils.email_service import send_otp_email
from src.models.emailotp import Emailotp
from datetime import datetime, timedelta
from src.models.user import User
from src.models.emailotp import Emailotp

router=APIRouter(prefix="/users" ,tags=["Users"])

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def generate_otp():
    return str(random.randint(100000,999999))
        
@router.post("/registration",response_model=UserResponse)
def registration(user:UserCreate,db:Session = Depends(get_db)):
    new_user = create_user(db, user)
    
    otp_code = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=5)
    
    otp_entry = Emailotp(email=new_user.email, otp=otp_code, expires_at=expiry)
    db.add(otp_entry)
    db.commit()
    send_otp_email(new_user.email, otp_code) 
    return new_user

@router.post("/verify-email")
def verify_email(email: str, otp: str, db: Session = Depends(get_db)):

    record = db.query(Emailotp).filter(
        Emailotp.email == email,
        Emailotp.verified == False
    ).first()

    if not record:
        raise HTTPException(status_code=400, detail="OTP not found")

    if record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    if record.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    record.verified = True      # Mark OTP verified

    user = db.query(User).filter(User.email == email).first()
    user.is_verified = True

    db.commit()
    return {"message": "Email verified successfully"}