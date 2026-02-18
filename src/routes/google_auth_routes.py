from fastapi import APIRouter,Depends,HTTPException
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from sqlalchemy.orm import Session
import os

from src.core.database import get_db
from src.utils.security import create_access_token
from src.models.user import User

router= APIRouter(prefix="/auth", tags=["Google Auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

@router.post("/google_auth")
def google_login(token:str,db:Session = Depends(get_db)):
    try:
        idinfo=id_token.verify_oauth2_token(
            token,
            Request(),
            GOOGLE_CLIENT_ID
        )
        email=idinfo["email"]
        name=idinfo["name"]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google token")
    
    ## find the email into db if avaliable
    user=db.query(User).filter(User.email == email).first()
    if user:
        access_token = create_access_token({"sub": user.email})
        return {
        "message": "Email already exists. Logged in successfully.",
        "user": {
            "email": user.email,
            "name": user.name
        }
    }
    if not user:
        user=User(
            name=name,
            email=email,
            password="",  # No password needed for Google
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
    access_token = create_access_token({"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "name": user.name
        }
    }
        

