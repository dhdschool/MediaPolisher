import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database_service.models import Feed


@pytest.mark.asyncio
async def test_database_write_read(db_session: AsyncSession):
    # Test write
    new_feed = Feed(url="https://news.ycombinator.com/rss", title="Hacker News")
    db_session.add(new_feed)
    await db_session.commit()

    # Test read
    stmt = select(Feed).where(Feed.url == "https://news.ycombinator.com/rss")
    result = await db_session.execute(stmt)
    fetched_feed = result.scalar_one_or_none()

    # Assertions
    assert fetched_feed is not None
    assert fetched_feed.title == "Hacker News"
    assert fetched_feed.id is not None  # UUID generation + mixin check
