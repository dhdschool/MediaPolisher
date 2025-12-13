from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import Settings


# Base class for declarative ORM metadata
class Base(DeclarativeBase):
    pass


engine = create_async_engine(Settings().DB_SERVICE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Creates a database connection that rollsback on errors

    Yields:
        Iterator[AsyncGenerator[AsyncSession, None]]: An async session instance
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()
