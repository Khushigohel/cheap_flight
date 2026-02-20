from src.models.user import User
from src.utils.security import hash_password
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate

def create_user(db: Session,users:UserCreate):
    db_user=User(
        name=users.name,
        email=users.email,
        password=hash_password(users.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 
    return db_user