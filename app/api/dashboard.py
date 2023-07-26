from typing import Annotated

from fastapi import APIRouter, Depends, Security
from app.core.security import verify_token
from app.models.user import UserModel

router = APIRouter(prefix='/dashboard', tags=['Dashboard'])


@router.get('/', dependencies=[Depends(verify_token)])
def dashboard(userdata: Annotated[UserModel, Security(scopes='items')]) -> dict:
    return {
        'test': 'test'
    }
