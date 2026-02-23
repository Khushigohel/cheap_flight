from fastapi import APIRouter,Depends,HTTPException,status
from src.schemas import user
from src.utils.security import verify_password
from sqlalchemy.orm import Session
from src.crud.user_registration import create_user
from src.schemas.user import MessageResponse, UserCreate,UserResponse
from src.core.database import SessionLocal
import random
from src.utils.email_service import send_otp_email
from src.models.emailotp import Emailotp
from datetime import datetime, timedelta
from src.models.user import User
from src.models.emailotp import Emailotp
from src.schemas.user import LoginRequest, LoginResponse,ForgotPasswordRequest,ResetPasswordRequest, MessageResponse
from src.models.user import User
from src.crud.forgot_password import create_reset_token, reset_password

router=APIRouter(prefix="/users" ,tags=["Users"])

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def generate_otp():
    return str(random.randint(100000,999999))
        
# registration api
@router.post("/registration",response_model=UserResponse)
def registration(user:UserCreate,db:Session = Depends(get_db)):
    new_user = create_user(db, user)
    
    otp_code = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=5)
    
    db.query(Emailotp).filter(
        Emailotp.user_id == new_user.user_id).delete()
    db.commit()
    
    otp_entry = Emailotp(user_id=new_user.user_id, otp=otp_code, expires_at=expiry)
    db.add(otp_entry)
    db.commit()
    send_otp_email(new_user.email, otp_code) 
    return new_user

# email verify via otp api
@router.post("/verify-email")
def verify_email(email: str, otp: str, db: Session = Depends(get_db)):

    user=db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found into db please try again later")
    record = db.query(Emailotp).filter(
        Emailotp.user_id == user.user_id,
         Emailotp.otp == otp,
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

# resend otp by email
@router.post("/resend-otp")
def resend_otp(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_code = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=5)

    # delete old OTP
    db.query(Emailotp).filter(
        Emailotp.user_id == user.user_id
    ).delete()

    new_otp = Emailotp(
        user_id=user.user_id,
        otp=otp_code,
        expires_at=expiry
    )

    db.add(new_otp)
    db.commit()

    send_otp_email(user.email, otp_code)

    return {"message": "OTP resent successfully"}

# login api
@router.post("/login", response_model=LoginResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return {
        "message": "Login successful",
        "user_id": user.user_id,
        "email": user.email
    }

# forgot password api
@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    token = create_reset_token(db, payload.email)
    
    # In real apps, email the token
    return {"message": "If the email exists, a reset link has been sent."}

# reset password api
@router.post("/reset-password", response_model=MessageResponse)
def reset_password_route(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    success = reset_password(db, payload.token, payload.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    return {"message": "Password reset successful"}
