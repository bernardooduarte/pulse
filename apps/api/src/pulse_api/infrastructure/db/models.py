from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class PollModel(Base):
    __tablename__ = "polls"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    question: Mapped[str] = mapped_column(String(280), nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    options: Mapped[list[PollOptionModel]] = relationship(
        back_populates="poll", cascade="all, delete-orphan", lazy="selectin"
    )


class PollOptionModel(Base):
    __tablename__ = "poll_options"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    poll_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("polls.id"), nullable=False)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    votes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    poll: Mapped[PollModel] = relationship(back_populates="options")
