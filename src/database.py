from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.settings import settings

engine = create_async_engine(settings.DB_URL)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass