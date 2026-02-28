from pydantic import BaseModel
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email:str
    password:str

class UserResponse(BaseModel):
    user_id:int
    name: str
    email:str
    
    class Config:
        from_attributes = True
        
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int
    email: EmailStr
    access_token: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class MessageResponse(BaseModel):
    message: str
