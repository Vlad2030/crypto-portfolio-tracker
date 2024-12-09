from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.data import Database

Base = declarative_base()
metadata = MetaData()
engine = create_async_engine(url=Database.url(), echo=False)
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)


async def async_create_all() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_all(engine: AsyncEngine) -> None:
    return metadata.create_all(engine)
