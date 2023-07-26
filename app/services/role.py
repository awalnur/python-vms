from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.models.role import RoleModel
from app.models.user import Role


def get_all_role(db: Annotated[Session, Depends(get_db)]) -> list[RoleModel]:
    role_data = db.query(Role.name, Role.description).all()
    data = {role.name: str(role.description) for role in role_data}
    return data


def get_role(db: Annotated[Session, Depends(get_db())], user_id: str) -> RoleModel:
    role_data = db.query(Role.namen).filter(Role.id == user_id).all()
    return role_data
