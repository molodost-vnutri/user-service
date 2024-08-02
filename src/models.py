from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    on_create = Column(DateTime, default=datetime.now())
    on_update = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    roles = relationship('UserRoles', back_populates='user')

class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True)
    user_roles = relationship('UserRoles', back_populates='role')

class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))
    user = relationship('Users', back_populates='roles')
    role = relationship('Roles', back_populates='user_roles')