from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Table, Text
from sqlalchemy.orm import relationship

from app.db.postgres import Base

user_role_association = Table('user_role_association', Base.metadata,
                              Column('user_id', Integer, ForeignKey('tbl_users.id'), primary_key=True),
                              Column('role_id', Integer, ForeignKey('tbl_roles.id'), primary_key=True)
                              )


class User(Base):
    __tablename__ = 'tbl_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Additional columns for soft delete
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    # Define the many-to-many relationship with roles
    roles = relationship('Role', secondary=user_role_association, back_populates='users')

    def delete(self):
        self.is_deleted = True
        self.deleted_at = func.now()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None


class Role(Base):
    __tablename__ = 'tbl_roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    # Define the many-to-many relationship with users
    users = relationship('User', secondary=user_role_association, back_populates='roles')

class UserModel(BaseModel):
    username: str
    email: str | None = None
