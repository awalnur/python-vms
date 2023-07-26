from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.db.postgres import get_db
from app.models.user import User


def get_user_by_username(db: Annotated[Session, Depends(get_db)], username: str):
    user_data = db.query(User).filter(User.username == username).first()

    # print(dict(role))
    return user_data

def get_user_by_id(db: Annotated[Session, Depends(get_db)], user_id: str) -> object:
    user_data = db.query(User).filter(User.id == user_id).first()
    return user_data


def get_role(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = get_user_by_id(db=db, user_id=user_id)
    role_data = user.roles
    return role_data


def authenticate_user(db: Annotated[Session, Depends(get_db)], username: str, password: str):
    user = get_user_by_username(db=db, username=username)
    if user and verify_password(password=password, hashed_password=user.password_hash):
        return user
    return None
