from datetime import datetime

from pydantic import BaseModel, HttpUrl


class FeedCreateRequest(BaseModel):
    url: HttpUrl
    title: str
    site_url: HttpUrl | None = None
    poll_frequency: int = 600  # Default to 10 minutes
    description: str | None = None


class FeedUpdateRequest(BaseModel):
    is_active: bool | None = None
    last_fetched_at: datetime | None = None
    etag: str | None = None
