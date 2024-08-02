from sqlalchemy import select, delete, update, insert
from sqlalchemy.orm import DeclarativeBase

from src.database import async_session
from src.models import Users, UserRoles, Roles

class __BaseCRUD__:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_arg):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_arg) # type: ignore
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_all(cls, **filter):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter) # type: ignore
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def model_add(cls, **add_arg):
        async with async_session() as session:
            query = insert(cls.model).values(**add_arg) # type: ignore
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def model_update(cls, id: int, **update_arg):
        async with async_session() as session:
            query = update(cls.model).filter_by(id=id).values(**update_arg) # type: ignore
            await session.execute(query)
            await session.commit()
    
    @classmethod
    async def model_delete(cls, id: int):
        async with async_session() as session:
            query = delete(cls.model).filter_by(id=id) # type: ignore
            await session.execute(query)
            await session.commit()

class UsersCRUD(__BaseCRUD__):
    model = Users

class UserRolesCRUD(__BaseCRUD__):
    model = UserRoles

class RolesCRUD(__BaseCRUD__):
    model = Roles