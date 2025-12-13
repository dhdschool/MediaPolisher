from typing import Sequence
from uuid import UUID

from models import Feed
from schemas import FeedCreateRequest, FeedUpdateRequest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_feed(db: AsyncSession, feed_data: FeedCreateRequest) -> Feed:
    """Converts a pydantic request into a SQLAlchemy model and saves it to the database

    Args:
        db (AsyncSession): The async database session
        feed_data (FeedCreateRequest): The feed creation request data

    Returns:
        Feed: The SQLAlchemy Feed model instance
    """
    db_feed = Feed(
        url=str(feed_data.url),
        title=feed_data.title,
        site_url=feed_data.site_url,
        description=feed_data.description,
        poll_frequency=feed_data.poll_frequency,
    )

    db.add(db_feed)
    await db.commit()
    await db.refresh(db_feed)
    return db_feed


async def get_feed_by_id(db: AsyncSession, feed_id: UUID) -> Feed | None:
    """Fetches a feed from the database by its UUID

    Args:
        db (AsyncSession): The async database session
        feed_id (UUID): The UUID of the feed to fetch

    Returns:
        Feed | None: The SQLAlchemy Feed model instance or None if not found
    """
    result = await db.execute(select(Feed).where(Feed.id == feed_id))
    return result.scalar_one_or_none()


async def get_all_feeds(db: AsyncSession) -> Sequence[Feed]:
    """Fetches all feeds from the database

    Args:
        db (AsyncSession): The async database session

    Returns:
        list[Feed]: A list of all SQLAlchemy Feed model instances
    """
    result = await db.execute(select(Feed))
    return result.scalars().all()


async def update_feed(
    db: AsyncSession, feed_id: UUID, feed_data: FeedUpdateRequest
) -> Feed | None:
    """Updates a feed in the database

    Args:
        db (AsyncSession): The async database session
        feed_id (UUID): The UUID of the feed to update
        feed_data (FeedUpdateRequest): The feed update request data

    Returns:
        Feed | None: The updated SQLAlchemy Feed model instance or None if not found
    """

    feed = await get_feed_by_id(db, feed_id)
    if not feed:
        return None

    if feed_data.is_active is not None:
        feed.is_active = feed_data.is_active

    if feed_data.last_fetched_at is not None:
        feed.last_fetched_at = feed_data.last_fetched_at

    if feed_data.etag is not None:
        feed.etag = feed_data.etag

    db.add(feed)
    await db.commit()
    await db.refresh(feed)
    return feed
