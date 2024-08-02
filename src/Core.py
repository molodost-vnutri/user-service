from datetime import UTC, datetime, timedelta
from typing import Type, Union
from json import dumps

from pika import BlockingConnection, ConnectionParameters
from fastapi import HTTPException
from jwt import decode, encode
from pydantic import BaseModel
from sqlalchemy import select, delete, update, insert

from src.exceptions import ExpireJwtToken, IncorrectJwtToken
from src.settings import settings
from src.database import async_session
from src.shemas import SendMail
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
    async def find_by_id(cls, id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalars().one()
    
    @classmethod
    async def find_all(cls, **filter):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter) # type: ignore
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def model_add(cls, **add_arg):
        async with async_session() as session:
            query = insert(cls.model).values(**add_arg).returning(cls.model.id) # type: ignore
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

class BaseJWT:
    schemas_create: Type[BaseModel] = None
    schemas_validator: Type[BaseModel] = None

    @classmethod
    def decode_token(cls, token: str) -> Union[BaseModel, HTTPException]:
        try:
            payload: dict = decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            exp_payload = str(payload['exp'])
            payload['exp'] = exp_payload
            shemas_use = cls.schemas_validator if cls.schemas_validator else cls.schemas_create
            shemas = shemas_use.parse_obj(payload)
        except:
            raise IncorrectJwtToken
        
        if datetime.now(UTC) > datetime.fromtimestamp(shemas.exp, tz=UTC):
            raise ExpireJwtToken
        
        return shemas

    @staticmethod
    def create_access_token(token: dict, **kwarg) -> str:
        encode_jwt = token.copy()
        expired = datetime.now(UTC) + timedelta(**kwarg)
        encode_jwt['exp'] = expired.timestamp()
        jwt_token = encode(
            payload=encode_jwt,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return jwt_token

class MailBase:
    @classmethod
    def send(body: SendMail):
        SMTP_MAIL: SendMail = SendMail(
            email=body.email,
            subject=body.subject,
            message=body.message
        )
        connection = BlockingConnection(
            ConnectionParameters('localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue='email_queue')

        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=dumps(SMTP_MAIL.model_dump())
        )
        connection.close()