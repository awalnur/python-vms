from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Annotated
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.db.postgres import get_db, SessionLocal
from app.models import auth
from app.models.user import User
from app.services.role import get_all_role
db = SessionLocal()
role = get_all_role(db=db)
db.close()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token",
                                    scopes=role)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)   


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict,
                        expires_delta: Optional[timedelta] = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: Annotated[str, Depends(oauth_scheme)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        _id: str = payload.get("user_id")
        if _id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        _id: str = payload.get("user_id")
        if _id is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception

def get_user(db:Session, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth_scheme)],
    db: Annotated[Session, Depends(get_db)] = Depends(get_db)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = auth.token_data(username=username, scopes=token_scopes)
    except (JWTError, ValidationError):
        raise credentials_exception
    # # user = get_user_by_username(db=db, username=username)
    # if user is None:
    #     raise credentials_exception
    # for scope in security_scopes.scopes:
    #     if scope not in token_data.scopes:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Not enough permissions",
    #             headers={"WWW-Authenticate": authenticate_value},
    #         )
    # return user