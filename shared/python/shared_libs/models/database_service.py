from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class FeedDTO(BaseModel):
    id: UUID
    url: HttpUrl
    site_url: Optional[HttpUrl]
    description: Optional[str]
    title: Optional[str]
    is_active: bool
    last_fetched_at: Optional[datetime]
    etag: Optional[str]
    poll_frequency: int

    model_config = ConfigDict(from_attributes=True)


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
