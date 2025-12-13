from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from shared_libs.models import FeedCreateRequest, FeedDTO, FeedUpdateRequest
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import create_feed, get_all_feeds, get_feed_by_id, update_feed
from .db_setup import get_db_session

app = FastAPI()


@app.post("/feeds/", response_model=FeedDTO, status_code=status.HTTP_201_CREATED)
async def create_feed_endpoint(
    feed: FeedCreateRequest, db: AsyncSession = Depends(get_db_session)
) -> FeedDTO:
    return await create_feed(db, feed)


@app.get("/feeds/{feed_id}", response_model=FeedDTO)
async def get_feed_endpoint(feed_id: UUID, db: AsyncSession = Depends(get_db_session)):
    db_feed = await get_feed_by_id(db, feed_id)
    if db_feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")
    return db_feed


@app.get("/feeds/", response_model=list[FeedDTO])
async def get_all_feeds_endpoint(db: AsyncSession = Depends(get_db_session)):
    return await get_all_feeds(db)


@app.patch("/feeds/{feed_id}", response_model=FeedDTO)
async def update_feed_endpoint(
    feed_id: UUID,
    feed_update: FeedUpdateRequest,
    db: AsyncSession = Depends(get_db_session),
):
    db_feed = await update_feed(db, feed_id, feed_update)
    if db_feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")
    return db_feed
