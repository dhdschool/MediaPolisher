from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db_setup import Base
from .mixins import TimestampMixin, UUIDMixin


class Feed(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "feeds"

    # Metadata fields
    url: Mapped[str] = mapped_column(
        String(2048), unique=True, nullable=False, index=True
    )
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    site_url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)

    # RSS tags
    etag: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_modified: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # State
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_fetched_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_count: Mapped[int] = mapped_column(Integer, default=0)

    # Poll frequency in seconds
    poll_frequnecy: Mapped[int] = mapped_column(
        Integer, default=600
    )  # Default to 10 minutes
