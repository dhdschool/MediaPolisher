from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import Settings


# Base class for declarative ORM metadata
class Base(DeclarativeBase):
    pass


# Global engine and session factory with lazy initialization
_engine = None
_session_factory = None


def get_engine():
    """Lazily initializes and returns the database engine."""
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            Settings().DB_SERVICE_URL, echo=False, future=True
        )
    return _engine


def get_session_factory():
    """Lazily initializes and returns the session factory."""
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            bind=get_engine(), class_=AsyncSession, expire_on_commit=False
        )
    return _session_factory


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Creates a database connection that rollsback on errors

    Yields:
        Iterator[AsyncGenerator[AsyncSession, None]]: An async session instance
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()
