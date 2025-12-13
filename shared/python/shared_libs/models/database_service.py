from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class FeedDTO(BaseModel):
    id: UUID
    url: HttpUrl
    title: Optional[str]
    is_active: bool
    last_fetched_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
