from fastapi import APIRouter,Depends,HTTPException,status
from src.schemas import user
from src.utils.security import verify_password
from sqlalchemy.orm import Session
from src.crud.user_registration import create_user
from src.schemas.user import MessageResponse, UserCreate,UserResponse
from src.core.database import SessionLocal
from src.schemas.user import LoginRequest, LoginResponse,ForgotPasswordRequest, ResetPasswordRequest, MessageResponse
from src.models.user import User
from src.crud.forgot_password import create_reset_token, reset_password


router=APIRouter(prefix="/users" ,tags=["Users"])

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/registration",response_model=UserResponse)
def registration(user:UserCreate,db:Session = Depends(get_db)):
    return create_user(db,user)


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

@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    token = create_reset_token(db, payload.email)

    # In real apps, email the token
    return {"message": "If the email exists, a reset link has been sent."}

@router.post("/reset-password", response_model=MessageResponse)
def reset_password_route(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    success = reset_password(db, payload.token, payload.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    return {"message": "Password reset successful"}