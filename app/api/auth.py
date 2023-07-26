from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_token
from app.db.postgres import get_db
from app.models.auth import login_request, auth_response, token_model
from app.services.auth import get_user_by_id, get_role, get_user_by_username, authenticate_user

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/login')
def login(db: Annotated[Session, Depends(get_db)], request: Annotated[login_request, Body()])->auth_response:
    # print(request.username)
    userdata = get_user_by_username(db=db, username=request.username)
    # print(userdata.username)
    if userdata is not None:
        if verify_password(password=request.password, hashed_password=userdata.password_hash):
            # print()
            user_role = userdata.roles
            role = [role.name for role in user_role]

            token_data = {
                'user_id': userdata.id,
                'username': userdata.username,
                'role': role,
            }
            token = create_access_token(data=token_data)
            ref_token = create_refresh_token(data=token_data)
            res = {
                'access_token': token,
                'refresh_token': ref_token,
                'token_type': 'bearer',
            }
            return res

    raise HTTPException(detail='Incorrect username or password', status_code=status.HTTP_401_UNAUTHORIZED)


# @router.post('/token')
# def get_token(db: Annotated[Session, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     check = authenticate_user(db, username=form_data.username, password=form_data.password)
#     return

# def refresh_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY_REFRESH, algorithms=[settings.ALGORITHM])
#         username: str = payload.get('sub')
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     return


@router.post("/token", response_model=token_model, include_in_schema=False)
async def get_token(
        db: Annotated[Session, Depends(get_db)],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    userdata = get_user_by_username(db=db, username=form_data.username)
    # print(userdata.username)
    if userdata is not None:
        if verify_password(password=form_data.password, hashed_password=userdata.password_hash):
            # print()
            user_role = userdata.roles
            roles = [role.name for role in user_role]

            token_data = {
                'user_id': userdata.id,
                'username': userdata.username,
                'role': roles,
                'scopes': form_data.scopes
            }
            token = create_access_token(data=token_data)
            ref_token = create_refresh_token(data=token_data)
            res = {
                'access_token': token,
                'refresh_token': ref_token,
                'token_type': 'bearer',
            }
            return res

    raise HTTPException(detail='Incorrect username or password', status_code=status.HTTP_401_UNAUTHORIZED)


@router.get('/tokendata')
def get_tokendata(token: Annotated[str, Depends(verify_token)]):
    return token
    # try:
    #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    #     username: str = payload.get('user_id')
    #     print(payload)
    #     if username is None:
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    #     # token_data = TokenData(username=username)
    # except JWTError:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    # return payload

