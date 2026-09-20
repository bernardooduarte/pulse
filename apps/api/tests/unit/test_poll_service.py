from __future__ import annotations

from uuid import UUID

import pytest

from pulse_api.application.poll_service import PollNotFoundError, PollService
from pulse_api.domain.entities import Poll


class InMemoryPollRepository:
    """Fake adapter used only in tests - proves the port abstraction works."""

    def __init__(self) -> None:
        self._polls: dict[UUID, Poll] = {}

    async def add(self, poll: Poll) -> None:
        self._polls[poll.id] = poll

    async def get(self, poll_id: UUID) -> Poll | None:
        return self._polls.get(poll_id)

    async def save(self, poll: Poll) -> None:
        self._polls[poll.id] = poll


@pytest.fixture
def service() -> PollService:
    return PollService(InMemoryPollRepository())


async def test_create_and_fetch_poll(service: PollService) -> None:
    created = await service.create_poll("Best editor?", ["Vim", "VS Code"])

    fetched = await service.get_poll(created.id)

    assert fetched.question == "Best editor?"
    assert len(fetched.options) == 2


async def test_get_missing_poll_raises(service: PollService) -> None:
    with pytest.raises(PollNotFoundError):
        await service.get_poll(UUID(int=0))


async def test_cast_vote_persists_through_repository(service: PollService) -> None:
    created = await service.create_poll("Best editor?", ["Vim", "VS Code"])
    option_id = created.options[0].id

    updated = await service.cast_vote(created.id, option_id)

    assert updated.total_votes == 1
