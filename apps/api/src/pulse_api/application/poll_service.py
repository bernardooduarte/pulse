from __future__ import annotations

from uuid import UUID

from pulse_api.domain.entities import Poll
from pulse_api.domain.ports import PollRepository


class PollNotFoundError(Exception):
    pass


class PollService:
    """Application layer: orchestrates use cases against the domain and ports.

    Holds no infrastructure knowledge - it is constructed with whatever
    PollRepository implementation the composition root wires in, which is
    what lets unit tests run against an in-memory fake with zero I/O.
    """

    def __init__(self, repository: PollRepository) -> None:
        self._repository = repository

    async def create_poll(self, question: str, options: list[str]) -> Poll:
        poll = Poll.create(question=question, option_labels=options)
        await self._repository.add(poll)
        return poll

    async def get_poll(self, poll_id: UUID) -> Poll:
        poll = await self._repository.get(poll_id)
        if poll is None:
            raise PollNotFoundError(f"Poll {poll_id} was not found.")
        return poll

    async def cast_vote(self, poll_id: UUID, option_id: UUID) -> Poll:
        poll = await self.get_poll(poll_id)
        poll.cast_vote(option_id)
        await self._repository.save(poll)
        return poll
