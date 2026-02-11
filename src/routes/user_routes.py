from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.crud.user_registration import create_user
from src.schemas.user import UserCreate,UserResponse
from src.core.database import SessionLocal

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