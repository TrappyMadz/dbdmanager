from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from .config import get_settings


engine = create_async_engine(get_settings().db_url)
session = async_sessionmaker(engine)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session() as db:
        yield db