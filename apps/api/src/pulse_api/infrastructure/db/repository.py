from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pulse_api.domain.entities import Poll, PollOption
from pulse_api.infrastructure.db.models import PollModel, PollOptionModel


class SqlAlchemyPollRepository:
    """Inbound-facing adapter implementing the PollRepository port with SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, poll: Poll) -> None:
        model = PollModel(
            id=poll.id,
            question=poll.question,
            is_closed=poll.is_closed,
            options=[
                PollOptionModel(id=o.id, poll_id=poll.id, label=o.label, votes=o.votes)
                for o in poll.options
            ],
        )
        self._session.add(model)
        await self._session.commit()

    async def get(self, poll_id: UUID) -> Poll | None:
        result = await self._session.execute(select(PollModel).where(PollModel.id == poll_id))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_entity(model)

    async def save(self, poll: Poll) -> None:
        result = await self._session.execute(select(PollModel).where(PollModel.id == poll.id))
        model = result.scalar_one()
        model.is_closed = poll.is_closed
        by_id = {o.id: o for o in poll.options}
        for option_model in model.options:
            updated = by_id[option_model.id]
            option_model.votes = updated.votes
        await self._session.commit()

    @staticmethod
    def _to_entity(model: PollModel) -> Poll:
        return Poll(
            id=model.id,
            question=model.question,
            is_closed=model.is_closed,
            created_at=model.created_at,
            options=[
                PollOption(id=o.id, label=o.label, votes=o.votes) for o in model.options
            ],
        )
