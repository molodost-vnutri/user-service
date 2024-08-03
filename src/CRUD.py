from sqlalchemy import select, insert

from src.Core import __BaseCRUD__
from src.models import UserRoles, Users, Roles
from src.database import async_session

class UsersCRUD(__BaseCRUD__):
    model = Users

class UserRolesCRUD(__BaseCRUD__):
    model = UserRoles
    @classmethod
    async def model_add(cls, role, user_id: int):
        async with async_session() as session:
            role_id_res = await RolesCRUD.find_one_or_none(role=role)
            role_id = role_id_res.id
            query = insert(cls.model).values(role_id=role_id, user_id=user_id).returning(cls.model.id) # type: ignore
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()
    @classmethod
    async def model_find_all_roles_current_user(cls, user_id: int):
        async with async_session() as session:
            query = select(Roles.role).join(UserRoles).filter(UserRoles.user_id == user_id)
            result = await session.execute(query)
            roles = result.scalars().all()
            return roles

class RolesCRUD(__BaseCRUD__):
    model = Roles