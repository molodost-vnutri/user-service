from datetime import UTC, datetime, timedelta
from typing import Type, Union
from json import dumps

from pika import BlockingConnection, ConnectionParameters
from fastapi import HTTPException
from jwt import decode, encode
from pydantic import BaseModel
from sqlalchemy import select, delete, update, insert

from src.settings import settings
from src.database import async_session
from src.exceptions import IncorrectJwtToken, ExpireJwtToken
from src.shemas import SMailSend

class __BaseCRUD__:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
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
            query = select(cls.model).filter_by(**filter)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def model_add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
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

class BaseJWT:
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
            shemas = cls.schemas_validator.model_validate(payload)
        except:
            raise IncorrectJwtToken
        
        if datetime.now(UTC) > datetime.fromtimestamp(shemas.exp, tz=UTC):
            raise ExpireJwtToken
        
        return shemas

    @staticmethod
    def create_access_token(token: dict, **kwarg) -> str:
        encode_jwt = token.copy()
        expired = datetime.now(UTC) + timedelta(**kwarg)
        encode_jwt.update({'exp': expired})
        jwt_token = encode(
            payload=encode_jwt,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return jwt_token

def send(body: SMailSend):
    SMTP_MAIL: SMailSend = SMailSend(
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