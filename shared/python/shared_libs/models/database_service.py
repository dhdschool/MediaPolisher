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
