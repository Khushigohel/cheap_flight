import secrets
from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from src.models.user import User
from src.utils.security import hash_password


def create_reset_token(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires = datetime.now(timezone.utc) + timedelta(minutes=15)

    db.commit()
    return token

def reset_password(db: Session, token: str, new_password: str) -> bool:
    user = db.query(User).filter(User.reset_token == token).first()

    if not user or user.reset_token_expires < datetime.now(timezone.utc):
        return False

    now_utc = datetime.now(timezone.utc)
    if user.reset_token_expires < now_utc:
        return False
    
    user.password = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expires = None

    db.commit()
    return True