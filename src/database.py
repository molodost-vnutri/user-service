from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.settings import settings

engine = create_async_engine(settings.DB_URL)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def init_db():
    with open('roles.sql') as roles:
        roles = roles.read()
    async with async_session() as session:
        Base.metadata.create_all()
        await session.execute(roles)
        await session.commit()