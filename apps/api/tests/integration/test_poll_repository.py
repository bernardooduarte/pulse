from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from pulse_api.domain.entities import Poll
from pulse_api.infrastructure.db.repository import SqlAlchemyPollRepository


async def test_add_and_get_round_trips_through_real_postgres(db_session: AsyncSession) -> None:
    repo = SqlAlchemyPollRepository(db_session)
    poll = Poll.create("Tabs or spaces?", ["Tabs", "Spaces"])

    await repo.add(poll)
    fetched = await repo.get(poll.id)

    assert fetched is not None
    assert fetched.question == "Tabs or spaces?"
    assert {o.label for o in fetched.options} == {"Tabs", "Spaces"}


async def test_save_persists_vote_counts(db_session: AsyncSession) -> None:
    repo = SqlAlchemyPollRepository(db_session)
    poll = Poll.create("Tabs or spaces?", ["Tabs", "Spaces"])
    await repo.add(poll)

    poll.cast_vote(poll.options[0].id)
    await repo.save(poll)

    reloaded = await repo.get(poll.id)
    assert reloaded is not None
    assert reloaded.total_votes == 1
